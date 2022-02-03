```
conda create -n dex "python=3.9"
conda activate dex
conda install -y pytorch torchvision cudatoolkit=11.3 -c pytorch
pip install -r requirements.txt
```

For earlier versions of CUDA:
```
conda install -y "cudatoolkit<11.2" -c conda-forge
conda install -y pytorch torchvision -c pytorch
```

This currently will not work (3.10 support is expected to be released in 1.11, maybe within a month)

```
conda create -n dex "python=3.10"
conda activate dex
conda install -y pytorch torchvision cudatoolkit=11.3 -c pytorch
pip install -r requirements.txt
```

