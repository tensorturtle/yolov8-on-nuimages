yolo detect train \
    data=/home/tensorturtle/Repos/yolov8-on-nuimages/nuImagesYoloDataset/nuimages.yaml \
    model=yolov8l.pt \
    epochs=100 \
    imgsz=960\
    val=false \
    batch=4 \
    patience=10 \
    pretrained=True \
    val=False \
    name=train-l-960px-100epochs \
    save=True \
    device=0,1,2,3




