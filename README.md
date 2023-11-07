# Train [YOLOv8](https://github.com/ultralytics/ultralytics) on [NuImages Dataset](https://www.nuscenes.org/nuimages)

NuImages is a 93,000-image dataset for self-driving that provides segmentation and 2D bounding boxes.

We will use the 2D bounding box annotations to train YOLOv8's detection model. We will not use the segmentation data.

This guide was created on PopOS 22.04 with NVIDIA RTX2070S GPU. It is expected to work identically with Ubuntu and other Linux distros.

## Download NuImages

1. Go to https://www.nuscenes.org/nuimages and request download access by creating an account.
2. Once logged in, navigate to https://www.nuscenes.org/nuimages#download
3. Download two files: All->Metadata (0.59GB) and All->Samples (15.27GB). No need to download All->Sweeps.

## Install NuScenes Devkit

1. Go to https://github.com/nutonomy/nuscenes-devkit
2. Clone the repository to download the tutorial jupyter notebook: `git clone git@github.com:nutonomy/nuscenes-devkit.git`
3. Download the python package: `pip3 install nuscenes-devkit`
4. Follow the 'nuImages' section of the README for a [tutorial](https://github.com/nutonomy/nuscenes-devkit#nuimages)

## Install YOLOv8

The [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) library provides all of the functionality we need as a command line tool, without touching any real code.

```
pip3 install ultralytics
```

## Creating a new dataset format 

Ultralytics has some documentation on [how to create a custom dataset](https://docs.ultralytics.com/datasets/#contribute-new-datasets)

The main work involves converting the dataset organization / annotation formats to [Ultralytics YOLO TXT format](https://docs.ultralytics.com/datasets/detect/)

nuImages has much richer, complex annotations for each image than YOLO's simplistic 2d bounding boxes. Therefore converting from nuImages to YOLO format will be lossy. For example, nuImages gives each object a 'category' and an 'attribte', where attribute describes a temporary state. For the `human.pedestrian.adult` category, one of the following attributes are also included: `pedestrian.standing`, `pedestrian.moving`, `pedestrian.sitting_lying`.
