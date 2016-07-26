
"""File to remove multiple galaxies in a given postage stamp
@input galaxy file, psf file, segmentation map, blank region
"""
from astropy.table import Table
import pyfits
import sys
import os
### make file listing location of empty region
### check multi objects in region

class Main_param:
    """Class containg parameters to pass to run analysis on each galaxy file."""
    def __init__(self,args):
        self.seg_id = args.seg_id
        self.num = args.num
        self.filters = args.filter_names
        self.blank_file = args.blank_file
        string = args.main_string.replace('segid', self.seg_id) 
        string1 = string.replace('num', self.num)        
        self.gal_files, self.psf_files, self.seg_files = {}, {}, {}
        n = len(self.filters)
        self.path = args.main_path + '/' + self.seg_id + '/postage_stamps/' 
        for i in range(n):
            filter1 = self.filters[i]
            string2 = string1.replace('filter', filter1)
            self.gal_files[filter1] = self.path + string2 + args.image_string
            self.psf_files[filter1] = self.path + string2 + args.psf_string
            self.seg_files[filter1] = self.path + string2 + args.seg_string


def div_pixels(seg_map, num):
    """Get pixels that belong to image, other objects, backgroung from
    segmentation map
    """
    s = seg_map.shape 
    xs = range(s[0])           
    ys = range(s[1])
    bl=[]
    oth ={}
    oth_segs=[]
    im = []
    check = 0
    for x in xs:
        for y in ys:
            if seg_map[x,y] == 0 :
                bl.append([x,y])
            elif seg_map[x,y] == int(num)+1 :
                im.append([x,y])
            else :
                if oth.has_key(str(seg_map[x,y])):
                    oth[str(seg_map[x,y])].append([x,y])
                else: 
                    oth[str(seg_map[x,y])] = [[x,y]]
                    oth_segs.append(str(seg_map[x,y]))
    if seg_map[s[0]/2, s[1]/2] != int(num)+1:
        check = 1
    return im, bl, oth, oth_segs, check

def get_dist(x0,y0, arr):
    """return distance between arr points and (x0,y0)"""
    dist = (arr[0] - x0)**2 + (arr[1] - y0)**2



def get_blank_reg(x_r, y_r,
                  bl_files, filt):
    """ Randomly pick one of the empty fields which will be used to replace other object.
    Return region of size x_r * y_r"""
    bls = Table.read(bl_files, format='ascii.basic')
    # get all blank regions larger than required size
    q, = np.where((bls['XSIZE']>=x_r) & (bls['YSIZE']>=y_r) & (bls['FILTER'] == filt) )
    try :
        bl = q[0]
        print 'empty region from file: ' , bls['FILE'][bl]
    except ValueError:
        print("Region to replace is larger than empty sky")
    xmin, xmax = bls['XMIN'][bl], bls['XMAX'][bl] 
    ymin, ymax = bls['YMIN'][bl], bls['YMAX'][bl]
    hdu = pyfits.open(bls['FILE'][bl])
    bl_dat = hdu[0].data[ymin:ymax, xmin:xmax]
    #print 'empty field size', bl_dat.shape
    hdu.close()
    # get 0,0(bottom left corner) of region to pick in the blank file
    s = bl_dat.shape
    x0_min = np.random.randint(s[0]-x_r)
    y0_min = np.random.randint(s[1]-y_r)
    #print 'y0_min, y_r, x0_min, y_r', y0_min, y_r, x0_min, x_r
    x0_max = x0_min + x_r +1
    y0_max = y0_min + y_r +1
    empty = bl_dat[x0_min:x0_max, y0_min:y0_max]
    return empty

def change_others(arr, to_change,
                  bl_files, filt, b_std):
    """Change pixels of  other object to background"""
    #get min max x cordinate 
    #print 'to_change', to_change
    xmin, xmax = np.min(to_change.T[0]), np.max(to_change.T[0])
    #get min max y cordinate 
    ymin, ymax = np.min(to_change.T[1]), np.max(to_change.T[1])            
    xr0 = xmax-xmin
    yr0 = ymax-ymin   
    bl_dat = get_blank_reg(xr0, yr0, bl_files,filt)
    #print 'empty returneed field size', bl_dat.shape
    #align 0,0 of both oth region and blank reg    
    bl_change = np.array([to_change.T[0]-xmin, to_change.T[1]-ymin]).T

    #print bl_change.shape, bl_change
    #print bl_dat.shape
    #print len(to_change)
    bl_pixels = [bl_dat[bl_change[i,0], bl_change[i,1]] for i in range(len(bl_change))]
    bl_mean, bl_std = get_stats(np.array(bl_pixels), str='Blank Region')
    bl_dat = bl_dat/bl_std*b_std    
    ### change pixels of oth in arr to blank value
    for p in range(len(to_change)):
        arr[to_change[p][0],to_change[p][1]] = bl_dat[bl_change[p][0],bl_change[p][1]]
    return arr


def get_stats(arr ,str=None):
    mean = np.mean(arr)
    t2 = arr - mean
    std = np.std(arr)
    t3 = np.sort(arr)
    #diff1s = arr[t3[round(0.84*len(t3))]] - arr[t3[round(0.16*len(t3))]]
    if str:
        print 'Measuring', str
    print 'STATS: mean= ',mean, ' stdev=', std#,diff1s
    return mean, std


def clean_pstamp(args):
    params = Main_param(args)
    for i, f1 in enumerate(params.filters):
        print "Running filter", f1
        if os.path.isdir(params.path + 'stamp_stats') is False:
            subprocess.call(["mkdir", params.path + 'stamp_stats'])
        hdu1 = pyfits.open(params.gal_files[f1])
        hdu2 = pyfits.open(params.seg_files[f1])
        im_dat = hdu1[0].data
        im_hdr = hdu1[0].header
        seg_dat = hdu2[0].data
        hdu1.close()
        hdu2.close()
        shape = im_dat.shape       
        x0, y0= shape[0]/2, shape[1]/2
        im, bl, oth, oth_segs, check = div_pixels(seg_dat, params.num)
        # Some bright object is nearby, dont consider central object
        if len(im)==0:
            print "Ignore object"
            peak_val = 0
            min_dist = 0.
            min_dist_seg = 0.        
            avg_flux = 0
            snr = -1
            info = [0, 0, 0 , min_dist, avg_flux, peak_val, snr ]
            np.savetxt(params.path + 'stamp_stats'+'/'+ params.num + '_'+ f1 + '.txt', info)
            new_im_name = params.path + f1 + '_'+ params.seg_id + '_'+ params.num +'_gal.fits'
            pyfits.writeto(new_im_name, im_dat, im_hdr, clobber=True)
            continue
        peak_val = np.max([[im_dat[im[i][0]][im[i][1]]] for i in range(len(im))])
        bck_pixels = [im_dat[bl[i][0], bl[i][1]] for i in range(len(bl))]
        b_mean, b_std = get_stats(np.array(bck_pixels), str='Image Background')
                
        #if check ==1:
        #    raise AttributeError("Pixel at center isn't main object")
        if len(oth_segs)==0 :
            print "No other object"
            min_dist = 0.
            min_dist_seg =0.        
            pix_near_dist = [shape[0]/2, shape[1]/2]
            avg_flux = get_avg_around_pix(pix_near_dist[0], pix_near_dist[1], im_dat)
            snr = get_snr(im_dat, b_std**2)
            info = [b_mean, b_std, np.sum(im_dat), min_dist, avg_flux, peak_val, snr ]
            np.savetxt(params.path + 'stamp_stats'+'/'+ params.num + '_'+ f1 + '.txt', info)
            new_im_name = params.path + f1 + '_'+ params.seg_id + '_'+ params.num +'_gal.fits'
            pyfits.writeto(new_im_name, im_dat, im_hdr, clobber=True)
            continue
        new_im = im_dat.copy()
        min_dists = []
        pix_min_dists = []
        for oth_seg in oth_segs:
            print "Other obejct detected with id ", oth_seg
            print 'MASKING: ', len(oth[oth_seg]) , ' pixels out of ', seg_dat.size 
            print " Blank files at", params.blank_file
            dist, pix = get_min_dist(x0,y0, np.array(oth[oth_seg]))
            new_im = change_others(new_im, np.array(oth[oth_seg]), params.blank_file, f1, b_std)
            min_dists.append(dist)
            pix_min_dists.append(pix)
            
        #print min_dists, pix_min_dists, oth_segs
        min_dist = np.min(min_dists)
        pix_near_dist = pix_min_dists[np.argmin(min_dists)]
        avg_flux = get_avg_around_pix(pix_near_dist[0], pix_near_dist[1], im_dat)
        snr = get_snr(new_im, b_std**2)
        info = [b_mean, b_std, np.sum(im_dat), min_dist, avg_flux, peak_val, snr]
        np.savetxt(params.path + 'stamp_stats'+'/'+ params.num + '_'+ f1 + '.txt', info)
        new_im_name = params.path + f1 + '_'+ params.seg_id + '_'+ params.num +'_gal.fits'
        print 'CREATED NEW POSTAGE STAMP', new_im_name
        pyfits.writeto(new_im_name, new_im, im_hdr, clobber=True)
        

def get_snr(image_data, b_var):
    img = galsim.Image(image_data)
    try:
        res = galsim.hsm.FindAdaptiveMom(img)
        aperture_noise = np.sqrt(b_var*2.*np.pi*(res.moments_sigma**2))
        sn_ellip_gauss = res.moments_amp / aperture_noise
    except:
        sn_ellip_gauss = -10.
    return sn_ellip_gauss


def get_min_dist(x0,y0,arr):
    dist = np.hypot(arr.T[0]-x0, arr.T[1]-y0)
    min_dist = np.min(dist)
    val = np.argmin(dist)
    return min_dist, arr[val]

def get_avg_around_pix(x0, y0,arr):
    x, y = [x0], [y0]
    if x0>0:
        x.append(x0-1)
    if arr.shape[0]-1>x0:
        x.append(x0+1)
    if y0>0:
        y.append(y0-1)
    if arr.shape[1]-1>y0:
        y.append(y0+1)
    neighb = [arr[i][j] for i in x for j in y]
    avg=sum(neighb)/len(neighb)
    return avg


if __name__ == '__main__':
    import subprocess
    import galsim
    import numpy as np
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--filter_names', default= ['f606w','f814w'],
                        help="names of filters [Default: ['f606w','f814w']]")
    parser.add_argument('--blank_file', type=str, default ='empty_fields.txt' ,
                        help="Path of file containing blank region of sky in each band [Default:'empty_fields.txt']] ")
    parser.add_argument('--main_path', default= '/nfs/slac/g/ki/ki19/deuce/AEGIS/testing/zero_pt/comb_det/',
                        help="Path where image files are stored [Default: '/nfs/slac/g/ki/ki19/deuce/AEGIS/output_table2/'] ")
    parser.add_argument('--main_string', default='filter_segid_num_',
                        help="String of file name with 'ident','segid','filter' instead[Default:'ident_segid_filter_']")
    parser.add_argument('--image_string', default='image.fits',
                        help="String of galaxy image file [Default:'image.fits']")
    parser.add_argument('--psf_string', default='psf.fits',
                        help="String of PSF file[Default:'psf.fits']")
    parser.add_argument('--seg_string', default='seg.fits',
                        help="String of segmentation map file[Default:'seg.fits']")
    parser.add_argument('--seg_id', default='0c',
                        help="Seg id of galaxy to run [Default:'0a']")
    parser.add_argument('--num', default='0',type=str,
                        help="Identifier of galaxy to run [Default:0")
    parser.add_argument('--pixel_scale', default='0.03',
                        help="Pixel scale of galaxy image[Default:'0.03' #arcsec/pixel]")
    args = parser.parse_args()
    clean_pstamp(args)