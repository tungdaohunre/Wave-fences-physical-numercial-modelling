# -*- coding: utf-8 -*-
"""
Exercise 01: Successfully plot and answer questions:
Question 1:
    1. What is the meausurment duration?
    2. Plot the surface elevation at all locations, at x = 25.5 m, and x = 30.0 m.

Question 2:
    1. What is the maximum value of spectral density at each measurement location?
    2. What is the peak wave period at each location?
    3. Plot the spectral density at x = 24.8 m, x = 25.5 m, and x = 30.0 m.
    4. plot significant wave heights that calculated from experimental data and from the numerical data. 

Author: Tung Dao
Year: 2021
"""
# In[Loading data]
import numpy as np
# Getting data from url
# fname_exp_url = 'https://raw.githubusercontent.com/HoangTungDao/education_python/main/Measure_01.txt'
fname_exp_url = 'https://gitlab.tudelft.nl/hdao/introduction-to-brushwood-fences-for-supporting-damaged-coasts/-/raw/master/Data/Measure_01.txt'
fname_swash_url = 'https://raw.githubusercontent.com/HoangTungDao/education_python/main/Calculate_01.txt'
# Loading data
data_exp = np.loadtxt(fname_exp_url, delimiter = "\t", skiprows = 0)
data_swash = np.loadtxt(fname_swash_url, delimiter = "\t", skiprows = 0)

# Loading constant values
# Start to set serval constant values and call varibles from loaded data. 
g = 9.81                             # gravitational accleration (m/s2)
tstep = 0.01                         # time step
Fs = 1/tstep                         # sampling frequency
d = 0.2                              # water depth
cali = 0.010                         # converting vol to meter

# Experimental data file has 12 columns, first column is time, from 2 to 10 are the measurements
# last two columns are the velocity, no used.
Ts = data_exp[:,0]                   # loading the time recored, time step is 0.01
eta = data_exp[:,1:10]*cali          # loading the surface elevation from data
n = len(eta[1,:])                    # number of measure points
neta = len(eta)                      # length of measurements at 1 column
mduration = (neta-1)*tstep           # measurement duration in seconds
mduration_min = mduration/60         # measurement duration in minutes

# Numerical data with 1 column is the significant wave heights along the profile
# this data was simulated to validate with experimental data above.
# the length of data is 20 m from 19 to 39 m.
Hs_sw = data_swash                   # set Hs
Hs_sw[Hs_sw == -9] = np.nan          # set all value = {-9} to NaN
x_sw = np.linspace(19,39,201)        # create x-axis for Hs_sw

# In[Q&A_1]

# 1. What is the meausurment duration?
# The measurement duration in second is ... seconds
print('The measurement duration in second is about ' + str(mduration) + str(' seconds'))
# The measurement duration in minutes is ... minutes
mduration_min = np.round(mduration_min, 2)
print('The measurement duration in minutes is about ' + str(mduration_min) + str(' minutes'))

# 2. Plot the surface elevation at all locations, at x = 25.5 m, and x = 30.0 m.
nTs = 60
# Total 9 wave gauges including 6 in front of and 3 behind the fence
plt.figure(figsize = (16, 12))
# Plotting all wave signals
plt.subplot(3,1,1)
plt.plot(Ts,eta)
plt.xlim([np.mean(Ts), np.mean(Ts+nTs)])
plt.ylim([-0.1, 0.1])
plt.ylabel('$\eta$ [m]')
plt.title('All locations', fontweight = 'bold')
# Plotting wave signals in front of the fence
plt.subplot(3,1,2)
ni = 5
plt.plot(Ts,eta[:,ni])
plt.xlim([np.mean(Ts), np.mean(Ts+nTs)])
plt.ylim([-0.1, 0.1])
plt.ylabel('$\eta$ [m]')
plt.title('x = ' + str(x_loc[ni]) + str(' [m]'), fontweight = 'bold')
# Plotting wave signals behind the fence
plt.subplot(3,1,3)
ni = 6
plt.plot(Ts,eta[:,ni])
plt.xlim([np.mean(Ts), np.mean(Ts+nTs)])
plt.ylim([-0.1, 0.1])
plt.ylabel('$\eta$ [m]')
plt.xlabel('Time [s]')
plt.title('x = ' + str(x_loc[ni]) + str(' [m]'), fontweight = 'bold')

# In[Q&A_2]

from Calculation_EHm0Tp import Calculation_EHm0Tp
from Calculation_EHm0Tp import wavelength

# Calculations
nfft = 2000
E_exp, fn_exp, f_exp, Hm0_exp, Tp_exp, Tp_exp_all = Calculation_EHm0Tp(eta, nfft, n, Fs)

# Wavelength
L_exp_all = np.zeros(n)
for i in range(n):
  L_exp_all[i], L0_exp = wavelength(Tp_exp_all[i], d)
L0_exp = np.round(L0_exp,2)
L_exp_all = np.round(L_exp_all,2)

# 1. What is the maximum value of spectral density at each measurement location?
E_max = np.zeros(n)                                          # create an array of E_max with n columns/rows
max_id = np.zeros(n)                                         # create an array of f_max_index with n columns/rows
for i in range(n):
  E_max[i] = np.max(E_exp[:,i])
  E_max = np.round(E_max,5)                                  # update E_max
  # Print out the value of spectral density
  print('The maximum value of spectral density at location ' +
        str(x_loc[i]) + str(' m is: ') + str(E_max[i]) + str(' m^2/Hz.'))

# 2. What is the peak wave period at each location?
  # Print out the peak period
  print('The peak wave period at location ' + str(x_loc[i]) + 
        str(' m is: ') + str(Tp_exp_all[i]) + str(' seconds.'))
  # Print out wave length
  print('Wavelength at location ' + str(x_loc[i]) + 
        str(' m is: ') + str(L_exp_all[i]) + str(' m.\n'))
  
# 3. Plot the spectral density at x = 24.8 m, x = 25.5 m, and x = 30.0 m.
plt.figure(figsize= (15, 5))
plt.subplot(1,3,1)
n_loc = 3                                                  # At loction where x_loc = x_loc[3]
plt.plot(f_exp, E_exp[:,n_loc], 'r-')
plt.legend(['x = ' + str(x_loc[n_loc]) + str(' [m]')])
plt.xlim([0, 2])
plt.ylim([0, 0.003])
plt.ylabel('E [$m^2/Hz$]')
plt.xlabel('f [Hz]')
plt.subplot(1,3,2)
n_loc = 5                                                  # At loction where x_loc = x_loc[5]
plt.plot(f_exp, E_exp[:,n_loc], 'b-')
plt.legend(['x = ' + str(x_loc[n_loc]) + str(' [m]')])
plt.xlim([0, 2])
plt.ylim([0, 0.003])
plt.xlabel('f [Hz]')
plt.subplot(1,3,3)
n_loc = 6                                                  # At loction where x_loc = x_loc[6]
plt.plot(f_exp, E_exp[:,n_loc], 'g-')
plt.legend(['x = ' + str(x_loc[n_loc]) + str(' [m]')])
plt.xlim([0, 2])
plt.ylim([0, 0.003])
plt.xlabel('f [Hz]')

# 4. plot significant wave heights that calculated from experimental data and from the numerical data.
plt.figure(figsize= (15, 8))
plt.subplot(2,1,1)
plt.plot(x_loc, Hm0_exp, 'or', x_sw, Hs_sw, 'b-')
plt.ylabel('z-axis [m]]')
plt.xlim([0, 40])
plt.subplot(2,1,2)
plt.plot(xp,zp,'k-',[0, 37],[0.2, 0.2],'b--')            # Black line is the profile, and blue dashed-line is the water level
plt.plot(xfe, zfe, 'k')
plt.annotate('Wooden fence', xy = (26.5, 0.35))
plt.ylabel('z-axis [m]]')
plt.xlim([0, 40])
plt.annotate('Water level', xy = (2, 0.22))