#!/bin/bash

cd pjproject-2.14.1/pjsip-apps/src
git clone https://github.com/mgwilliams/python3-pjsip.git
cd python3-pjsip/
python3 setup.py build
python3 setup.py install
