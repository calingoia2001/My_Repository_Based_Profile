#!/bin/bash

apt-get update
apt install vim -y
tar -xvzf pjproject-2.14.1.tar.gz
cd pjproject-2.14.1/
./configure CFLAGS="-fPIC"
make dep
make
apt-get install swig -y
apt-get install python3-dev -y
cd pjsip-apps/src/swig/python
make
make install
