import numpy as np
import galsim
import pyfits
from astropy.table import Table

def make_cf(args):
    bls = Table.read(args.blank_file, format='ascii.basic')    
    for f, filt in enumerate(args.filter_names):
        print "Making Correlation function for ", filt
        q, = np.where(bls['FILTER'] == filt) 
        bl = q[0]
        xmin, xmax = bls['XMIN'][bl], bls['XMAX'][bl] 
        ymin, ymax = bls['YMIN'][bl], bls['YMAX'][bl]
        hdu = pyfits.open(bls['FILE'][bl])
        bl_dat = hdu[0].data[ymin:ymax, xmin:xmax]
        hdu.close()
        rng = galsim.BaseDeviate(123456)
        img = galsim.Image(bl_dat)
        cn = galsim.CorrelatedNoise(img, rng=rng, scale=0.03)
        image = galsim.ImageD(80, 80, scale=0.03)
        cf = cn.drawImage(image)
        name = args.out_path+args.out_name.replace('filter', args.file_filter_name[f])
        print "Savings fits file at ", name
        pyfits.writeto( name, cf.array, clobber=True)


if __name__ == '__main__':
    import subprocess
    import numpy as np
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--blank_file', type=str, default ='empty_fields.txt' ,
                        help="Path of file containing blank region of sky in each band [Default:'empty_fields.txt']] ")
    parser.add_argument('--out_path', default= '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_full/AEGIS_training_sample/',
                        help="Path to where you want the output store [Default: /nfs/slac/g/ki/ki19/deuce/AEGISAEGIS_full/AEGIS_training_sample/] ")
    parser.add_argument('--out_name', default='acs_filter_unrot_sci_20_cf.fits',
                        help="File name of image with 'filter' in place in place of actual filter name")
    parser.add_argument('--filter_names', default= ['f606w','f814w'],
                        help="names of filters [Default: ['f606w','f814w']]")
    parser.add_argument('--file_filter_name', default =['V', 'I'] ,
                        help="Name of filter to use ")
    args = parser.parse_args()
    make_cf(args)

