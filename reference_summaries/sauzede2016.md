# Sauzède2016 summary


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