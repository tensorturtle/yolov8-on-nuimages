yolo detect train \
    data=/home/tensorturtle/Repos/yolov8-on-nuimages/nuImagesYoloDataset/nuimages.yaml \
    model=runs/detect/train-l-960px-100epochs7/weights/last.pt \
    epochs=100 \
    imgsz=960\
    val=false \
    batch=4 \
    patience=10 \
    pretrained=True \
    val=False \
    name=train-l-960px-100epochs \
    save=True \
    resume=True




