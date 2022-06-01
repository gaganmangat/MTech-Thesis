#!/bin/bash

cd hpcg-1s
sbatch -N 1 --job-name=hpcg_1s --output=hpcg_1s.out --error=hpcg_1s.out --ntasks-per-node=16 --exclusive /scratch/gagandeep20/socket-testing/hpcg-1s/hpcg_1s.sh
cd ..

cd hpcg-2s
sbatch -N 1 --job-name=hpcg_2s --output=hpcg_2s.out --error=hpcg_2s.out --ntasks-per-node=16 --exclusive /scratch/gagandeep20/socket-testing/hpcg-2s/hpcg_2s.sh
cd ..

cd hpcg-rs
sbatch -N 1 --job-name=hpcg_rs --output=hpcg_rs.out --error=hpcg_rs.out --ntasks-per-node=16 --exclusive /scratch/gagandeep20/socket-testing/hpcg-rs/hpcg_rs.sh
cd ..