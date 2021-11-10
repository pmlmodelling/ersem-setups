#!/usr/bin/env bash

module load intel intel-mpi netcdf-intelmpi hdf5-intelmpi

while getopts ":s:" flag; do
        case "${flag}" in
        s) SCRIPT_DIR=${OPTARG};;
    esac
done

CODE_DIR=$SCRIPT_DIR/code
INSTALL_DIR=$SCRIPT_DIR/model

cd $CODE_DIR

git clone git@gitlab.ecosystem-modelling.pml.ac.uk:nemo-fabm/NEMO-ERSEM-shelf.git

cd $CODE_DIR/NEMO-ERSEM-shelf/NEMOGCM/CONFIG/AMM7_FABM_ERSEM/EXP03

git checkout fabm1

sed -i 's@export XIOS_HOME=$HOME/local/xios-intel@export XIOS_HOME='$INSTALL_DIR'/xios-intel@g' build-nemo.sh
sed -i 's@export FABM_HOME=$HOME/local/fabm/nemo@export FABM_HOME='$INSTALL_DIR'/FABM-ERSEM@g' build-nemo.sh
sed -i 's@echo "Cleaning old build..."@@g' build-nemo.sh
sed -i 's@./makenemo -m $ARCH -n AMM7_BLD_SCRATCH clean_config@@g' build-nemo.sh
sed -i 's@NEMO_BUILD_DIR=$HOME/git/NEMO-shelf/NEMOGCM/CONFIG@NEMO_BUILD_DIR='$CODE_DIR'/NEMO-ERSEM-shelf/NEMOGCM/CONFIG@g' build-nemo.sh
sed -i 's@RUNDIR=~/build/NEMO-shelf@RUNDIR='$INSTALL_DIR'@g' build-nemo.sh

./build-nemo.sh

