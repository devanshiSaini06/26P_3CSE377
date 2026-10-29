# Corrected Phase-I Report Sections (Step 10 Fixes Applied)
**Project ID:** PT377  
**Title:** Sentinel-2 Multispectral Change Detection for Monitoring Urban Expansion and Loss of Water Bodies  
**Institution:** School of Computer Science and Engineering, IILM University, Greater Noida  
**Team Members:** Shivani (2410031096), Devanshi Saini (2410031106), Saurav Raj (2410031136), Mohit Sharma (2410031144)  
**Supervisor:** Mr. Amit Agrawal (Associate Professor)

---

## 1. Corrected ABSTRACT (Fixed `NBDI` -> `NDBI` typo & grammar)
The rapid loss of lakes, ponds, and wetlands due to accelerated urbanization has become one of the primary drivers of ecological degradation in Indian metropolitan and peri-urban regions. This project presents a satellite-based multispectral change detection framework for quantifying how urban expansion impacts surface hydrology and how inland water bodies shrink over time. The study investigates two contrasting urbanizing regions of India—Greater Noida (Gautam Buddha Nagar, Uttar Pradesh – NCR Region) and Bengaluru Urban (Karnataka)—over a nine-year period from 2018 to 2026 (comprising eight annual transitions). High-resolution (10 m) Sentinel-2 MultiSpectral Instrument (MSI) Level-2A surface reflectance imagery is extracted and cloud-masked via Google Earth Engine (GEE) for both pre-monsoon and post-monsoon seasons. The Normalized Difference Built-up Index (NDBI) is computed to map impervious built-up expansion, while the Modified Normalized Difference Water Index (MNDWI) delineates open surface water, supported by the Normalized Difference Vegetation Index (NDVI) to suppress spectral confusion between built-up shadows, wetland macrophytes, and water surfaces. A temporally anchored Random Forest (RF) supervised classifier trained on 2021 reference labels—combined with a 3-year temporal majority filter and a non-reversion constraint—generates consistent annual Land Use and Land Cover (LULC) maps across four classes (Built-up, Water, Vegetation, and Barren). Post-classification pixel cross-tabulation matrices quantify class-to-class conversions, and the resulting time-series statistics and spatial maps are deployed in an interactive four-view Streamlit dashboard. Empirical findings confirm a statistically significant inverse correlation between built-up growth and surface water spread in both cities ($r = -0.98$ in Greater Noida and $r = -0.99$ in Bengaluru), providing urban development authorities and environmental regulators with a reproducible, cloud-based decision-support tool.

**Keywords:** Sentinel-2, NDBI, MNDWI, NDVI, LULC change detection, Google Earth Engine, urban water body shrinkage, Greater Noida, Bengaluru, Streamlit dashboard

---

## 2. Corrected PROBLEM DEFINITION (Fixed `DEFINATION` -> `DEFINITION` & typos)
India's urban population is expanding rapidly, making it critical to monitor and plan the sustainable utilization of land and surface water resources. Unregulated urban growth converts agricultural land, open spaces, and natural catchment buffers into impervious housing and industrial infrastructure, disrupting natural drainage channels and depleting surface water reservoirs. Two prominent manifestations of this phenomenon are examined in this study:

1. **Greater Noida:** A rapidly developing planned industrial and residential hub in Gautam Buddha Nagar district (Uttar Pradesh, NCR Region) that has undergone intense infrastructure and real-estate expansion over the last decade, placing severe encroachment pressure on peri-urban wetlands such as the Surajpur Bird Sanctuary catchment and Hindon floodplain ponds.
2. **Bengaluru:** The capital of Karnataka and India's primary technology hub, historically sustained by an interconnected network of more than 200 cascading man-made tanks and lakes for water supply, flood buffering, and groundwater recharge. Rapid peri-urban sprawl has fragmented lake catchments (such as Bellandur and Varthur), resulting in surface water shrinkage and macrophyte encroachment.

This study investigates whether a 10 m resolution, multi-index, cloud-computed Random Forest change detection framework—packaged as an accessible web dashboard—can reliably quantify and visualize the spatio-temporal relationship between built-up expansion and surface water body depletion in Greater Noida and Bengaluru between 2018 and 2026.

---

## 3. Corrected LITERATURE SURVEY INTRO (Removed leftover AI sentence)
Table 2.1 summarizes peer-reviewed remote sensing and urban hydrology studies published between 2018 and 2025 covering spectral water/built-up index refinement, lake degradation in Bengaluru and NCR, and Google Earth Engine machine learning workflows.

---

## 4. Corrected Final Reference Entry (Fixed truncated last line)
- **Casal, G. (2022).** Assessment of Sentinel-2 to monitor highly dynamic small water bodies: The case of Louro lagoon (Galicia, NW Spain). *Oceanologia*, 64(1), 88–102. https://doi.org/10.1016/j.oceano.2021.09.004
- **Google Developers (2026).** *Google Earth Engine Sentinel-2 MSI Level-2A (`COPERNICUS/S2_SR_HARMONIZED`) Dataset Documentation*. https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED
