# -*- coding: utf-8 -*-
"""
This function is to calculate wave heights from experiment data or time series data
There are three sub-function inside it, the variance density spectrum, spectral moment, and wavelength calculation
Input: 
    Time series data
    nfft
    Number of column in data file (n, this parameter is depend on measurement sensors)
    The sampling frequency (Fs = 1/dt)
Output: 
    Spectral density, frequency, 
    The zeroth order or signinficant wave heights
    Wave period (this is to compare to the initial input at wave generator)
    
Author: Tung Dao
Year: Sep 2021
"""

def Calculation_EHm0Tp(elevation, nfft, n, Fs):
    import numpy as np
    # This function is to calculate Spectral density at all sensor in the measurement
    # Inputs include the measurement (eta), number of sensors (measured points), and water depth
    # Outputs are spectral density, frequency, wave period, wavelength (deep, intermediate and shallow zones)
    E_tot = []                    # creating an array of variable of spectral density
    f_tot = []                    # creating an array of variable of frequency
    fp_tot = []
    Hm0_tot = []
    for i in range(n):
        # for calculating wave spectrum
        eta_i = elevation[:, i]
        temp_e_tot, temp_f_tot, confLow, confUpp = wave_spectrum(eta_i, nfft, Fs)
        # Update E_tot, f_top
        E_tot = np.append(E_tot, temp_e_tot.flatten())
        f_tot = np.append(f_tot, temp_f_tot.flatten())
        f1 = np.min(temp_f_tot)
        f2 = np.max(temp_f_tot)
        max_id = np.argmax(temp_e_tot)                      # finding index of maximum spectral density
        fp_tot = np.append(fp_tot, temp_f_tot[max_id])      # finding frequency corresponding to max E
        # for calculating wave height
        temp_Hm0_tot = 4*np.sqrt(spectral_moment(temp_f_tot, temp_e_tot, f1, f2, 0))
        Hm0_tot = np.append(Hm0_tot, temp_Hm0_tot)           # update Hm0
    # Convert to array
    E_tot = np.asarray(E_tot, dtype=np.float64).reshape(n, -1).T
    f_tot = np.asarray(f_tot, dtype=np.float64).reshape(n, -1).T
    # Other calculations
    Tp_tot = np.round(1.0/fp_tot,2)
    Tp = np.round(np.mean(Tp_tot), 2)
    f = f_tot[:, 0]    
    return E_tot, fp_tot, f, Hm0_tot, Tp, Tp_tot
    
# Functions used in above calculations
def wave_spectrum(data,nfft, Fs):
    """
    ### Variance density spectrum
    Compute variance spectral density spectrum of the time-series and its 90% confidence intervals.
    The time series is first divided into blocks of length $nfft$ before being Fourier-transformed.
    **Input**:
        * data: time series
        * nfft: block length
        * Fs: sampling frequency (Hz)
    **Output**:
        * E: variance spectral density. The data is meter, then $E$ is in $m^2/Hz$.
        * f: frequency axis (Hz)
    """
    # cal libs
    import numpy as np
    import scipy.signal 
    from scipy.fftpack import fft        # importing Fourer transform package
    from scipy.stats import chi2         # importing confidence interval package
    
    # Function for calcualting wave spectrum from time-series data
    n = len(data)                                 # Length of the time-series
    nfft = int(nfft - (nfft%2))                   # Length of window contain even number
    data = scipy.signal.detrend(data)             # Detrend the time-series
    nBlocks = int(n/nfft)                         # Number of blocks
    data_new = data[0:nBlocks*nfft]                # Completed blocks
    # The organization of the initial time-series into blocks of length nfft
    dataBlock = np.reshape(data_new,(nBlocks,nfft)) # Each column of dataBlock is one block

    # Definition frequency axis 
    df = Fs/nfft                                  # Frequency resolution of spectrum df=1/[Duration of 1 block]
    f = np.arange(0,Fs/2+df,df)                   # Frequency axis (Fs/2 = max frequency)
    fId = np.arange(0,len(f))                     # 

      # Calculation of the variance for each block and for each frequency
    fft_data = fft(dataBlock,n = nfft,axis = 1)   # Frourier transform of the data
    fft_data = fft_data[:,fId]                    # Only one side needed
    A = 2.0/nfft*np.real(fft_data)                # A(i,b) & B(i,b) contain the Frourier coefficients
    B = 2.0/nfft*np.imag(fft_data)                # 
    E = (A**2 + B**2)/2                           # E(i,b) = ai^2/2 = variance at frequency Fi for the data
    # Averaging the variance over the blocks, and divide by df to ge the variance
    E = np.mean(E,axis = 0)/df                    # 
    # Confidence intervals
    edf = round(nBlocks*2)                        # Degrees of freedom
    alpha = 0.1                                   # Calulation of the 90% confidence interval

    confLow = edf/chi2.ppf(1-alpha/2,edf)         # 
    confUpp = edf/chi2.ppf(alpha/2,edf)           #

    return E,f,confLow,confUpp

def spectral_moment(f,E,f1,f2,n):
    import numpy as np
    """
    Calculate the n th-order spectral moment for a given frequency band [fmin, fmax].
    Input:
        E: variance density spectrum
        f: frequency axis
        fmin and fmax (f1 & f2): minimum and maximum frequency considered in the moment calculation
        n: order of moment (if n = 0, it is the zeroth order)
    Output:
        mn: spectral moment. This varible is to calculate wave height in the same order of moment
    """
    if n >= 0:
        ind_f = np.where((f >= f1)&(f <= f2))[0]
    # indices of the frequencies larger than fmin and smaller than fmax
    else:
        ind_f = np.where((f >= f1)&(f <= f2)&(f!=0))[0]
        # when n < 0, f cannot be equal to zero as f^(-N) = (1/f)^(N) = infinity if f = 0
    mn = np.trapz(E[ind_f] * f[ind_f]**n,f[ind_f]);
    
    return mn
    
def wavelength(T, d):
    import numpy as np
    """ 
    Wave length calculation based on period (T) and water depth (d)
    """
    # cosntant
    g = 9.81           # gravitational accleration (m/s2)
    # wavelength at deep water
    L0 = (g*T**2)/(2*np.pi)
    guess = L0
    L = (g*T**2)/(2*np.pi)*np.tanh((2*np.pi)*(d/guess))
    diff = abs(L-guess)
    # wavelength at intermediate water depth and shallow water
    while diff > 0.01:
        diff = abs(L-guess)
        guess = L + (0.5*diff)
        L = (g*T**2)/(2*np.pi)*np.tanh((2*np.pi)*(d/guess))
    
    return L0, L
