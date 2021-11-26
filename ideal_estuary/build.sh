#!/usr/bin/env bash

module load intel-mpi/5.1.2 netcdf-intelmpi/default intel/intel-2016 hdf5-intelmpi/default

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CODE_DIR=$SCRIPT_DIR/code
INSTALL_DIR=$SCRIPT_DIR/model

num_cpu=$(nproc)

website=("git@github.com:UK-FVCOM-Usergroup/uk-fvcom.git" "git@github.com:pmlmodelling/ersem.git" "git@github.com:fabm-model/fabm.git")
name=("uk-fvcom" "ersem" "fabm")
branch=("FVCOM-FABM" "master" "master")

mkdir $CODE_DIR
cd $CODE_DIR

echo "Obtaining source code"
for i in 0 1 2
do
    git clone ${website[i]} ${name[i]}
    cd ${name[i]}
    git checkout ${branch[i]}
    cd $CODE_DIR
done

cd $SCRIPT_DIR

FABM=$CODE_DIR/fabm/src
ERSEM=$CODE_DIR/ersem
FABM_INSTALL=$INSTALL_DIR/FABM-ERSEM
FC=$(which mpiifort)

mkdir -p $FABM_INSTALL

cd $FABM
mkdir build
cd build
# Production config:
cmake $FABM -DFABM_HOST=fvcom -DFABM_ERSEM_BASE=$ERSEM -DCMAKE_Fortran_COMPILER=$FC -DCMAKE_INSTALL_PREFIX=$FABM_INSTALL
make install -j $num_cpu

cd $SCRIPT_DIR

sed -i 's|BASE_SETUP_DIR|'"$SCRIPT_DIR"'|g' make_ideal_estuary.inc
ln -s $SCRIPT_DIR/make_ideal_estuary.inc $SCRIPT_DIR/code/uk-fvcom/FVCOM_source/make.inc

# Installing FVCOM additional packages (METIS, Proj, etc)
cd $SCRIPT_DIR/code/uk-fvcom/FVCOM_source/libs
mv makefile makefile_
ln -s makefile.CETO makefile
make -j $num_cpu

# Building FVCOM
cd ..
make -j $num_cpu
