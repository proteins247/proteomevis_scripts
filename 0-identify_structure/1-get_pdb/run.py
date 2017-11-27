#!/usr/bin/python

#download PDB complexes' structures
#some big structures need to be manually downloaded (bundle) 

import sys, os
import urllib

sys.path.append('../../../utlts/')
from read_in_file import read_in
from parse_data import organism_list



def setup():
	for organism in organism_list:
		if os.path.exists(organism):
			os.mkdir(organism)

def save_pdb_file(pdb_list):
	url = "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId="
	not_available_list = []
	for pdb in pdb_list:
		pdb_name = "{0}.pdb".format(pdb)
		if not os.path.exists(pdb_name):
			pdbid = url+str(pdb)
			content = urllib.urlopen(pdbid).read()
			if '404 Not Found' in content: not_available_list.append(pdb)
			else:
				open(pdb_name, "w" ).write(content)
				print pdb_name 
	return not_available_list
 
def check(not_available_list):
	new_list = not_available_list[:]
	for pdb in not_available_list:
		if os.path.exists('{0}-pdb-bundle.tar.gz'.format(pdb)) or os.path.exists('{0}-pdb-bundle.tar'.format(pdb)):
			new_list.remove(pdb)
	if new_list:
		print "copy and paste the {0} structures below in the rcsb.org download feature".format(len(new_list))	#obtain bundle case
		print ",".join(new_list)


if __name__ == "__main__":
	setup()
	d = read_in('pdb', 'uniprot', 'pre_seq2struc')
	pdb_list = [x[:4] for x in d]
	not_available_list = save_pdb_file(set(pdb_list))
	check(not_available_list)	
