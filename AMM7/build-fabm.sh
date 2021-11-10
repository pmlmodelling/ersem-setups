#!/usr/bin/env bash

module load intel intel-mpi netcdf-intelmpi hdf5-intelmpi

while getopts ":s:" flag; do
    case "${flag}" in
        s) SCRIPT_DIR=${OPTARG};;
    esac
done
CODE_DIR=$SCRIPT_DIR/code
INSTALL_DIR=$SCRIPT_DIR/model

website=("git@github.com:pmlmodelling/ersem.git" "git@github.com:fabm-model/fabm.git")
name=("ersem" "fabm")
branch=("master" "master")

num_cpu=$(nproc)

cd $CODE_DIR

echo "obtaining source code"
for i in 0 1
do
    git clone ${website[i]} ${name[i]}
    cd ${name[i]}
    git checkout ${branch[i]}
    cd $CODE_DIR
done

FABM=$CODE_DIR/fabm/src
ERSEM=$CODE_DIR/ersem
FABM_INSTALL=$INSTALL_DIR/FABM-ERSEM
FC=$(which mpiifort)

mkdir -p $FABM_INSTALL

cd $FABM
mkdir build
cd build
# Production config:
cmake $FABM -DFABM_HOST=nemo -DFABM_ERSEM_BASE=$ERSEM -DCMAKE_Fortran_COMPILER=$FC -DCMAKE_INSTALL_PREFIX=$FABM_INSTALL
make install -j $num_cpu
