this is lammps support file

lammps:  
          1,yaya_metal.yaya_nnp.basic_cal        read_energy:energy read_forces:forces
          2,yaya_metal.yaya_nnp.simu        mc:energy
          
minimize:
          1,yaya_metal.yaya_nnp.simu        minimize
