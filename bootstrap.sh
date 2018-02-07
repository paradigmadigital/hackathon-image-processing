#!/bin/bash

echo "Updating package repositories.."
apt-get update

echo "Install opencv..."
apt-get -y install build-essential cmake pkg-config git
apt-get -y install libffi-dev libffi6
apt-get -y install libjpeg-dev libpng-dev
apt-get -y install libsm6 libxrender1 libfontconfig1
apt-get -y install python-dev python-tk python-setuptools python-virtualenv

# echo "Installing python3.6.."
# add-apt-repository ppa:jonathonf/python-3.6
# apt-get update
# apt-get -y install python3.6