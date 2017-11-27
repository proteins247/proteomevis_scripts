#!/usr/bin/python
import sys, os, glob

sys.path.append('../utlts/')
from read_in_file import read_in
from parse_data import organism_list, initialize_dict


def get_path(pdb):	
	dir1 = pdb[0]
	dir2 = pdb[1]
	path = "pdb_image/{0}/{1}/{2}".format(dir1, dir2, pdb)
	return path

def get_file():
	f = []
	for (dirpath, dirnames, filenames) in os.walk("pdb_image/"):
		f.extend(filenames)
	return f

def update_file_list(file_list, d):
	update = file_list[:]
	for organism, d_pdb in d.iteritems():
		for pdb in d_pdb:
			pdb_file = pdb+'.png'
			if pdb_file in file_list:
				update.remove(pdb_file)
	return update

def remove_image(update):
	for pdb_file in update:
		path = get_path(pdb_file)
		print path
		os.remove(path)

if __name__ == "__main__":
	file_list = get_file()
	d = initialize_dict('dict')
	for organism in organism_list:
		d[organism] = read_in('pdb', 'uniprot', organism=organism)
	update = update_file_list(file_list, d)
	remove_image(update)
