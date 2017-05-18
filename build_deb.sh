#!/bin/bash
python setup.py --command-packages=stdeb.command bdist_deb
CWD=$(pwd)
cd deb_dist/pymetawear-*
CWD2=$(pwd)
cd debian/python-kinemic-pymetawear/usr/lib/python2.7/dist-packages/pymetawear
mv libmetawear.*.so libmetawear.so
cd $CWD2
dh_builddeb -O--buildsystem=pybuild
cd $CWD



