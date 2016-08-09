import subprocess
import glob
import os
import numpy as np


def run_clean_pstamps():
    for fl in glob.glob('outfile/out_3_seg_*'):
        os.remove(fl)
    file_name ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt'
    #all_seg_ids = np.loadtxt(file_name, delimiter=" ",dtype='S2')
    all_seg_ids = [ '0i', '0j', '0k', '0l', '0m',
       '0n', '0o', '0p', '0q', '0r', '0s', '0t', '0u', '0v', '0w', '0x',
       '0y', '0z', '10', '11', '12', '13', '14', '15', '16', '17', '18',
       '19', '1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h', '1i', '1j',
       '1k', '1l', '1m', '1n', '1o', '1p', '1q', '1r']
    all_seg_ids = ['0h']
    for seg_id in all_seg_ids:
        print 'SEG ID ', seg_id
        outfile = 'outfile/out_3_seg_{0}.txt'.format(seg_id)
        com = 'python run_clean_seg.py --seg_id='+ seg_id
        final_args =['bsub', '-W' , '0:55',com ]    
        subprocess.call(final_args)

if __name__ == '__main__':
    run_clean_pstamps()
