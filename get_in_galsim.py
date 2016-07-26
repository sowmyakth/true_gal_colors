from astropy.io import fits
from astropy.table import Table,Column, vstack, hstack, join
import os,glob


def get_in_galsim(args):
    if os.path.isdir(args.main_path + args.out_dir) is False:
            subprocess.call(["mkdir", args.main_path + args.out_dir])
    else:
    	for fl in glob.glob(args.main_path + args.out_dir+'*'):
            os.remove(fl)
    index_table = assign_num(args)
    for f, filt in enumerate(args.filter_names):
        get_images(args, index_table, filt, args.file_filter_name[f])
    get_main_catalog(args, index_table)
    get_selection_catalog(args, index_table)
    get_fits_catalog(args, index_table)
    
def main_table():
    names = ('IDENT', 'RA', 'DEC', 'MAG', 'BAND', 'WEIGHT', 'GAL_FILENAME')
    names+= ('PSF_FILENAME', 'GAL_HDU', 'PSF_HDU', 'PIXEL_SCALE')
    names+= ('NOISE_MEAN', 'NOISE_VARIANCE', 'NOISE_FILENAME', 'stamp_flux')
    dtype = ('i4', 'f8', 'f8', 'f8', 'S40', 'f8', 'S256')
    dtype+= ('S288', 'i4', 'i4', 'f8')
    dtype+= ('f8', 'f8', 'S208', 'f8')
    table = Table(names=names, dtype=dtype)
    return table
    
			
def selection_table():
    names = ('IDENT', 'dmag', 'sn_ellip_gauss', 'min_mask_dist_pixels')
    names+= ('average_mask_adjacent_pixel_count', 'peak_image_pixel_count')
    dtype = ('i4', 'f8', 'f8', 'f8', 'f8', 'f8')
    table = Table(names=names, dtype=dtype)
    return table


def fits_table():
    names = ('IDENT', 'mag_auto', 'flux_radius', 'zphot','fit_mad_s', 'fit_mad_b')
    names+= ('fit_dvc_btt', 'use_bulgefit', 'viable_sersic', 'flux')
    dtype = ('i4', 'f8', 'f8', 'f8', 'f8','f8')
    dtype+= ('f8', 'i4', 'i4', 'f8')
    table = Table(names=names, dtype=dtype,)
    col = Column( name='sersicfit', shape=(8,), dtype='f8')
    table.add_column(col, index=4)
    col = Column( name='bulgefit', shape=(16,), dtype='f8')
    table.add_column(col, index=5)
    col = Column( name='fit_status', shape=(5,), dtype='i4')
    table.add_column(col, index=6)
    col = Column( name='hlr', shape=(3,), dtype='f8')
    table.add_column(col)
    return table

def get_main_catalog(args, index_table):
    """Make catlog containing info about all galaxies in final catalog.
    Columns are identical to cosmos real galaxy catalog"""
    print "Creating main catalog" 
    all_seg_ids = np.loadtxt(args.seg_list_file, delimiter=" ",dtype='S2')
    for f, filt in enumerate(args.filter_names):
    	final_table = main_table()
        for seg_id in all_seg_ids:
            file_name = args.main_path + seg_id + '/' + filt + '_with_pstamp.cat'
            seg_cat = Table.read(file_name, format='ascii.basic')
            q, = np.where(index_table['SEG_ID'] == seg_id)
            indx_seg = index_table[q]
            temp = join(seg_cat, indx_seg, keys='NUMBER')
            col = Column(temp['HDU'], name='PSF_HDU')
            temp.add_column(col)
            temp.rename_column('MAG_AUTO', 'MAG')
            temp.rename_column('HDU', 'GAL_HDU')
            p_scales = np.ones(len(q))*0.03
            weights = np.ones(len(q))
            im = [args.gal_im_name.replace('filter', args.file_filter_name[f])]*len(q)
            im_names = [im[i].replace('umber',str(temp['FILE_NUM'][i])) for i in range(len(im))]
            psf = [args.psf_im_name.replace('filter', args.file_filter_name[f])]*len(q)
            psf_names = [psf[i].replace('umber',str(temp['FILE_NUM'][i])) for i in range(len(psf))]
            names = ('WEIGHT','GAL_FILENAME', 'PSF_FILENAME', 'PIXEL_SCALE')
            dtype =('f8', 'S256', 'S288', 'f8')
            tab = [weights, im_names, psf_names, p_scales]
            temp2 = Table(tab, names=names, dtype=dtype)
            temp = hstack([temp,temp2])
            final_table = vstack([final_table,temp], join_type='inner')
        path = args.main_path + args.out_dir 
        cat_name = args.cat_name.replace('filter', args.file_filter_name[f])
        final_table.write(path + cat_name, format='ascii.basic')

def get_selection_catalog(args, index_table):
    """Make catlog containing info about all galaxies in final catalog.
    Columns are identical to cosmos real galaxy catalog"""
    print "Creating selection catalog" 
    all_seg_ids = np.loadtxt(args.seg_list_file, delimiter=" ",dtype='S2')
    for f, filt in enumerate(args.filter_names):
    	final_table = selection_table()
        for seg_id in all_seg_ids:
            file_name = args.main_path + seg_id + '/' + filt + '_with_pstamp.cat'
            seg_cat = Table.read(file_name, format='ascii.basic')
            q, = np.where(index_table['SEG_ID'] == seg_id)
            indx_seg = index_table[q]
            temp = join(seg_cat, indx_seg, keys='NUMBER')
            col =Column(np.zeros(len(q)), name='dmag')
            temp.add_column(col)
            final_table = vstack([final_table,temp], join_type='inner')
        path = args.main_path + args.out_dir 
        file_name = args.selec_file_name.replace('filter', args.file_filter_name[f])
        final_table.write(path + file_name, format='ascii.basic')

def get_fits_catalog(args, index_table):
    """Make catlog containing info about all galaxies in final catalog.
    Columns are identical to cosmos real galaxy catalog"""   
    print "Creating fits catalog" 
    all_seg_ids = np.loadtxt(args.seg_list_file, delimiter=" ",dtype='S2')
    for f, filt in enumerate(args.filter_names):
    	final_table = fits_table()
        for seg_id in all_seg_ids:
            file_name = args.main_path + seg_id + '/' + filt + '_with_pstamp.cat'
            seg_cat = Table.read(file_name, format='ascii.basic')
            q, = np.where(index_table['SEG_ID'] == seg_id)
            indx_seg = index_table[q]
            temp = join(seg_cat, indx_seg, keys='NUMBER')
            temp.rename_column('MAG_AUTO', 'mag_auto')
            temp.rename_column('FLUX_RADIUS', 'flux_radius')            
            col = Column(temp['stamp_flux'], name='flux')
            temp.add_column(col)
            zphot = np.zeros(len(q))
            fit_mad_s = np.zeros(len(q))
            fit_mad_b= np.zeros(len(q))
            fit_dvc_btt = np.zeros(len(q))
            use_bulgefit = np.zeros(len(q))
            viable_sersic = np.zeros(len(q))
            fit_status = [[1]*5]*len(q)
            sersicfit = [[0]*8]*len(q)
            bulgefit = [[0]*16]*len(q)
            hlr = [[0]*3]*len(q)
            names = ('zphot','fit_mad_s', 'fit_mad_b', 'fit_dvc_btt', 'use_bulgefit')
            names+= ('viable_sersic', 'fit_status', 'sersicfit', 'bulgefit', 'hlr')
            dtype =('f8', 'f8', 'f8', 'f8','i4')
            dtype+=('i4', 'i4','f8', 'f8', 'f8')
            tab = [zphot, fit_mad_s, fit_mad_b, fit_dvc_btt, use_bulgefit]
            tab+= [viable_sersic, fit_status, sersicfit, bulgefit, hlr]
            temp2 = Table(tab, names=names, dtype=dtype)
            temp = hstack([temp,temp2])
            final_table = vstack([final_table,temp], join_type='inner')
        path = args.main_path + args.out_dir 
        file_name = args.fits_file_name.replace('filter', args.file_filter_name[f])
        print "Savings fits file at ", path + file_name
        #import ipdb;ipdb.set_trace()
        final_table.write(path + file_name)


def get_images(args, index_table,
               filt, filt_name):
    """Make fits files of postage stamps"""
    print "Saving images"
    n = np.max(index_table['FILE_NUM'])
    for f in range(1,n+1):
        hdu_count = 0
        q, = np.where(index_table['FILE_NUM'] == f)
        im_hdul = fits.HDUList()
        psf_hdul = fits.HDUList()
        for i in q:
            path = args.main_path + '/' + index_table['SEG_ID'][i]+'/postage_stamps/'
            name = filt + '_' + index_table['SEG_ID'][i]+ '_' +str(index_table['NUMBER'][i])+'_image.fits'
            im_file=  path + name
            name = filt + '_' + index_table['SEG_ID'][i]+ '_' +str(index_table['NUMBER'][i])+'_psf.fits'
            psf_file =  path + name
            im = fits.open(im_file)[0].data
            psf = fits.open(psf_file)[0].data
            im_hdul.append(fits.ImageHDU(im))
            psf_hdul.append(fits.ImageHDU(psf))
            index_table['HDU'][i] = hdu_count
            hdu_count+=1
        path = args.main_path + args.out_dir 
        im_name = args.gal_im_name.replace('umber', str(f))
        im_name = im_name.replace('filter', filt_name)
        im_name = path + im_name
        psf_name = args.psf_im_name.replace('umber', str(f))
        psf_name = psf_name.replace('filter', filt_name)
        psf_name = path + psf_name
        im_hdul.writeto(im_name, clobber=True)
        psf_hdul.writeto(psf_name, clobber=True)


def assign_num(args):
    """Assign individual identification number to each object"""
    print "Assigning number"
    names = ('SEG_ID', 'NUMBER', 'IDENT', 'FILE_NUM', 'HDU')
    dtype = ('string', 'int', 'int' ,'int', 'int')
    index_table = Table(names=names, dtype = dtype)
    ident = 0
    #objects detected same in all filters. So read catalog only of first filter
    filt = args.filter_names[0]
    all_seg_ids = np.loadtxt(args.seg_list_file, delimiter=" ",dtype='S2')
    for seg_id in all_seg_ids:
        #for filt in args.filter_names
        #    seg_cat = Table.read()
        #    mag.append(seg_cat['MAG_AUTO'])
        #cond1 = (np.max(np.array(mag).T, axis=1) < args.mag_cutoff)
        file_name = args.main_path + seg_id + '/' + filt + '_with_pstamp.cat'
        catalog = Table.read(file_name, format='ascii.basic')
        idents = range(ident,ident+len(catalog))
        seg_ids = [seg_id]*len(catalog)
        numbers = catalog['NUMBER']
        file_nums = np.array(idents)/1000 + 1
        hdus= np.zeros(len(catalog))
        temp = Table([seg_ids, numbers, idents, file_nums, hdus],names=names, dtype = dtype)
        index_table = vstack([index_table,temp])
        ident+=len(catalog)
    return index_table



if __name__ == '__main__':
    import subprocess
    import numpy as np
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--n_filters', type=int, default=2,
                        help="number of image filters [Default: 2]")
    parser.add_argument('--filter_names', default= ['f606w','f814w'],
                        help="names of filters [Default: ['f606w','f814w']]")
    parser.add_argument('--main_path',
                        default = '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_full/')
    parser.add_argument('--out_dir', default = "AEGIS_training_sample/",
                        help="directory containing the final catalog")
    parser.add_argument('--cat_name', default = "AEGIS_galaxy_catalog_filter_25.2.fits",
                        help="Final catalog name")
    parser.add_argument('--gal_im_name', default = "AEGIS_galaxy_images_filter_25.2_number.fits",
                        help="Final name of galaxy images")
    parser.add_argument('--psf_im_name', default = "AEGIS_galaxy_PSF_images_filter_25.2_number.fits",
                        help="Final name of PSF images")
    parser.add_argument('--selec_file_name', default = "AEGIS_catalog_filter_25.2_selection.fits",
                        help="Catalog with selection information")
    parser.add_argument('--file_filter_name', default =['V', 'I'] ,
                        help="Catalog with selection information")
    parser.add_argument('--fits_file_name', default = "AEGIS_catalog_filter_25.2_fits.fits",
                        help="Name of Catalog with fit information")
    parser.add_argument('--seg_list_file', default ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt',
                        help="file with all seg id names" )
    args = parser.parse_args()
    get_in_galsim(args)

