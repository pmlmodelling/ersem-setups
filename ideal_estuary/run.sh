#!/usr/bin/env bash

module load intel-mpi/5.1.2 netcdf-intelmpi/default intel/intel-2016 hdf5-intelmpi/default

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CODE_DIR=$SCRIPT_DIR/code
INSTALL_DIR=$SCRIPT_DIR/model

echo $SCRIPT_DIR

echo "\n\n\nBUILDING FVCOM-ERSEM\n\n\n"
./build.sh


echo "\n\n\nSETTING UP ESTUARY DESCRIPTION AND MODEL RUN SCRIPTS\n\n\n"
mkdir -p $SCRIPT_DIR/model/estuary/bin
cp $CODE_DIR/uk-fvcom/FVCOM_source/fvcom $SCRIPT_DIR/model/estuary/bin

echo "\n\n\nRUNNING MODEL\n\n\n"
cd $INSTALL_DIR/estuary
sbatch launch_estuary.slurm
cd $SCRIPT_DIR

