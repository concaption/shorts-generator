#!/usr/bin/env bash

### Sets up python packages in for devcontainer.json

#create a virtualenv
python -m venv .venv

# append it to bash so every shell launches with it
echo 'source .venv/bin/activate' >> ~/.bashrc

# update apt-get and install ffmpeg
sudo apt-get update
sudo apt-get install ffmpeg -y

# source virtualenv
source .venv/bin/activate

# install all software
make install