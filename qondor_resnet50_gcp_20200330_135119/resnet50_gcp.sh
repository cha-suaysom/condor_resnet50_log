#!/bin/bash
set -e
echo "hostname: $(hostname)"
echo "date:     $(date)"
echo "pwd:      $(pwd)"
echo "Redirecting all output to stderr from here on out"
exec 1>&2

export gccsetup=/cvmfs/sft.cern.ch/lcg/contrib/gcc/7/x86_64-centos7/setup.sh
export rootsetup=/cvmfs/sft.cern.ch/lcg/releases/LCG_95/ROOT/6.16.00/x86_64-centos7-gcc7-opt/ROOT-env.sh
export pipdir=/cvmfs/sft.cern.ch/lcg/releases/pip/19.0.3-06476/x86_64-centos7-gcc7-opt
export SCRAM_ARCH=slc7_amd64_gcc700

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source /cvmfs/cms.cern.ch/cmsset_default.sh
source "${gccsetup}"
source "${rootsetup}"
export PATH="${pipdir}/bin:${PATH}"
export PYTHONPATH="${pipdir}/lib/python2.7/site-packages/:${PYTHONPATH}"

set -uxoE pipefail
echo "Setting up custom pip install dir"
HOME="$(pwd)"
pip(){ ${pipdir}/bin/pip "$@"; }  # To avoid any local pip installations
export pip_install_dir="$(pwd)/install"
mkdir -p "${pip_install_dir}/bin"
mkdir -p "${pip_install_dir}/lib/python2.7/site-packages"
export PATH="${pip_install_dir}/bin:${PATH}"
export PYTHONPATH="${pip_install_dir}/lib/python2.7/site-packages:${PYTHONPATH}"

pip -V
which pip

mkdir qondor
tar xf qondor.tar -C qondor
pip install --install-option="--prefix=${pip_install_dir}" -e qondor/
python resnet50_gcp.py
