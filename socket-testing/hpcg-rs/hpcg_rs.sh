#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --mem-per-cpu=8G

module load compiler/intel/2018.5.274
module load python/3.6

source $HOME/.ipmpi
export PROFILE_DIR=./
export I_MPI_STATS=ipm
export I_MPI_STATS_FILE=prof.dat

lscpu
export I_MPI_DEBUG=4
export I_MPI_PIN=1
export I_MPI_PIN_PROCESSOR_LIST=27,5,29,11,25,26,0,9,17,22,44,39,3,20,7,34

filename=Nodelist-${SLURM_JOB_NAME}.txt
echo "${SLURM_JOB_NODELIST}" | tee -a $filename

start_time=$(date +%s)
mpiexec.hydra -np 16 /scratch/gagandeep20/benchmarks/hpcg/bin/xhpcg 176 160 176 > mpiop_rs
end_time=$(date +%s)
elapsed=$(( end_time - start_time ))
comm_time=`python $HOME/getCommTime.py $(pwd)/prof.dat`
echo ipmpi run completed in $elapsed seconds with communication time percentage ${comm_time}
sleep 2s

#generate ipmpi files
GEN_PROFILE_DIR=$(pwd)
python3 $HOME/commscripts/getIPMPIMat.py $GEN_PROFILE_DIR comm_ipmpi_hpcgrs.mat 16
python3 $HOME/commscripts/getCountMatrix.py $GEN_PROFILE_DIR count_ipmpi_hpcgrs 16