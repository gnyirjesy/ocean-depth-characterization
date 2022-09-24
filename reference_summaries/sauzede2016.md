# Sauzède2016 summary

*Note: the database, float details, and prodecures specific to this 2016 paper may or may not align with the data and details we are concerned with for this project in 2022.*

## Goal
*"Develop and examine the potential of a new global method for merging satellite ocean color and physical Argo data to infer the vertical distribution of $b_{bp}$ with a relatively high spatiotemporal resolution, i.e., the resolution of Argo-to-satellite matchup data"*


## Abstract
**SOCA-BBP**: Satellite Ocean-Color merged with Argo data to infer the vertical distribution of the Particulate Backscattering coefficient
- neural netowrk-based method
- three inputs:
        - satellite data: $b_{bp}$ and *chlor-a* surface estimates
        - float data: temperature-salinity profiles at various depths
        - date: to match satellite and float data


## Introduction
**Particulate Organic Carbon (POC)**
- a vector of carbon export, composed of:
    - giogenetic detrital particles
    - microzooplankton
    - heterotorphic bacteria
    - viruses
    - aggregates present in the water column
- ocean sampling measurements are detailed and direct, but insufficient in time-space coverage
- optical sensors allow a broader range of study
- optical proxies developed, namely particulate backscattering coefficient and particulate beam attenuation coefficient

**$b_{bp}$: particulate backscattering coefficient**
- a key bio-optical property to study the space-time dynamic of POC and possibly phytoplankton biomass
    - a widely used optical proxy of POC
    - index of phytoplankton particulate load (dependent on particle size and phytoplankton size structure)
    - possible indicator of phytoplankton carbon and biomass (making it a possible alternative to *chlor-a*)
- can be measured continuously from autonomous floats and satellites sensing ocean color
- understanding $b_{bp}$ can help improve assessments and understanding of global ocean carbon fluxes

**Surface to depth**
- vertical distribution of POC is highly variable in time and space
    - satellites estimates—restricted to the ocean surface—are insufficient to measure carbon production and export
    - therefore extending surface b_bp  measurements (POC proxy) to below-surface b_bp  estimates is complex
    - must combine satellite information with nutrient availability, light regime, and other physical properties of the water column
        - accomplished by over 3800 Argo floats that measure upper 2000m of the ocean


## Data Presentation and Processing
**Bio-Agro floats**
- concurrent vertical profiles of temperature, salinity, and $b_{bp}$
- collect measurements 1000m to the surface with ~1 m resolution
    - collection as infrequent as once every 10 days, and as frequent as 3 times per day
- the databased contained 8300 vertical profiles from 83 floats from 2008 to 2015 (most after 2013)
    - 43% of profiles discarded after satellite matching for 4725 remaining floats
    - temporal data acquisition bias due to lack of satellite images aat high latitudes during fall and winter
    - Southern Hemisphere is underrepresented

**Volume scattering function (VSF)**
- $\beta(\theta,\lambda)$; defined as the angular distribution of scattering relative to the direction of light propagation $\theta$ at the optical wavelength $\lambda$
    - $\beta_p$ for particle contribution
    - $\beta_{sw}$ for pure seawater contribution
- $\theta = 124\degree$ when $\lambda = 700$ nm or 532 nm
- $b_{bp}(\lambda) = 2\pi\chi(\beta_p(124\degree, \lambda) - \beta_{sw}(124\degree, \lambda))$
    - moving foward, $b_{bp}$ indicates $b_{bp}(700)$; all profiles in data were converted to $b_{bp}(700)$ using a power law of spectral dependency

**Matching float profile data to satellite ocean color data**
- satellite $b_{bp}$ data estimated for wavelength of 700 nm
- each Argo profile was matched with the satellite data of surface $b_{bp}(700)$ and chlorophyll *a* concentration (Chl) **using the closest pixel from the standard level 3 eight day MODIS-Aqua composites with a 9 km resolution**
    - source: http://oceancolor.gsfc.nasa.gov


