import numpy as np
import pyfits
import glob
import os


def make_rms_map():
	"""Script to create rms map from weight map"""
	path = '/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/'
	file_name = path+'seg_ids.txt'
	all_seg_ids = np.loadtxt(file_name, delimiter=" ",dtype='S2')
	#all_seg_ids=['01']
	filters = ['f606w', 'f814w']
	for f in filters:
		for fl in glob.glob(path+f+'/*_rms.fits'):
			os.remove(fl)
		for id in all_seg_ids:
			file_name = path + f +'/EGS_10134_'+ id +'_acs_wfc_'+f+'_30mas_unrot_wht.fits'
			hdu = pyfits.open(file_name)
			dat = hdu[0].data
			new_dat = 1/(np.array(dat)**0.5)
			new_header = hdu[0].header
			hdu.close()
			new_name = path + f +'/EGS_10134_'+ id +'_acs_wfc_'+f+'_30mas_unrot_rms.fits'
			pyfits.writeto(new_name, new_dat, new_header)
			



if __name__ == '__main__':
    make_rms_map()