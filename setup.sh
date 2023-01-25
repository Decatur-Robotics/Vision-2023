

#!/bin/bash
cd ~
cd pult
sudo ln -s source /home/ubuntu/anaconda3/etc/profile.d/conda.sh
conda activate pult
export FLASK_APP=hello.py
conda activate pult

conda create -n 2023-Vision python=3.10
conda activate 2023-Vision
pip install opencv-python
pip install pupil-apriltags
pip install keyboard