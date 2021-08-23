#!/bin/bash


mpirun -np 8 my_lmp -in run.in >/dev/null 2>&1
wait
#0 >/dev/null 2>&1 
