#!/bin/bash
                                                                                                                      

mpirun -np 1 yaya_lmp -in run.in >/dev/null 2>&1
wait
#0 >/dev/null 2>&1 
