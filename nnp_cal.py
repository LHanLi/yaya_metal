import numpy as np
from myvasp import vasp_func as vf
import os, copy, time
import yaya_io

# get neural network potential energy of atoms. file lammps is needed which contains 
#nnp-data(contains input.nn, scaling.data, weights.*.data) lammps in file and run.bash to excute lammps file.
#through this steps we obtain energy.out, writing etotal natoms etotal/natoms

#run lammps output energy, forces file.
def eval_nnp(atoms):
    try:
        os.chdir('lammps')
    except:                        
        print('!!!!!!!!!!!!!!!!!!!no lammps!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')                                     
        os._exit(0) 
    yaya_io.write_lammps_data(atoms)
# mpirun my_lmp 
    os.system('./run.bash')                                                                              
    os.chdir('../')
    return 0


# get energy from energy.out                      le[0] etotal le[1] count(all) le[2] e per atom
def read_energy(i):
    os.chdir('lammps')
    with open('energy.out','r') as e:
        lines = e.readlines()
        for l in lines:
            if l[0] != '#':
                le = l.split()
                energy = float(le[i])
    os.chdir('../')
    return energy


# read forces    forces[0][0] is fx of 0th atom
def read_forces():
    os.chdir('lammps')
    f = open('forces.out','r')
    lines = f.readlines()
    forces = []
    i = 0
    for line in lines:
        i = i+1
        if (i >= 10):
            l = line.split()
            force = [float(l[1]),float(l[2]),float(l[3])]
            forces.append(force)
    f.close()
    os.chdir('../')
    return forces

