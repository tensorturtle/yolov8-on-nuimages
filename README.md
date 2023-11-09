# Train [YOLOv8](https://github.com/ultralytics/ultralytics) on [NuImages Dataset](https://www.nuscenes.org/nuimages)

NuImages is a 93,000-image dataset for self-driving that provides segmentation and 2D bounding boxes.

We will use the 2D bounding box annotations to train YOLOv8's detection model. We will not use the segmentation data.

This guide was created on PopOS 22.04 with NVIDIA RTX2070S GPU. It is expected to work identically with Ubuntu and other Linux distros.

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

We now have 5 new directories. Move them to a convenient location. We'll call that directory `nuimages_root`
```
nuimages_root
├── samples
├── v1.0-mini
├── v1.0-test
├── v1.0-train
└── v1.0-val
```


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


Bounding box [xmin, ymin, xmax, ymax]

### Overall Strategy
x