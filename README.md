# true_gal_colors
This README file describes the python code used to process AEGIS HST images in V and I bands to produce a sample of galxies.
The final products are similar to the COSMOS real galaxy training sample.
The code can be implemented to any HST field data in multiple filters. It takes HST images in multiple bands, identifies objects with SExtractor, classifies those objects as stars and galaxies. Stars are the used to measure the PSF. Galaxies that satisfy certain criterion (see sec: ) are selected for the main catalog. Catalogs are made for each band. A postage stamp image is drawn for each galaxy in the catalog. Each galaxy image will also have a postage stamp of its PSF. The output of the code can be opened with the RealGalaxyCatalog and COSMOSCatalog module of GalSim.

##Requirements:
### Input Files:
* Image files: Science images in fits format along with its corresponding weight map in a single folder. The input files for the multiple filters are in seperate folders, each folder name being the filter name (file_path/filter/file_name).
* Co-added images 
* Tiny Tim Images: Images of PSF at different location on the field for different focus length. The PSF field files for the multiple filters are in seperate folders.
* File with regions for manual masks. These are regions that upon visual inspection were found to contain artefacts Eg: ghosting, and hence need to be masked out. The ext file contains segment ID, filter, x and y cordinates of the points on a quadrilateral that mark the region to be masked, file name of science image with region to be masked. Note: script identifies and masks regions near saturated stars, hence need not be included in manual masks.
* Noise map: Fits file with covariance matrix of noise feild for each band. Identify blank regions in the science image and compute covariance matrix.(See ipython notebook)
### Input Parmeters for script:
* Zero point magnitudes for multiple filters
* Diffraction spike parameters: These parameters are sused to compute the size of the diffraction spikes. Parameters are [slope(pixels/ADU),intercept(pixels),width(pixels),angle(degrees)]. Slope and intercept relate the FLUX_AUTO of the star to the length the spike (Obtained from a linear fit to the length of the spike measured manually and FLUX_AUTO for 10 saturated stars). the width of the spikes is set with width. Angle gives the angle by which the polygon has to be rotated. 
* Star galaxy params: Parameters used to seperate galaxies and stars in MU_MAX Vs MAG_AUTO plot(x_div, y_div, slope). x_div gives the maximum magnitude, below whch the object is saturated. y_div is the value of surface brightness per pixel for a saturated star. The slope of the line seperating stars and galaxies is given by slope (See ipython notebook)  

## Running the script

The entire pipeline contains 6 scripts that are to be run one after another in the order: 

 I have also included additional scripts to run the above scripts through batch , for faster computation. Note: the script is written to be run on SLAC batch farm with LSF batch system. You might have to tweak it dependeing on how you run



### Script: The script is run entirely in python. make sure the following modules are loaded:
galsim, numpy, astropy, asciidata, subprocess, os, scipy



## Output:
Fits files with galaxy images (in multiple bands), files with psf images (in 
multiple bands), main catalog file, selection file and fits file.
