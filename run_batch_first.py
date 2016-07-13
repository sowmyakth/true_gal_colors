#Run this first
#import glob
#names = glob.glob('*drz.fits')
#seg_id=[]
#for name in names:
#    id = name[10:12]
#    seg_id.append(id)
#np.savetxt('/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt', seg_id, delimiter=" ", fmt="%s")
#

#option to pick detection filter


import subprocess
import numpy as np
import glob
import os




def run_batch():
    for fl in glob.glob('outfile/out_*'):
        os.remove(fl)
    file_name ='/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt'
    #all_seg_ids = np.loadtxt(file_name, delimiter=" ",dtype='S2')
    all_seg_ids = ['01']#, '02', '04', '0a'] 
    for seg_id in all_seg_ids:
        print 'SEG ID ', seg_id
        outfile = 'outfile/out_{0}.txt'.format(seg_id)
        com1 = '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_training_sample'
        com2 = 'python get_objects.py --out_path='+ com1
        final_args =['bsub', '-W' , '1:40', '-o', outfile , com2 ]
        final_args.append('--wht_name=EGS_10134_seg_id_acs_wfc_filter_30mas_unrot_rms.fits')
        final_args.append("--wht_type=MAP_RMS")
        final_args.append("--seg_id="+ seg_id)        
        subprocess.call(final_args)
        #subprocess.call('ls')
    #print final_args


if __name__ == '__main__':
    run_batch()