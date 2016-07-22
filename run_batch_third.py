import subprocess
import numpy as np
import glob
import os
from astropy.table import Table


def run_clean_pstamps():
    for fl in glob.glob('outfile/out_3*'):
        os.remove(fl)
    file_name ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt'
    all_seg_ids = np.loadtxt(file_name, delimiter=" ",dtype='S2')
    all_seg_ids = ['0a']
    for seg_id in all_seg_ids:
        print 'SEG ID ', seg_id
        path = '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_training_sample/'
        obj_file =  path + seg_id + '/objects_with_p_stamps.txt'
        cat_file = path + seg_id + '/f606w_clean.cat'
        cat = Table.read(cat_file, format="ascii.basic" )
        obj_list = np.loadtxt(obj_file, dtype=int)
        #obj_list=[380, 387, 389, 383]
        obj_list=[1001, 10003, 9, 4 , 7 ,8 ]
        for num in  obj_list:
            outfile = 'outfile/out_3_{0}_{1}.txt'.format(seg_id, num)
            com = 'python clean_pstamp.py --main_path='+ path
            final_args =['bsub', '-W' , '0:55', '-o', outfile , com]
            final_args.append("--seg_id="+seg_id)
            final_args.append("--num="+str(num))
            subprocess.call(final_args)


if __name__ == '__main__':
    run_clean_pstamps()
