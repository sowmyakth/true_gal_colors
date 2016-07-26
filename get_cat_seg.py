import subprocess
import numpy as np
import glob
import os
from astropy.table import Table, Column

def get_cat_seg(args):
    seg = args.seg_id
    filt = args.filter
    cat_name = args.main_path + seg + '/' + filt + '_full.cat'
    cat = Table.read(cat_name, format= 'ascii.basic')
    obj_list= args.main_path + seg + '/objects_with_p_stamps.txt' 
    objs = np.loadtxt(obj_list, dtype="int")
    temp = cat[objs]
    col = Column(np.zeros(len(temp)),name='NOISE_MEAN',dtype='float', description = 'Mean of background noise' )
    temp.add_column(col)
    col = Column(np.zeros(len(temp)),name='NOISE_VARIANCE',dtype='float', description = 'Variance of background noise' )
    temp.add_column(col)
    col= Column(np.zeros(len(temp)),name='stamp_flux',dtype='float', description = 'Total flux in the postage stamp' )
    temp.add_column(col)
    col= Column(np.zeros(len(temp)),name='sn_ellip_gauss',dtype='float')
    temp.add_column(col)
    col= Column(np.zeros(len(temp)),name='min_mask_dist_pixels',dtype='float')
    temp.add_column(col)
    col= Column(np.zeros(len(temp)),name='average_mask_adjacent_pixel_count',dtype='float')
    temp.add_column(col)
    col= Column(np.zeros(len(temp)),name='peak_image_pixel_count',dtype='float')
    temp.add_column(col)
            
    for idx,obj in enumerate(objs):
        path = args.main_path + seg + '/postage_stamps/stamp_stats/'
        stats_file =  path + str(obj) + '_' + filt + '.txt'
        stats = np.loadtxt(stats_file) 
        [b_mean, b_std, flux, min_dist, avg_flux, peak_val, snr ] = stats
        temp['NOISE_MEAN'][idx] = b_mean
        temp['NOISE_VARIANCE'][idx] = b_std**2
        temp['stamp_flux'][idx] = flux
        temp['sn_ellip_gauss'][idx] = snr
        temp['min_mask_dist_pixels'][idx] = min_dist
        temp['average_mask_adjacent_pixel_count'][idx] = avg_flux
        temp['peak_image_pixel_count'][idx] = peak_val
    new_cat_name = args.main_path + seg + '/' + filt + '_with_pstamp.cat'
    print "Catalog with pstamps saved at ", new_cat_name
    temp.write(new_cat_name, format='ascii.basic')  

if __name__ == '__main__':
    import subprocess
    import numpy as np
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--seg_id', default= ['0a'],
                        help="id of segment to run [Default: ['0a']]")
    parser.add_argument('--filter', default= ['f814w'],
                        help="filter of segment to run [Default: ['f814w']]")
    parser.add_argument('--main_path',
                        default = '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_full/')
    parser.add_argument('--seg_file_name', default ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt',
                        help="file with all seg id names" )
    args = parser.parse_args()
    get_cat_seg(args)

