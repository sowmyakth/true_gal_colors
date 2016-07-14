#Run this first
#import glob
#names = glob.glob('*drz.fits')
#seg_id=[]
#for name in names:
#    id = name[10:12]
#    seg_id.append(id)
#np.savetxt('/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt', seg_id, delimiter=" ", fmt="%s")
#


import subprocess
import numpy as np
import glob
import os


def main():
    for fl in glob.glob('outfile/out_2*'):
        os.remove(fl)
    file_name ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt'
    all_seg_ids = np.loadtxt(file_name, delimiter=" ",dtype='S2')
    #all_seg_ids = ['07','08','16','07','08','0x','16','19']
    #all_seg_ids = ['04'] 
    for seg_id in all_seg_ids:
        print 'SEG ID ', seg_id
        path='/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_training_sample/'
        outfile = 'outfile/out_2_{0}.txt'.format(seg_id)
        com2 = 'python get_psf.py --out_path='+ path
        final_args =['bsub', '-W' , '0:55', '-o', outfile , com2 ]        
        final_args.append("--bad_stars_file="+ 'bad_stars.txt' )
        final_args.append("--seg_id="+seg_id)
        subprocess.call(final_args)



if __name__ == '__main__':
    main()