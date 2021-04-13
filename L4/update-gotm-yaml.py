import argparse
import subprocess
import sys
import os

if not (sys.version_info.major == 3):
    message = "This script requires python 3 to run, " \
              "you are using python {}".format(sys.version_info.major)
    sys.exit(message)

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gotm', help='Path to GOTM executable.')
args = parser.parse_args()

gotm_exe = args.gotm
url = \
    "https://raw.githubusercontent.com/gotm-model/code/v6.0/scripts/python/update_setup.py"

try:
    import wget
    wget.download(url)
    updater = url.split('/')[-1]
    command = "{} {} gotm.yaml".format(os.environ['_'], updater)
    if gotm_exe:
        command += " --gotm {}".format(gotm_exe)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    os.remove(updater)
except:
    message = "You will need to have `wget` and `pyyaml` installed " \
              "this can be done with `pip` by the following " \
              "command `python -m pip install wget pyyaml`"
    sys.exit(message)
