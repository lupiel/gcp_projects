VENV_NAME=venv-ocr

# install miniconda
```
sudo apt-get update
sudo apt-get install bzip2 libxml2-dev
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh
source .bashrc
```
# Create virtual environment
```
conda create --no-default-packages --name=$VENV_NAME python=3.8
conda activate $VENV_NAME
```
# Installing packages
```
python -m pip install --upgrade pip
pip install pip install git+https://github.com/JaidedAI/EasyOCR.git

#or e.g.# 
#git clone https://github.com/JaidedAI/EasyOCR.git
#pip install -e ".[devel]"
```
# Enabling virtual environment in jupyter notebook
```
conda install ipykernel
conda deactivate
conda activate $VENV_NAME
ipython kernel install --user --name=$VENV_NAME
#jupyter kernelspec uninstall $VENV_NAME
```
# teardown
```
conda env remove --name $VENV_NAME
```
