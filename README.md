# Train [YOLOv8](https://github.com/ultralytics/ultralytics) on [NuImages Dataset](https://www.nuscenes.org/nuimages)

NuImages is a 93,000-image dataset for self-driving that provides segmentation and 2D bounding boxes.

We will use the 2D bounding box annotations to train YOLOv8's detection model. We will not use the segmentation data.

## Download NuImages

1. Go to https://www.nuscenes.org/nuimages and request download access by creating an account.
2. Once logged in, navigate to https://www.nuscenes.org/nuimages#download
3. Download 2 files: All->Metadata (0.59GB) and All->Samples (15.27GB). No need to download All->Sweeps.

