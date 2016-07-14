# true_gal_colors
This README file describes the python code used to process AAEGIS HST images in V and I bands to produce a sample of galxies.
The final products are similar to the COSMOS real galaxy training sample, except in the AEGIS field and in two filters.
The code can be implemented to any HST field data in multiple filters.

##Requirements:
### Input:
* Image files in fits format along with a weight map in a single folder. The input files for the multiple filters are in  seperate folders.
* fits files containing images of PSF at different loacation on the field at different focus positions. The PSF feild files for the multiple filters are in seperate folders.
* file with regions for manual masks. Eg: ghosting
* zero point magnitudes for multiple filters
* diffraction spike parameters

