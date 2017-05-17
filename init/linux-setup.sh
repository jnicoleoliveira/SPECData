#!/usr/bin/env bash

echo "Installing Conda Environment..."
conda env create -n specdata-env -f bin/conda_environment_linux.yml

echo "Open Environment.."
source activate specdata-env

cd ..
python run_wizard.py

