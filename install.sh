#!/bin/bash

# Install necessary building tools
sudo apt-get install build-essential libreadline-dev libffi-dev git
pkg-config gcc-arm-none-eabi libnewlib-arm-none-eabi

# Clone micropython
git clone https://github.com/micropython/micropython.git upython

# Build micropython and making it available from everwhere
cd upython/mpy-cross && make
cd ../ports/unix
make submodules && make
mkdir $HOME/bin
mv micropython $HOME/bin/micropython
sudo echo 'export PATH=$PATH":$HOME/bin"' >> $HOME/.bashrc
cd ../../../
sudo rm -r upython
source $HOME/.bashrc
