# Introduction to brushwood fences for supporting damaged coasts
This is an example of a study case for building a master programe which is based on [Tung Dao Ph.D. thesis](https://doi.org/10.4233/uuid:0251e545-2b71-4eb9-b755-def24a3e0da6). The thesis is about hydraulic performance of wooden fences applied in the Mekong Delta.

---
## Introduction
1. About Tung Dao research

In the past decade the role of wooden fences, containing brushwood and branches, in efforts to restoring mangroves has been recognized since a vast reduction of mangroves occurred along the Mekong deltaic coast. This study aims to better understand the hydrodynamic performance related to the possible mechanism of wave reduction and the influence of wave characteristics on wave damping due to wooden fences and, in this study, brushwood fences in particular.

[The brushwood fence or dam](https://drive.google.com/file/d/11zm1OStK9D_ZhLGszBrhvxqLhdP3CH8G/view?usp=sharing) (used in Indonesia and Suriname) is a soft/green infrastructure used to support a damaged coast. It could be used in either a mangrove coast that already suffered from a mass reduction or an eroded coast. The common structure of the brushwood fence has two main parts, the frame and the inner parts. The frame consists of a large bamboo/tree with a diameter from 8-10 cm forming into two to three parallel rows. The frame has a very low permeable value, in another way, the purpose is to keep inner parts in place. The inner parts construct bunches of tree/bamboo branches with an average diameter of 1-2 cm. The average porosity value of the inner parts is about 80% to 90% which is enough for damping wave energy and promoting sediments and nutrient for mangroves. Although the efficiency of wooden fence on damping waves is presented clearly in Tung Dao thesis, the statement about sediment transport through brushwood fences is carrying out in the future research.

In Tung Dao research, data from experiments, physical and numerical modeling were collected to obtain the background knowledge of the interaction between flows (and waves) and circular cylinders. Firstly, the interaction between flows and cylinders (an array of random cylinders or a random arrangement of cylinders) was investigated to obtain the proper bulk drag coefficient (Cd) for a particular arrangement of the fence's inner part in the separated experiments. The Cd, then, can be used to calibrate the numerical model, [SWASH](http://swash.sourceforge.net/), alongside with the physical data obtained from the wave flume tests. Further investigation about nonlinear waves and wooden fences then was studied by the SWASH model. The relationship between nonlinear waves might play an important role in the sediment transport in the Mekong deltaic coast, and the fence's characteristics were then carried out. Finally, the application of the SWASH model in the real boundary conditions, such as waves and topography, was studied.

This Ph.D. research can finally bring out the knowledge gaps that the previous literature was failed to find. However, there are more contents needed to study, for example, the 2D and 3D studies on hydraulic display for the fence, wave, and flow, and especially, the sediment transport as well as coming back to the goal that is to restore mangrove loss along the Mekong deltaic coasts.

2. Exercise 01

In this section, serval exercises will be provide to describe how wave and wooden fence interact. The python script for this exercise can be found in Exercise 01 directory.

---
## Numerical models
Numerical models have been applied in many fields, and it is more important to apply them to solve the coastal hydraulic problem thank to the rapid development of computing technology. The numerical technique can be based on the finite element method, finite difference method , boundary element method, finite volume method and Eulerian-Lagrangian method. The time-stepping algorithm can be implicit, semi-implicit, explicit, or characteristic-based. The shape function can be of the first order, second order, or a higher order. The modelling can be simplified into different spatial dimensions, i.e., a one-dimensional (1D) model, two-dimensional (2D) depth-integrated model, 2D lateral-integrated model, 2D layered model and 3D model [(Coastal Wiki)](http://www.coastalwiki.org/wiki/Modelling_coastal_hydrodynamics).

1. SWASH

The [SWASH](https://swash.sourceforge.io/) (an acronym of Simulating WAves till SHore) is a non-hydrostatic wave-flow model and is intended to be used for predicting transformation of dispersive surface waves from offshore to the beach for studying the surf zone and swash zone dynamics, wave propagation and agitation in ports and harbours, rapidly varied shallow water flows typically found in coastal flooding resulting from e.g. dike breaks, tsunamis and flood waves, density driven flows in coastal waters, and large-scale ocean circulation, tides and storm surges. Many studies have applied this model to solve coastal problem, including the nearzone, sediment transport, and vegetation interaction. The related publication can be found [here](https://swash.sourceforge.io/references/references.htm).

The SWASH model have been applied in wave propagation to the shore and was validated in many studies, for example, wave attenuation and wave breaking processes in the swash-zone [(Smit, Zijlema, and Stelling, 2013)](https://www.sciencedirect.com/science/article/abs/pii/S0378383913000215?via%3Dihub). Furthermore, most of studies which consider wave reduction due to vegetation are also taken into account the SWASH model with the vegetation implementation as a good tools. 

The PhD thesis of [Phan, L.K. (2019)](https://research.tudelft.nl/en/publications/wave-attenuation-in-coastal-mangroves-mangrove-squeeze-in-the-mek), including a study of the effect of nonlinear wave reduction by vegetation, present an example of applying SWASH model. Moreover, [Cao 2016](https://bioone.org/journals/journal-of-coastal-research/volume-75/issue-sp1/SI75-167.1/Numerical-Modeling-of-Wave-Transformation-and-Runup-Reduction-by-Coastal/10.2112/SI75-167.1.short) studied wave transformation and run up reduction by coastal vegetation and especially the consideration of both horizontal and vertical components of mangroves in SWASH model in study of [Suzuki et al. (2019)](https://www.sciencedirect.com/science/article/abs/pii/S0378383917304179?via%3Dihub) brings to the new explaination for wave attenuation inside an mangrove area. 

Eventually, [Dao et al., 2021](https://journals.open.tudelft.nl/jchs/article/view/5612) validated and calibrated the SWASH model using experimental data of wave damping due to wooden fence by applying the new vegetation implementation equation in [Suzuki et al. 2019](https://www.sciencedirect.com/science/article/pii/S0378383917304179).

The mentioned examples are proven the trust of using this model for further simulations, especially in the laboratory condition, even though it is even more confident if validating the model with the field measurement data. Thus, this model can be a good computational laboratory for studying purpose.

2. Alternative models

Moreover, [SWAN](https://swanmodel.sourceforge.io/) is a third-generation wave model, developed at Delft University of Technology, that computes random, short-crested wind-generated waves in coastal regions and inland waters. Many related publications that taken into account SWAN to solve ocean issues can be found [here](https://swanmodel.sourceforge.io/references/references.htm).

SWAN accounts for the following physics:
  * Wave propagation in time and space, shoaling, refraction due to current and depth, frequency shifting due to currents and non-stationary depth.
  * Wave generation by wind.
  * Three- and four-wave interactions.
  * Whitecapping, bottom friction and depth-induced breaking.
  * Dissipation due to aquatic vegetation, turbulent flow and viscous fluid mud.
  * Wave-induced set-up.
  * Propagation from laboratory up to global scales.
  * Transmission through and reflection (specular and diffuse) against obstacles.
  * Diffraction.

There are also many numerical models that can be suitable for simulating coastal hydralic problems, such as Sbeach, Xbeach, Duros Plus, Litpack, Genesis, Unibest-CL, Delft3D, Telemac, EFDC.

3. SWASH Exercises

Before practicing, it is recommendedn that users should read the User Manual and examples on the official website of SWASH. Also, the brief guideline for installation, interpretation of commnand files and bathymetry for 1D simulation can be found [here](https://colab.research.google.com/drive/1M7YrSOv6xSdRSPI2K2ttvPI689O7bMaU).

In this practice, users successfully run 1D test of wave propagation to the shore from the water depth of 10 m. The forshore slope is 1:10, uniform and rectangular. Still water level is 0.0 m. The wave conditions are regular with Hrms = 1.0 m, and T = 5.5 seconds.

The outputs are wave height at 8 m, 5 m, and 1 m water depth. And calculating wave heights, wavelengths, and wave periods at the same locations from elevation results.

The python scripts will be given in the Exercise 02 directory.
