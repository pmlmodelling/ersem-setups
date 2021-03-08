# L4 setup

The setup in this folder was created for gotm v5. Running a later version of gotm you will need to update the `gotm.yaml` file. This can be done by following the description below.

Option 1:
1. Download the `gotm` updater from [here](https://github.com/gotm-model/code/blob/master/scripts/python/update_setup.py)
2. Run `python <path-to-updater> gotm.yaml --gotm <gotm-executable>`, please note you need to run this script with `python` version 3.
3. Re-run gotm in L4 setups folder

Option 2:
1. Run `python update-gotm-yaml.py` in the L4 setups folder. You can add the optional argument `--gotm <gotm-excutable>` which will include all extra comments in the yaml file `python update-gotm-yaml.py --gotm <gotm-excutable>`
