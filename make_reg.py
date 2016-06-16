from astropy.table import Table
import numpy as np


def make_reg():
    """Make region file to identify objects in ds9"""
    seg = '0a'
    filter1 = 'f606w'
    main_path='/nfs/slac/g/ki/ki19/deuce/AEGIS/testing/'+ seg +'_new/'
    header1 ='# Filename: acisf01712N003_evt2.fits[EVENTS] \n'
    header2 ='global color=green dashlist=8 3 width=1 font="helvetica 10 normal" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1 \n'
    header3 = 'physical\n'
    bt_seg_file = main_path + filter1 + '_bright_seg_map.fits'
    ft_seg_file = main_path + filter1 + '_faint_seg_map.fits'
    bt_cat_file = main_path + filter1 + 'bright.cat'
    ft_cat_file = main_path + filter1 + '_faint.cat'
    main_cat_file = main_path + filter1 + '_clean.cat'
    #bt_cat = Table.read(bt_cat_file, format='ascii.basic')
    #ft_cat = Table.read(ft_cat_file, format='ascii.basic')
    main_cat = Table.read(main_cat_file, format='ascii.basic')
    print main_cat.columns
    reg_file = main_path + filter1+'_'+ seg +'_seg.reg'
    print reg_file
    f = open(reg_file,'w')
    f.write(header1+header2+header3)
    cond1 = (main_cat['IS_STAR'] == 0)
    cond2 = (main_cat['IN_MASK'] == 0) 
    cond3  =  (main_cat['SNR'] >= 20)
    q, = np.where(cond1 & cond2 & cond3)
    #q = range(len(main_cat))
    #q, = np.where(cond1)
    for i in q:
    	x0 = main_cat['X_IMAGE'][int(i)]
        y0 = main_cat['Y_IMAGE'][int(i)]
    	r = main_cat['FLUX_RADIUS'][int(i)]
        t = main_cat['THETA_IMAGE'][int(i)]
        e= main_cat['ELLIPTICITY'][int(i)]
        A = 2.5*(main_cat['A_IMAGE'][int(i)])*(main_cat['KRON_RADIUS'][int(i)])
    	x_size = A*(np.absolute(np.sin(t))+(1-e)*np.absolute(np.cos(t)))
        y_size = A*(np.absolute(np.cos(t))+(1-e)*np.absolute(np.sin(t)))
    	str1 = 'box(' + str(x0) +','+ str(y0) +','+ str(x_size) +','+ str(y_size)+','+ str(0) + ')\n'
        f.write(str1)
        if main_cat['IS_BRIGHT'][int(i)] == 1:
        	str1 ='circle('+ str(x0) +','+ str(y0) +',' + str(r*2) + ') # color=red \n'
        else:
        	str1 ='circle('+ str(x0) +','+ str(y0) +',' + str(r*2) + ') # color=blue \n'
        f.write(str1)  	
    f.close()




if __name__ == '__main__':
    make_reg()