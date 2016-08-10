# true_gal_colors
This README file describes the python code used to process AEGIS HST images in V and I bands to produce a sample of galxies.
The final products are similar to the COSMOS real galaxy training sample.
The code can be implemented to any HST field data in multiple filters. It takes HST images in multiple bands, identifies objects with SExtractor, classifies those objects as stars and galaxies. Stars are the used to measure the PSF. Galaxies that satisfy certain criterion (see sec: ) are selected for the main catalog. Catalogs are made for each band. A postage stamp image is drawn for each galaxy in the catalog. Each galaxy image will also have a postage stamp of its PSF. The output of the code can be opened with the RealGalaxyCatalog and COSMOSCatalog module of GalSim.

##Requirements:
### Input:
* Image files:
 in fits format along with a weight map in a single folder. The input files for the multiple filters are in  seperate folders.
* Images of PSF at different location on the field for different focus length. The PSF field files for the multiple filters are in seperate folders.
* file with regions for manual masks. Eg: ghosting
* Zero point magnitudes for multiple filters
* Diffraction spike parameters
* Noise map

