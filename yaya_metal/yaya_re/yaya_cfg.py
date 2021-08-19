import numpy as np
import os,sys,copy
from myvasp import vasp_func as vf
from myvasp import vasp_create_fcc as vcf

def disorder_atoms(atoms):
    # randomize pos
# follow a random number after each position, sort random number
    natoms = atoms.numbers.shape[0]
    temp = np.hstack([ atoms.positions, \
    np.random.random_sample([natoms, 1]) ])
    ind = np.argsort(temp[:, -1])
    atoms.set_positions(temp[ind, 0:3], apply_constraint=False)
    return atoms
  


def create_random_alloys(atoms_in, cn, nsamples=1, id1=1, vasp5=False):
    atoms = copy.deepcopy(atoms_in)
    natoms = atoms.numbers.shape[0]
   
    # calc natoms_elem
    cn = cn/cn.sum()     
    natoms_elem = np.around( cn * natoms )

# 0 atom
    if natoms_elem.min() < 0.1:
        sys.exit('==> ABORT. natoms is too small. ')

    max_elem = np.argmax( natoms_elem )
#make sure total atoms is natoms
    temp = natoms_elem.sum() - natoms_elem[max_elem]
    natoms_elem[max_elem] = natoms - temp
    print(natoms_elem)

    # new symbols
    symb = np.array([])
#every element
    for i in np.arange(natoms_elem.shape[0]):
#every atom
        for j in np.arange(natoms_elem[i]):
            symb = np.append(symb, i+1)     # 1 is H
    atoms.set_chemical_symbols( symb )
    for i in np.arange(nsamples):
        atoms = disorder_atoms(atoms)
        filename = 'POSCAR_%.2f_%03d'%(cn[0], i + id1 )
        vf.my_write_vasp(atoms, filename, vasp5=vasp5)


###############################################################################################
        
        
'''
#creat 2*2*3 fcc super cell 
a=3.810
ncell = np.array([2,2,3])
vcf.vasp_create_fcc_100(a,ncell)
#default vcf ouput filename
pos_file = 'POSCAR'
pos = vf.my_read_vasp( pos_file)
'''

#create random alloy for different content
'''
c_list = []
for i in range(11):
    new = [0.1*i, 1-0.1*i]
	c_list.append(new)
c_list = np.array(c_list)
# n POSCAR to create for each c
n = int(5)
for i in range(len(c_list)):
	if i!=0 and i!=(len(c_list)-1):
		print(i)
		create_random_alloys(pos, c_list[i], n)
'''

#creat 128 50 50 CONTCAR
#c_n = np.array([0.5,0.5])
#create_random_alloys(pos, c_n, 128, 72)
