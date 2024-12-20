# Spatio-temporal Diffusion Point Processes

![OverallFramework](./assets/framework.png "Our proposed framework")

This project was initially described in the full research track paper *[Spatio-temporal Diffusion Point Processes](https://dl.acm.org/doi/10.1145/3580305.3599511)* at KDD 2023 in Long Beach, CA. Contributors to this project are from the *[Future Intelligence laB (FIB)](https://fi.ee.tsinghua.edu.cn/)* at *[Tsinghua University](https://www.tsinghua.edu.cn/en/)*.

The code is tested under a Linux desktop with torch 1.7 and Python 3.7.10.

## Installation

### Environment
- Tested OS: Linux
- Python >= 3.7
- PyTorch == 1.7.1
- Tensorboard

### Dependencies
1. Install PyTorch 1.7.1 with the correct CUDA version. Recommend CUDA 11.7.
2. Use the ``pip install -r requirements. txt`` command to install all of the Python modules and packages used in this project.

## Model Training

Use the following command to train DSTPP on `AnimalTracking` dataset: 

``
python app.py --dataset AnimalTracking --mode train --timesteps 200 --samplingsteps 200 --batch_size 64 --total_epochs 200
``

To train DSTPP on other datasets:

``
python app.py --dataset Storms --mode train --timesteps 200 --samplingsteps 200 --batch_size 64 --total_epochs 200
``

``
python app.py --dataset Atlantic --mode train --timesteps 200 --samplingsteps 200 --batch_size 64 --total_epochs 200
``

The trained models are saved in ``ModelSave/``.

The logs are saved in ``logs/``.

Use tensorboard to view visualized result.

``
tensorboard --logdir=logs
``

## Data Source

**Atlantic**：https://www.kaggle.com/datasets/utkarshx27/noaa-atlantic-hurricane-database  


**Storms**：https://www.kaggle.com/datasets/noaa/hurricane-database  


**AnimalTracking**：https://www.kaggle.com/datasets/pulkit8595/movebank-animal-tracking  


## Note

The implemention is based on *[DDPM](https://github.com/lucidrains/denoising-diffusion-pytorch)*.

If you found this library useful in your research, please consider citing:

```
@inproceedings{yuan2023DSTPP,
  author = {Yuan, Yuan and Ding, Jingtao and Shao, Chenyang and Jin, Depeng and Li, Yong},
  title = {Spatio-Temporal Diffusion Point Processes},
  year = {2023},
  booktitle = {Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining},
  pages = {3173–3184},
}
```
