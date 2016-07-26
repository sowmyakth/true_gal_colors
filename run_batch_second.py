####### Run remove multi.py before this"
import subprocess
import numpy as np
import glob
import os


def main():
    for fl in glob.glob('outfile/out_2_*'):
        os.remove(fl)
    file_name ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt'
    all_seg_ids = np.loadtxt(file_name, delimiter=" ",dtype='S2')
    for seg_id in all_seg_ids:
        print 'SEG ID ', seg_id
        path='/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_full/'
        outfile = 'outfile/out_2_{0}.txt'.format(seg_id)
        com2 = 'python get_psf.py --out_path='+ path
        final_args =['bsub', '-W' , '2:55', '-o', outfile , com2 ]    
        final_args.append("--bad_stars_file="+ 'bad_stars.txt' )
        final_args.append("--seg_id="+seg_id)
        subprocess.call(final_args)

if __name__ == '__main__':
    main()