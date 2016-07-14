from astropy.table import Table,Column
from scipy import spatial

def main(args):
    all_seg = np.loadtxt(args.seg_file_name, delimiter=" ",dtype='S2')
    for f, filt in enumerate(args.filter_names):
        check_segs = list(all_seg)
        for seg in all_seg:
            cat_name = args.main_path + seg + '/' + filt + '_clean.cat'
            cat = Table.read(cat_name, format= 'ascii.basic')
            q1, = np.where(cat['IN_MASK'] == 0)
            tree=spatial.KDTree(zip(cat['ALPHA_SKY'][q1], cat['DELTA_SKY'][q1]))
            check_segs.remove(seg)
            for check_seg in check_segs:
                print seg, check_seg
                ch_cat_name = args.main_path + check_seg + '/' + filt + '_clean.cat'
                ch_cat = Table.read(ch_cat_name, format= 'ascii.basic')
                q2, = np.where(ch_cat['IN_MASK'] == 0)
                pts = zip(ch_cat['ALPHA_SKY'][q2], ch_cat['DELTA_SKY'][q2])
                #ch_tree = spatial.KDTree(zip(ch_cat['ALPHA_SKY'][q2], ch_cat['DELTA_SKY'][q2]))
                #s = tree.query_ball_tree(ch_tree,args.tolerance)
                #q,= np.where((np.array(t) != 1) & (np.array(t) != 0 ))
                #multi = [s[q[i]] for i in range(len(q))]
                #t = [len(s[i]) for i in range(len(s))]
                s = tree.query(pts, distance_upper_bound=args.tolerance)
                ch_q, = np.where(s[0]!= np.inf)
                if len(ch_q)==0:
                    continue
                q = s[1][ch_q]
                #If the object in check seg is worse
                cond1 = list(cat['FLAGS'][q] < ch_cat['FLAGS'][ch_q])
                cond2 = list(cat['SNR'][q] > ch_cat['SNR'][ch_q])
                multi, = np.where(cond1 or cond2)
                ch_cat['MULTI_DET'][ch_q][multi] = 1
                obj= [seg + '.'+ str(cat['NUMBER'][q][num]) for num in multi]
                print multi, obj
                ch_cat['MULTI_DET_OBJ'][ch_q][multi] = obj
                print ch_cat['MULTI_DET_OBJ'][ch_q][multi]
                q = np.delete(q, multi)
                ch_q = np.delete(ch_q, multi)

                # object in  seg is worse
                
                cat['MULTI_DET'][q] = 1
                obj= [check_seg + '.'+ str(ch_cat['NUMBER'][c]) for c in ch_q]
                print q, obj
                cat['MULTI_DET_OBJ'][q] = obj
                ch_cat.write(ch_cat_name, format='ascii.basic')
            cat.write(cat_name, format='ascii.basic')  
              

if __name__ == '__main__':
    import subprocess
    import galsim
    import numpy as np
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--filter_names', default= ['f606w','f814w'],
                        help="names of filters [Default: ['f606w','f814w']]")
    parser.add_argument('--main_path',
                        default = '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_training_sample/')
    parser.add_argument('--seg_file_name', default ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt',
                        help="file with all seg id names" )
    parser.add_argument('--tolerance', type=float, default=1/1800.,
                         help="tolerance(in degrees) allowed while comparing objects in 2 seg fields")
    args = parser.parse_args()
    main(args)




    """
#If the object in detction seg is worse
                multi, = np.where(cat['FLAGS'][q1]>ch_cat['FLAGS'][ch_q])
                cat['MULTI_DET'][q][multi] = 1
                obj= [check_seg + '.'+ strch_cat['NUMBER'][ch_q][num] for num in multi]
                cat['MULTI_DET_OBJ'][q][multi] = obj
                #If the object in check seg is worse
                multi, = np.where(cat['FLAGS'][q1]<ch_cat['FLAGS'][ch_q])
                ch_cat['MULTI_DET'][ch_q][multi] = 1
                obj= [seg + '.'+ cat['NUMBER'][q][num] for num in multi]
                ch_cat['MULTI_DET_OBJ'][ch_q][multi] = obj
                x, = np.where(cat['FLAGS'][q1] = ch_cat['FLAGS'][ch_q])
                multi, = np.where(cat['SNR'][q1][x] >= ch_cat['SNR'][ch_q][x])
                ch_cat['MULTI_DET'][ch_q][x][multi] = 1
                obj= [seg + '.'+ cat['NUMBER'][q][x][num] for num in multi]
                ch_cat['MULTI_DET_OBJ'][ch_q][q][multi] = obj
                ch_cat.write(ch_cat_name, format='ascii.basic')"""