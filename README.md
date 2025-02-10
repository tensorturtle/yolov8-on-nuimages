# Train [YOLOv8](https://github.com/ultralytics/ultralytics) on [NuImages Dataset](https://www.nuscenes.org/nuimages)

[![Run Unit Test via Pytest](https://github.com/tensorturtle/yolov8-on-nuimages/actions/workflows/run_unit_tests.yml/badge.svg)](https://github.com/tensorturtle/yolov8-on-nuimages/actions/workflows/run_unit_tests.yml)

NuImages is a 93,000-image dataset for self-driving that provides segmentation and 2D bounding boxes.

We will use the 2D bounding box annotations to train YOLOv8's detection model. We will not use the segmentation data.

This guide was created on PopOS 22.04 with NVIDIA RTX2070S GPU. It is expected to work identically with Ubuntu and other Linux distros.

## Clone this repository

```
git clone git@github.com:tensorturtle/yolov8-on-nuimages.git

cd yolov8-on-nuimages
```

## Download NuImages

1. Go to https://www.nuscenes.org/nuimages and request download access by creating an account.
2. Once logged in, navigate to https://www.nuscenes.org/nuimages#download
3. Download two files: All->Metadata (0.59GB) and All->Samples (15.27GB). No need to download All->Sweeps.

The two downloaded files:
```
~/Downloads
├── nuimages-v1.0-all-metadata.tgz
└── nuimages-v1.0-all-samples.tgz
```

Unpack them:
```
tar -xvf nuimages-v1.0-all-metadata.tgz
tar -xvf nuimages-v1.0-all-samples.tgz
```

We now have 5 new directories. Move them to a convenient location. We'll call that directory `NUIM_ROOT`
```
NUIM_ROOT
├── samples
├── v1.0-mini
├── v1.0-test
├── v1.0-train
└── v1.0-val
```

## Install Python packages

```
pip3 install -r requirements.txt
```

## Run script

Two arguments are required:
+ `--nuim-root`: The directory where nuimages metadata and samples directories are located. Path to `NUIM_ROOT` above

```
python3 convert.py --nuim-root=/abs/path/to/NUIM_ROOT
```

Live progress bars will be shown. The total runtime is less than 1 minute

NOTE: This script 'mv's the files to their new directories. If something went wrong and you need to run it again, you need to start from the `tar -xvf` part to restore the files in the nuim root.

Typical output:
```
$ python3 convert.py --nuim-root=/home/tensorturtle/DatasetsPublic/nuimages-full
INFO:root:Creating output directories at: nuImagesYoloDataset...
INFO:root:Moving train images...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 67279/67279 [00:04<00:00, 14277.85it/s]
INFO:root:Moving val images...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 16445/16445 [00:01<00:00, 14548.88it/s]
INFO:root:Moving test images...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 9752/9752 [00:00<00:00, 14908.98it/s]
INFO:root:Converting and writing train annotations...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 557715/557715 [00:21<00:00, 25911.76it/s]
INFO:root:Converting and writing val annotations...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 136074/136074 [00:04<00:00, 28257.51it/s]
INFO:root:Done! Results in output directory: nuImagesYoloDataset
```

The `nuImagesYoloDataset` directory contains everything you need to train YOLOv8 as a YOLO TXT dataset format.

## Add fine-tuning dataset

At this point, add additional datasets using the same categories and format into the `train/images` and `train/labels` directories.

## Train YOLOv8

Install Python library / CLI tool for YOLOv8:
```
pip3 install ultralytics
```

As an example, we'll train a YOLOv8n model on our newly created dataset:
```
yolo detect train data=nuImagesYoloDataset/nuimages.yaml model=yolov8n.pt epochs=100 imgsz=640
```

# Development Help & Implementation Details

## Install NuScenes Devkit

`convert.py` uses `from nuimages import NuImages` package to read annotation data.

A tutorial for that package is available at: https://github.com/nutonomy/nuscenes-devkit

1. Clone the repository to download the tutorial jupyter notebook: `git clone git@github.com:nutonomy/nuscenes-devkit.git`
2. Download the python package: `pip3 install nuscenes-devkit`
3. Follow the 'nuImages' section of the README for a [tutorial](https://github.com/nutonomy/nuscenes-devkit#nuimages)

## Creating a new dataset format 

Ultralytics has some documentation on [how to create a custom dataset](https://docs.ultralytics.com/datasets/#contribute-new-datasets)

The main work involves converting the dataset organization / annotation formats to [Ultralytics YOLO TXT format](https://docs.ultralytics.com/datasets/detect/)

### Considerations When Converting Annotations

Generally, nuImages has much richer, complex annotations for each image than YOLO's simplistic 2d bounding boxes. Therefore converting from nuImages to YOLO format will be lossy

nuImages contains `object` and `surface` annotations. We use `object` only. The `surface` annotations refers to segmentations of the road

nuImages gives each object a 'category' and an 'attribte', where attribute describes a temporary state. As an example, for the `human.pedestrian.adult` category, one of the following attributes are also included: `pedestrian.standing`, `pedestrian.moving`, `pedestrian.sitting_lying`.

The following table describes the lossy assignment of nuImages objects categories & attributes to YOLO categories. Note that the choices made here are focused toward ADAS development and may not be optimal for general purpose uses.

nuImages Category(s) | nuImages Attribute(s) | YOLO Category 
--- | --- | ---
`animal` | all | none
`human.pedestrian.adult` | all except `pedestrian.sitting_lying` | `pedestrian`
`human.pedestrian.adult` | `pedestrian.sitting_lying` | none; Not a moving concern
`human.pedestrian.child` | all except `pedestrian.sitting_lying` | `pedestrian`
`human.pedestrian.child` | `pedestrian.sitting_lying` | none; Not a moving concern
`human.pedestrian.construction_worker` | any | `pedestrian`
`human.pedestrian.personal_mobility` | any | `uprightmobility`
`human.pedestrian.police_officer` | any | `pedestrian`
`human.pedestrian.stroller` | any | `stroller`
`human.pedestrian.wheelchair` | any | `wheelchair`
`movable_object.barrier` | any | none; Too broad
`movable_object.pushable_pullable` | any | none; Too broad
`movable_object.debris` | any | none; Too broad
`movable_object.trafficcone` | any | `trafficcone`
`static_object.bicycle_rack` | any | none; Too broad
`vehicle.bicycle` | `cycle.with_rider` | `cyclist`
`vehicle.bicycle` | `cycle.without_rider` | `bicycle`
`vehicle.bus.bendy` | any | `bus`; Each section is labeled as a separate bus
`vehicle.bus.rigid` | any | `bus`
`vehicle.car` | any | `car`
`vehicle.construction` | any | none; Too broad and generally stationary
`vehicle.ego` | any | none; Purposefully ignore
`vehicle.emergency.ambulance` | any | `ambulance`
`vehicle.emergency.police` | any | none; Too broad (all types of police vehicles)
`vehicle.motorcycle` | `cycle.with_rider` | `motorcyclist`
`vehicle.motorcycle` | `cycle.without_rider` | `motorcycle`
`vehicle.trailer` | any | none; Too broad (for trucks, cars, bikes)
`vehicle.truck` | any | `truck`

# Future Features

+ [ ] Segmentation

# Training on a different machine

Copy over

+ `nuImagesYoloDataset.tar` - run `tar -cvf nuImagesYoloDataset` on the directory that was created in the convert step.
+ `train.sh`

Install `pip3 install ultralytics`

Potentially required stuff that might be necessary:
```
apt-get update
apt-get install -y libgl1
pip3 install -U numpy # on multi-GPU systems
```

Run `train.sh`

# Later Updates

This section was created 1 year after most of the above was created. 
Upon reviewing the dataset use in practice, it was determined that the categories can be simplified further.

The `--label-mapping` allows you to specify either FAITHFUL, SIMPLER (4 categories), and SIMPLEST (2 categories).

To use this binary category system:
```
python3 convert.py --nuim-root=/abs/path/to/NUIM_ROOT --label-mapping SIMPLER
```


