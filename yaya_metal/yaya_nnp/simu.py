import numpy as np 
from myvasp import vasp_func as vf 
import copy, os, sys, shutil, time
from yaya_metal.yaya_nnp import basic_cal
from yaya_metal.yaya_re import yaya_io


# need file minimize
def minimize(atoms_in):
    os.chdir('minimize')
    yaya_io.write_lammps_data(atoms_in)
    os.system('./run.bash')
    atoms = yaya_io.read_lammps_dump('min')
    os.chdir('../')
    return atoms


def md(atoms_in):
    os.chdir('md')
    yaya_io.write_lammps_data(atoms_in)
    os.system('./run.bash')
    atoms = yaya_io.read_lammps_dump('min')
    os.chdir('../')
    return atoms




# need file lammps
def mc(atoms_in, T, nstep):
    atoms = copy.deepcopy(atoms_in)
    natoms = len( atoms.get_positions() )
  #type of atom
    atom_num = atoms.get_atomic_numbers()
# phy constants
    kB = 8.617333e-5  #[eV/K]	
    kT = kB*T

    # initialization
    #Ef0 total energy
    basic_cal.eval_nnp(atoms_in)
    Ef0 = basic_cal.read_energy(0)
    Ef_all = np.array([Ef0]) 

    #==================================
    # enter MC loop
    for i in np.arange(1, nstep+1):
        # choice two random id
        sid1 = rand_id(natoms)
        sid2 = rand_id(natoms)

        while atom_num[sid1] == atom_num[sid2]:    
            # not same element
            sid1 = rand_id(natoms)
            sid2 = rand_id(natoms)

        
        # eval energy change of new structure
        pos = atoms.get_positions()
        temp = pos[sid1,:].copy()
        pos[sid1,:] = pos[sid2,:].copy()
        pos[sid2,:] = temp.copy()
        
        atoms2 = copy.deepcopy(atoms)
        atoms2.set_positions(pos, apply_constraint=False )
        basic_cal.eval_nnp(atoms2)
        Ef2 = basic_cal.read_energy(0)
        dEf = Ef2 - Ef_all[-1]    
        
        
        #acceptance probability
        P = np.exp( -dEf/kT )
        print(Ef_all[-1],P,Ef2)
        if P > np.random.random_sample() :
          #accept
            atoms = copy.deepcopy(atoms2)
            Ef_new = Ef2
        else:
            Ef_new = Ef_all[-1]
        
        Ef_all = np.append(Ef_all, Ef_new)

    
    return atoms



def rand_id(natoms):
    y = int( np.floor( np.random.random_sample()*natoms ) )
    return y
