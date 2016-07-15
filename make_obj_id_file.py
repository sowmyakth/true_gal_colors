import glob
import numpy as np

"""Program to create a file contating object ids of objects whos postage stamps are drawn
for each segment"""

def main():
    """Script to create rms map from weight map"""
    path = '/nfs/slac/g/ki/ki19/deuce/AEGIS/AEGIS_training_sample/'
    seg_file_name = path+'seg_ids.txt'
    filters = ['f606w', 'f814w']
    seg_file_name = '/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/seg_ids.txt'
    all_segs = np.loadtxt(seg_file_name, delimiter=" ",dtype='S2')
    for seg in all_segs:
        file_path = path +  seg + '/'+'postage_stamps/'
        names = glob.glob(file_path + filters[0] + '*_image.fits')
        names = [names[i].replace(file_path, '') for i in range(len(names))]
        names = [names[i].replace(filters[0] + '_'+ seg + '_', '') for i in range(len(names))]
        num = [names[i].replace('_image.fits', '') for i in range(len(names))]
        num_name = path + '/'+ seg + '/objects_with_p_stamps.txt'
        np.savetxt(num_name, num, delimiter=" ", fmt="%s")


if __name__ == '__main__':
    main()