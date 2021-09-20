# Rumpleteazer

## environment setup

```commandline
conda create -n Rumpleteazer python=3.8.10

conda install cudatoolkit=11.1 -c nvidia
conda install -n Rumpleteazer opencv -c conda-forge

python -m pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

python -m pip install mmcv-full==1.3.12 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.9.0/index.html
python -m pip install mmdet
python -m pip install mmpose
python -m pip install -r mmpose/requirements/optional.txt
```

## git submodule and sparse checkout

```commandline
git init mmdetection
cd mmdetection
git remote add origin git@github.com:open-mmlab/mmdetection.git
git config core.sparsecheckout true
echo "/configs/*" >> .git/info/sparse-checkout
git pull origin master
cd ..

git submodule add ./mmdetection
```