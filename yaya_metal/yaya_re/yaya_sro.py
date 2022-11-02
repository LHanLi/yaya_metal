from myvasp import vasp_EPI_dp_shell as epi_dp          
from ovito.io import import_file
from ovito.modifiers import CoordinationAnalysisModifier
from yaya_metal.yaya_re import yaya_io
import numpy as np
import os, re

# scale rdf to eta
def calc_cc_scale(cn):
    # scaling factors, e.g., c1c1, 2c1c2, c2c2
    cn2 = cn[np.newaxis, :].copy()
    cn2prod = cn2.T @ cn2

    nelem = cn.shape[0]
    cc_scale = np.array([])

    for i in np.arange(nelem):
        for j in np.arange(i, nelem):
            temp = cn2prod[i, j]
            if i != j :
                temp = temp*2
            cc_scale = np.append(cc_scale, temp)

    return cc_scale

#a = 3.81
#V0 = a**3/4
# order i.e. order first as 'H-H'  then ('He-He','He-H','H-H') reverse
def calc_eta(atoms,cutoff_radius,n_of_bins,order):
# get rdf
    from ovito.pipeline import StaticSource, Pipeline
    from ovito.io.ase import ase_to_ovito
    data = ase_to_ovito(atoms)
    pipeline = Pipeline(source = StaticSource(data = data))
    pipeline.modifiers.append(CoordinationAnalysisModifier(cutoff=cutoff_radius, number_of_bins=n_of_bins, partial=True))
    rdf_table = pipeline.compute().tables['coordination-rdf']
    data_rdf = rdf_table.xy()
    rdf_names = rdf_table.y.component_names
# V0
    V0 = atoms.get_volume()/len(atoms.numbers)
# cc_scale
    cc_scale = calc_cc_scale(atoms.cn)
    
# get eta
    data = data_rdf.copy()
    r = data[:,0].copy()
    dr = r[1] - r[0]
    n = data[:, 1:].copy()   # number of neighbours for each pair

    dv = 1/V0*4/3*np.pi * ((r+dr/2)**3 - (r-dr/2)**3)
    n = (n.T * dv).T

    eta = n * cc_scale

# short eta(delte 0 row)
    eta = eta[eta.sum(axis=1)!=0,:]

# check order
    if(rdf_names[0] != order):
        eta = np.array([i[::-1] for i in eta])

    return eta

def sro_from_eta(atoms,eta):
    sro = np.array([1 - i[1]/2/(atoms.cn[0]*atoms.cn[1]*(i[0]+i[1]+i[2])) for i in eta])
    return sro
    

    
    

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
