## Cornec 2021 Summary

### Notes

**Objective:**
- Distinguish between chlorophyll a concentrations from phytoplankton biomass or an increase in chlorophyll a per phytoplankton carbon (i.e. **Are there more phytoplankton or are they just emmitting more chlorophyll?**)
- Understand DCM characteristics and conditions in establishment and maintenance

**Dictionary:**
- **DCM:** deep chlorophyll a maximum, can be from DBM and/or DAM
- **DBM:** deep biomass maximum, phytoplankton
- **DAM:** deep photoAcclimation maximum from an increase in chlorophyll a per phytoplankton carbon

**General:**
- DCMs detected from BGB-Argo floats
    - Seasonal dynamics are region-dependent
	- Appearance and depth primarily driven by light attenuation in the upper layer
	- DCM drivers:
		- **Nutrients**
			- Stratified conditions so flux of nutrients from below and thickness of mixed layer allows phytoplankton growth
		- **Light**
			- Surface irradiance and thickness of mixed layer and phytoplankton content control flux of photons to depth favorable to phytoplankton growth
			- require minimum light level in mixed layer
	- Characterize DCM as majority increase in phytoplankton or increase in photoacclimation
		- Use combination of chlorophyll a concentration ([Chla]) and particulate organic carbon concentrations (POC)
	- Presence of DCM has a strong latitudinal and seasonal dependence
		- similar gradient exists in water-column stability; water can remain stratifies to encorage DCM drivers
		- DCMs are permanent and frequent at low latitudes
		- DCMs are sparse and only in the end of spring-summer growth at higher latitudes

	

- BGC-Argo floats
	- measurements:
        - **Cholorophyll a fluorescence (proxy for [Chla])**
        - **Particle backscattering coefficients (bbp) - proxy for POC**
        - Temperature
        - Salinity
        - PAR - Irradiance - photosynthetically available radiance
        - Nitrate
	- Info
		- 10 years of data (2010-2019)
		- 505 profiling floats
		- Coriolis database
		- Also some floats in north atlantic
	- Why better than ships
		-  Ships are expensive for monitoring
        - Ships are area and season specific (sparse data)

**Methods:**
- Classify DCM as DBM or DAM
    - Use shape of [Chla] and bbp by depth plots
    - No phytoplankton [Chla] can develop below 300m
	- DBM when max b<sub>bp_max</sub> > b<sub>bp_min</sub> in first 15 m. Otherwise DAM ([Chla] maximum did not match b<sub>bp_max</sub>)
- K-means Clustering
	- Group by mean DCM depth, mean [Chla] at DCM depth, annual occurrence of DCM profiles, annual occurrence of DBM profiles
    - test k=2-10
	- Another group on intensity, depth, and typology to define 4 zones with a latitudinal pattern (high latitudes in both hemispheres and low-latitude areas)


**Findings:**
- Four regional zones:
	- Shallow maxima zone (SHAZ)
		- high-latitude regions in northern hemisphere
		- DCM growth only in summer months, still sparse during that season
		- intense (2.4 mg chla $m^{-3}$) DCMs
		- shallow (37m)
		- DCMs with high biomass 
		- nitrate limited growth
	- ghost zone (CHOZ)
		- four sub-regions of southern ocean and north atlantic current
		- DCM growth restricted to summer months and are sparse
		- deeper (64m) and less intense (1.4 mg chla $m^{-3}$) than DCMs in SHAZ
		- iron limited growth
	- deep photoacclimation zone (DAZ)
		- DCMs are permanent features
		- permanently stratified conditions
		- low and middle latitudes
		- deep, weak, and photoacclimated DCMS
		- favorable conditions for DCM growth at great depths with low light availability
		- high proportion of DAM profiles
		- growth driven by nutrient inputs from layers below
	- deep biomass zone (DBZ)
		- DCMs are permanent features
		- permanently stratified conditions
		- low and middle latitudes
		- stronger and shallower maxima features than DAZ
		- optimal light and nutrients from DCM growth



