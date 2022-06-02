#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --mem-per-cpu=12G

module load compiler/intel/2018.5.274
module load python/3.6
export BIN_SIZE=102400

source $HOME/.ipmpi
export PROFILE_DIR=./
export I_MPI_STATS=ipm
export I_MPI_STATS_FILE=prof.dat

lscpu
export I_MPI_DEBUG=4
export I_MPI_PIN=1

commpath="../comm_ipmpi_hpcg_256_256_256.mat"
nodes=16

perm=$(../gps ${nodes} ${commpath})
echo $perm
export I_MPI_PIN_PROCESSOR_LIST=$perm

filename=Nodelist-${SLURM_JOB_NAME}.txt
echo "${SLURM_JOB_NODELIST}" | tee -a $filename

start_time=$(date +%s)
mpiexec.hydra -np 16 /scratch/gagandeep20/benchmarks/hpcg/bin/xhpcg 256 256 256 > mpiop_metis
end_time=$(date +%s)
elapsed=$(( end_time - start_time ))
comm_time=`python $HOME/getCommTime.py $(pwd)/prof.dat`
echo ipmpi run completed in $elapsed seconds with communication time percentage ${comm_time}
sleep 2s

#generate ipmpi files
GEN_PROFILE_DIR=$(pwd)
python3 $HOME/commscripts/getIPMPIMat.py $GEN_PROFILE_DIR comm_ipmpi_hpcg1s.mat 16
python3 $HOME/commscripts/getCountMatrix.py $GEN_PROFILE_DIR count_ipmpi_hpcg1s 16