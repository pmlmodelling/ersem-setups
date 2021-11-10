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
git clone git@gitlab.ecosystem-modelling.pml.ac.uk:nemo-fabm/XIOS1.git

cd $CODE_DIR/XIOS1

./make_xios --arch ifort_CETO --prod --full --netcdf_lib netcdf4_par

rsync -a $CODE_DIR/XIOS1/bin $CODE_DIR/XIOS1/inc $CODE_DIR/XIOS1/lib $INSTALL_DIR/xios-intel

