from myvasp import vasp_EPI_dp_shell as epi_dp                                                                        
from yaya_metal.yaya_re import yaya_io
import numpy as np
import os, re

# require file perfect_lattice

def sro_perfect_lattice(file_set):
  sro_per_cfg = []
  for f in file_set:
      atoms = yaya_io.read_lammps_data(f)
      atoms.pos_a0 = 3.81   # myvasp need
      try:
          epi_dp.calc_pairs_per_shell(atoms)
      except:
          sro_per_cfg.append(911)
          break;
      sro_list = np.loadtxt('y_post_WC_SRO_shell.txt')
  #    normal = np.array([12,6,24,12])    # pair per shell
  #    normal = normal/normal.sum()
  #    sro = (normal*sro_list).sum()
      sro_per_cfg.append(sro_list)
  sro_per_cfg = np.array(sro_per_cfg)
  return sro_per_cfg

def sro_relaxed_lattice(file_set):
  sro_per_cfg = []
  for f in file_set:
      atoms = yaya_io.read_lammps_data(f)
  # perfect lattice
      os.chdir('perfect_lattice')
      yaya_io.write_lammps_data(atoms)
      os.system('./run.bash')
      atoms = yaya_io.read_lammps_dump('perfect')
      os.chdir('../')
      atoms.pos_a0 = 3.81   # myvasp need
      try:
          epi_dp.calc_pairs_per_shell(atoms)
      except:
          sro_per_cfg.append(911)
          break;
      sro_list = np.loadtxt('y_post_WC_SRO_shell.txt')
  #    normal = np.array([12,6,24,12])    # pair per shell
  #    normal = normal/normal.sum()
  #    sro = (normal*sro_list).sum()
      sro_per_cfg.append(sro_list)
  sro_per_cfg = np.array(sro_per_cfg)
  return sro_per_cfg
