#!/usr/bin/env bash

export MODULEPATH=$MODULEPATH:/users/modellers/pica/Software/modules/
module load ipd

python plot_transect_Ideal.py
python plot_output.py

