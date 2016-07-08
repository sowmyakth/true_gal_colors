import numpy as np
import pyfits
import glob
import os
import subprocess

"""Program to add the input fits files in the 2 filters and make a single 
files. The rms files are sqaured and added"""



def add_images():
	"""Script to create rms map from weight map"""
	path = '/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/'
	if os.path.isdir(path+'/added') is False:
		subprocess.call(["mkdir", path+'/added'])
		print "CREATING output folder"
	for fl in glob.glob(path+'/added/*.fits'):
		os.remove(fl)
	file_name = path+'seg_ids.txt'
	all_seg_ids = np.loadtxt(file_name, delimiter=" ",dtype='S2')
	#all_seg_ids=['01']
	filters = ['f606w', 'f814w']	
	for id in all_seg_ids:
		im_data=[]
		var_data=[]
		for f in filters:
			file_name = path + f +'/EGS_10134_'+ id +'_acs_wfc_'+f+'_30mas_unrot_wht.fits'
			hdu1 = pyfits.open(file_name)
			dat = hdu1[0].data
			var = 1/np.array(dat)
			var_data.append(var)
			file_name = path + f +'/EGS_10134_'+ id +'_acs_wfc_'+f+'_30mas_unrot_drz.fits'
			hdu2 = pyfits.open(file_name)
			im = hdu2[0].data
			im_data.append(im)
			hdu1.close()
			hdu2.close()
		final_im = np.sum(im_data,axis=0)
		final_var = np.sum(var_data,axis=0)
		final_wht = 1/final_var
		final_rms = final_var**0.5
		new_name = path+'/added'+'/EGS_10134_'+ id +'_acs_wfc_30mas_unrot_added_drz.fits'
		pyfits.writeto(new_name, final_im)
		new_name = path+'/added'+'/EGS_10134_'+ id +'_acs_wfc_30mas_unrot_added_wht.fits'
		pyfits.writeto(new_name, final_wht)
		new_name = path+'/added'+'/EGS_10134_'+ id +'_acs_wfc_30mas_unrot_added_rms.fits'
		pyfits.writeto(new_name, final_rms)
	
if __name__ == '__main__':
    add_images()