# -*- coding: utf-8 -*-
"""
One of cases in Tung Dao Ph.D. which was recored in the wave flume at Hydraulic Engineering Laboratory to test wave damping due to wooden fences. 
The case is H_s = 0.07 [m], T_p = 2.4 [s], at water depth d = 0.2 [m]. 
There were total 12 gauges, 09 wave gauges that recored surface elevations and 02 velocity gauges. 
However, this exercise only uses 09 wave gauges.
The second data is the significant wave heights simulated in the SWASH model. 
These wave heights are generated along the profile, showed below.

Author: Tung Dao
Year: Sep 2021
"""
# In[Visualized wave flume]
# Loading constant values
# This section is to visualize the profile of Tung Dao work in wave flume. It does not need to load any data. 
import numpy as np
import matplotlib.pyplot as plt

# Visualization the profile, wave gauges, and wooden fences
# Horizontal position of wave gauges
x_loc = np.array([19.2, 19.5, 19.9, 24.8, 25.1, 25.5, 30.0, 30.4, 30.7]);
zgauges = np.repeat(0.22,len(x_loc))

# creating profile as followed by Tung Dao thesis
zp = np.array([-0.50, -0.50, -0.30, 0.0, 0.0, 0.80])
xp = np.array([0, 6, 8, 15, 36, 40])

# Wooden fence
xfe = np.array([np.arange(28.0, 29.25, 0.25),
                np.arange(28.0, 29.25, 0.25)])
zfe = np.array([np.zeros(5),
               np.repeat(0.3, 5)])

# ploting profile
plt.figure(figsize = (15, 10))

plt.subplot(2,1,1)
plt.plot(xp,zp,'k-', [0, 37], [0.2, 0.2], 'b--')   # Black line is the profile, and blue dashed-line is the water level
plt.plot(xfe, zfe, 'k')                            # Wooden fences
plt.annotate('Slope 1/10', xy = (7.48, -0.4))
plt.annotate('Slope 1/20', xy = (11.6, -0.2))
plt.annotate('Horizontal bed', xy = (18, -0.06))
plt.annotate('Wooden fence', xy = (26.5, 0.35))
plt.ylabel('z-axis [m]]')
plt.xlim([0, 40])
plt.annotate('Water level', xy = (2, 0.22))

plt.subplot(2,1,2)
plt.plot(xp,zp,'k-',[0, 37],[0.2, 0.2],'b--')
plt.plot(xfe, zfe, 'k')
plt.plot(x_loc,zgauges,'gv')
plt.annotate('Wave gauges', xy = (18.5, 0.28))
plt.annotate('Wooden fence', xy = (27.5, 0.35))
plt.xlabel('x-axis [m]')
plt.ylabel('z-axis [m]]')
plt.xlim([18, 38])
plt.ylim([-0.05, 0.6])