import subprocess
import numpy as np
import glob
import os
from astropy.table import Table



def run_clean_seg(args):
    seg_id= args.seg_id
    for fl in glob.glob('outfile/out_3_' + seg_id +'_*'):
        os.remove(fl)
    print 'SEG ID ', seg_id
    path = '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_full/'
    obj_file =  path + seg_id + '/objects_with_p_stamps.txt'
    obj_list = np.loadtxt(obj_file, dtype=int)   
    #Re running on images that failed
    all_seg_ids, num = np.loadtxt('run_again.txt', delimiter=" ",dtype='S8').T
    q, = np.where(seg_id==all_seg_ids)
    obj_list = num[q]
    for num in  obj_list:
        outfile = 'outfile/out_3_{0}_{1}.txt'.format(seg_id, num)
        com = 'python clean_pstamp.py'# --main_path='+ path
        final_args =['bsub', '-W' , '0:25',  '-o',outfile, com]
        final_args.append("--seg_id=" + seg_id)
        final_args.append("--num=" + str(num))
        subprocess.call(final_args)

if __name__ == '__main__':
    import subprocess
    import numpy as np
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--seg_id', default= ['0a'],
                        help="id of segment to run [Default: ['0a']]")
    args = parser.parse_args()
    run_clean_seg(args)

