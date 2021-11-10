#!/usr/bin/env bash

module load intel intel-mpi netcdf-intelmpi hdf5-intelmpi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

CODE_DIR=$SCRIPT_DIR/code
INSTALL_DIR=$SCRIPT_DIR/model

mkdir $CODE_DIR
mkdir $INSTALL_DIR

./build-fabm.sh -s $SCRIPT_DIR

./build-xios.sh -s $SCRIPT_DIR

./build-nemo.sh -s $SCRIPT_DIR

