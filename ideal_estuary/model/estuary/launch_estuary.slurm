#!/bin/bash --login

#SBATCH --nodes=4
#SBATCH --ntasks-per-node=20
#SBATCH --threads-per-core=1
#SBATCH --job-name=estuary
#SBATCH --partition=all
#SBATCH --time=48:00:00
##SBATCH --mail-type=ALL
##SBATCH --mail-user=your_mail@pml.ac.uk

# Set the number of processes based on the number of nodes we have `select'ed.
np=$SLURM_NTASKS

# Export the libraries to LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$(readlink -f $WORKDIR/install/lib):$LD_LIBRARY_PATH

set -eu
ulimit -s unlimited

# Number of months to skip
skip=0

# d53f5083 = FVCOM v3.2.2, M-Y, HEATING_ON, ceto
binary=bin/fvcom
grid=${grid:-"estuary"}
casename="${grid}"

# Make sure any symbolic links are resolved to absolute path
export WORKDIR=$(readlink -f $(pwd))

# Set the number of threads to 1
#   This prevents any system libraries from automatically
#   using threading.
export OMP_NUM_THREADS=1

# Magic stuff from the Atos scripts.
export I_MPI_PIN_PROCS=0-19
export I_MPI_EXTRA_FILESYSTEM=on
export I_MPI_EXTRA_FILESYSTEM_LIST=gpfs
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so

# Change to the directory from which the job was submitted. This should be the
# project "run" directory as all the paths are assumed relative to that.
cd $WORKDIR

if [ ! -d ./logs/slurm ]; then
    mkdir -p ./logs/slurm
fi
mv *.out logs/slurm || true
if [ -f ./core ]; then
    rm core
fi

if [ ! -d ./output ]; then
    mkdir -p ./output
fi

# Iterate over the months in the year

    # Launch the parallel job
    srun -n $np $binary --casename=$casename --dbg=0 > logs/${casename}-$SLURM_JOBID.log


    # Check if we crashed and if so, exit the script, bypassing the restart
    # file creation.
    if grep -q NaN logs/${casename}-$SLURM_JOBID.log; then
        echo "NaNs in the output. Halting run."
        exit 2
    fi



