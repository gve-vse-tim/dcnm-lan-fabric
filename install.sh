#!/usr/bin/env bash
#  While this is written as a bash script, it almost certainly
#  won't work correctly if you execute it.  Source this file
#  instead:  source install.sh

conda create -y -n dcnm-lan-sdk python~=3.8.0

conda activate dcnm-lan-sdk && python setup.py install

