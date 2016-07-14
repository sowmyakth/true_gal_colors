
import glob

"""Program to craete a file contating seg ids of all images"""

def main():
	"""Script to create rms map from weight map"""
	path = '/nfs/slac/g/ki/ki19/deuce/AEGIS/unzip/'

	filters = ['f606w', 'f814w']
	file_name = path+'seg_ids.txt'
	names = glob.glob(path + filters[0] + '/'+ '*drz.fits')
    seg_id=[]
    for name in names:
        id = name[10:12]
        seg_id.append(id)
    np.savetxt(file_name, seg_id, delimiter=" ", fmt="%s")


if __name__ == '__main__':
    main()