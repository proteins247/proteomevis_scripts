#!/usr/bin/python

help_msg = 'generate edges data'

import sys, os
import numpy as np
import collections

CWD = os.getcwd()
UTLTS_DIR = CWD[:CWD.index('proteomevis_scripts')]+'/proteomevis_scripts/utlts'
sys.path.append(UTLTS_DIR)
from parse_user_input import help_message
from read_in_file import read_in
from parse_data import initialize_dict, organism_list, int2organism
from properties import database
from write_sqlite3 import SQLite3
from output import print_next_step


def read_in_ppi_partners():
	d = initialize_dict("dict")
	for organism in organism_list:
		with open("../../1-property_proteomevis/ppi_partner/{0}/ppi_partners.txt".format(organism), "r") as rfile:
			label_list = next(rfile).split('\t')
			label_list = [x.rstrip() for x in label_list]
			for line in rfile:
				word_list = line.split()
				protein = word_list[label_list.index('protein')]	
				ppi = word_list[label_list.index('protein partners'):]
				d[organism][protein] = ppi
	return d	

def prepare_sql(d_org, d_index, d_ppi, d_val):
	line_list = []
	count=0
	for o in range(len(d_org)):
		organism = d_org[o]
		total = len(d_index[organism])
		for p1 in range(total):
			pdb1 = d_index[organism][p1]
			for p2 in range(p1+1, total):
				pdb2 = d_index[organism][p2]
				
				ppi_bool = 0
				if pdb1 in d_ppi[organism]:			#pdb1 might have 0 partners
					if pdb2 in d_ppi[organism][pdb1]:	#pdb1 might not ppi with pdb1	
						ppi_bool = 1

				pdb_pair = pdb1 +','+ pdb2
				if pdb_pair not in d_val[organism][0]:
					pdb_pair = pdb2 +','+ pdb1
				line = [count, o, p1, p2, float(d_val[organism][0][pdb_pair]), float(d_val[organism][1][pdb_pair]), int(d_val[organism][2][pdb_pair]), ppi_bool]
				line_list.append(line)
				count+=1
	return line_list


if __name__ == "__main__":
	help_message(help_msg, bool_org_dir = False)
	d_org = int2organism() 
	d_index = initialize_dict('dict')
	d_val = initialize_dict('list')

	for organism in organism_list:
		pre_d_i = read_in('pdb', 'uniprot', organism=organism)
		pre_d_i = collections.OrderedDict(sorted(pre_d_i.items()))
		d_index[organism] = {i:pdb for i,pdb in enumerate(pre_d_i)}

		for x in ['TM', 'SID', 'nal']:	#, 'align1', 'align2']:	sequence alignments takes up 700MB! makes downloading edges impossible
			d_val[organism].append(read_in(*database(organism, x)))
	d_ppi = read_in_ppi_partners()
	line_list = prepare_sql(d_org, d_index, d_ppi, d_val)

	columns = ['id','species','sourceID','targetID','tm','sid','align_length','ppi']
	write_sqlite = SQLite3('proteomevis_edge', columns, line_list)
	write_sqlite.run()

	print_next_step('../')	
