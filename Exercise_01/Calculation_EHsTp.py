# In[Introduction]
"""
# Description
The functions in this package is to calculate significant wave height,
spectral density, and related wave characteristics from time series data.

The main function to calculate mentioned characteristics calls
`Calculation_EHsTp`. Several suport functions are to calculate wave spectrum,
wave momentum in zeroth order (could be in 1$^{st}$ or 2$^{nd}$ order), and
wavelength in specific depth. 
<br><br>
Author: Tung Dao, Dec 2021
"""

# In[Introduction]
"""
* This function is to calculate wave heights from experiment data or time
series data.
* There are three sub-function inside it, the variance density spectrum,
spectral moment, and wavelength calculation
* Input:
    * Time series data
    * nfft
    * Number of column in data file (n, this parameter is depend on
                                     measurement sensors)
    * The sampling frequency (Fs = 1/dt)
* Output: 
    * Spectral density, frequency, 
    * The zeroth order or signinficant wave heights
    * Wave period (this is to compare to the initial input at wave generator)

Author: Tung Dao
Year: Sep 2021
"""

# In[Main function]


def Calculation_EHsTp(data, block_length, measured_points, freq_sample):
    import numpy as np
    """
    This function is to calculate Spectral density at all sensor
        in the measurement
    Inputs: data: Time series water elevation
            ntff: block length
            n: number of sensors (measured points)
            fs: Sampling frequency (Hz)
    Outputs:
            E: spectral density (m^2/Hz)
            f, fp: Range wave frequency & peak wave frequency (Hz)
            Tp: Peak wave period (s)
            Hs: Significant wave heights (m)
    """
    # Create an array of variables:
    Spect_density = []
    freq = []
    freq_peak = []
    Hsig = []
    for i in range(measured_points):
        # for calculating wave spectrum
        eta_i = data[:, i]
        temp_sp, temp_freq, con_a, con_b = wave_spectrum(
            eta_i, block_length, freq_sample)

        # Update E & f
        Spect_density = np.append(Spect_density, temp_sp.flatten())
        freq = np.append(freq, temp_freq.flatten())

        # Set minimum and maximum frequencies
        freq_min = np.min(temp_freq)
        freq_max = np.max(temp_freq)

        # Finding index of maximum spectral density
        max_id = np.argmax(temp_sp)

        # Finding frequency corresponding to max E
        freq_peak = np.append(freq_peak, temp_freq[max_id])

        # Calculating Significant_wave_height
        temp_Hs = 4*np.sqrt(spectral_moment(temp_freq, temp_sp,
                                            freq_min, freq_max, 0))

        # Update Significant_wave_height
        Hsig = np.append(Hsig, temp_Hs)

    # Convert to array: cut 9 column and put into a row
    Spect_density = np.asarray(Spect_density,
                               dtype=np.float64).reshape(measured_points, -1).T
    freq = np.asarray(freq, dtype=np.float64).reshape(measured_points, -1).T

    # Calculate peak wave period from fp
    wperiod_peak = np.round(1.0/freq_peak, 2)
    freq = freq[:, 0]
    return Spect_density, freq, freq_peak, Hsig, wperiod_peak

# In[Functions used in above calculations]


def wave_spectrum(data, nfft, freq_sample):
    """
    ### Variance density spectrum
    Compute variance spectral density spectrum of the time-series and its
        90% confidence intervals.
    The time series is first divided into blocks of length $nfft$ before
        being Fourier-transformed.
    **Input**:
        * data: time series
        * nfft: block length
        * freq_sample: sampling frequency (Hz)
    **Output**:
        * E: variance spectral density. The data is meter, then $E$ is in 
        $m^2/Hz$.
        * freq_axis: frequency axis (Hz)
    """
    # cal libs
    import numpy as np
    import scipy.signal
    from scipy.fftpack import fft        # importing Fourer transform package
    from scipy.stats import chi2         # importing confidence interval package

    # Function for calcualting wave spectrum from time-series data
    # Length of the time-series
    data_length = len(data)
    # Length of window contain even number
    nfft = int(nfft - (nfft % 2))
    data = scipy.signal.detrend(data)             # Detrend the time-series
    nBlocks = int(data_length/nfft)                         # Number of blocks
    data_new = data[0:nBlocks*nfft]                # Completed blocks
    # The organization of the initial time-series into blocks of length nfft
    # Each column of dataBlock is one block
    dataBlock = np.reshape(data_new, (nBlocks, nfft))

    # Definition frequency axis
    # Frequency resolution of spectrum freq_res=1/[Duration of 1 block]
    freq_res = freq_sample/nfft
    # Frequency axis (freq_sample/2 = max frequency)
    freq_axis = np.arange(0, freq_sample/2+freq_res, freq_res)
    fId = np.arange(0, len(freq_axis))                     #

    # Calculation of the variance for each block and for each frequency
    fft_data = fft(dataBlock, nfft, axis=1)   # Frourier transform of the data
    fft_data = fft_data[:, fId]                    # Only one side needed
    # A(i,b) & B(i,b) contain the Frourier coefficients
    fft_A = 2.0/nfft*np.real(fft_data)
    fft_B = 2.0/nfft*np.imag(fft_data)                #
    # E(i,b) = ai^2/2 = variance at frequency Fi for the data
    spectral_density = (fft_A**2 + fft_B**2)/2
    # Averaging the variance over the blocks, and divide by freq_res to ge the variance
    spectral_density = np.mean(spectral_density, axis=0) / \
        freq_res                    #
    # Confidence intervals
    efreq_res = round(nBlocks*2)                        # Degrees of freedom
    # Calulation of the 90% confidence interval
    alpha = 0.1

    confLow = efreq_res/chi2.ppf(1-alpha/2, efreq_res)         #
    confUpp = efreq_res/chi2.ppf(alpha/2, efreq_res)           #

    return spectral_density, freq_axis, confLow, confUpp

# In[Spectral density]


def spectral_moment(freq, spectral_dens, freq_min, freq_max, order):
    import numpy as np
    """
    Calculate the n th-order spectral moment for a given frequency band
    [fmin, fmax].
    Input:
        E: variance density spectrum
        f: frequency axis
        fmin and fmax (f1 & f2): minimum and maximum frequency considered
            in the moment calculation
        order: order of moment (if n = 0, it is the zeroth order)
    Output:
        mn: spectral moment. This varible is to calculate wave height in the
            same order of moment
    """
    if order >= 0:
        ind_freq = np.where((freq >= freq_min) & (freq <= freq_max))[0]
    # indices of the frequencies larger than fmin and smaller than fmax
    else:
        ind_freq = np.where((freq >= freq_min) & (freq <= freq_max) &
                            (freq != 0))[0]
    moment_order = np.trapz(spectral_dens[ind_freq] *
                            freq[ind_freq] ** order, freq[ind_freq])

    return moment_order


# In[Wavelength]


def wavelength(w_period, w_depth):
    import numpy as np
    """ 
    Wave length calculation based on period and water depth
    """
    # cosntant
    grav = 9.81           # gravitational accleration (m/s2)
    # wavelength at deep water
    wlength_0 = (grav * w_period ** 2) / (2 * np.pi)
    guess_wlength = wlength_0
    wlength = (grav * w_period ** 2) / (2 * np.pi) * \
        np.tanh((2 * np.pi) * (w_depth / guess_wlength))
    diff = abs(wlength - guess_wlength)
    # wavelength at intermediate water depth and shallow water
    while diff > 0.01:
        diff = abs(wlength - guess_wlength)
        guess_wlength = wlength + (0.5 * diff)
        wlength = (grav * w_period ** 2) / (2 * np.pi) *\
            np.tanh((2 * np.pi) * (w_depth / guess_wlength))

    return wlength_0, wlength
