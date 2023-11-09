import logging
from pathlib import Path
from nuimages import NuImages
from tqdm import tqdm
import numpy as np
from argparse import ArgumentParser

from utils import PxyXY_to_Nxcycwh
from classes import simplify_nuimage_labels, NuImageSimpleCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def mkdir_output_dirs(p: Path):
    logger.info(f"Creating output directories at: {p}...")
    p.mkdir(parents=True, exist_ok=True)

    (p / 'train').mkdir(parents=True, exist_ok=True)
    (p / 'train' / 'images').mkdir(parents=True, exist_ok=True)
    (p / 'train' / 'labels').mkdir(parents=True, exist_ok=True)

    (p / 'val').mkdir(parents=True, exist_ok=True)
    (p / 'val' / 'images').mkdir(parents=True, exist_ok=True)
    (p / 'val' / 'labels').mkdir(parents=True, exist_ok=True)

def move_sample(sample, set_type: str, nuim: NuImages, nuim_root: Path, output_root: Path):
    sample_data_token = sample['key_camera_token']
    sample_data = nuim.get("sample_data", sample_data_token)

    origin_jpg_path = Path(nuim_root) / sample_data['filename']
    try:
        assert origin_jpg_path.exists() & origin_jpg_path.is_file()
    except:
        logger.error(f"No image file found at {origin_jpg_path}.\nTip: Maybe this is your second time running this script and the files have already been moved? Re-extract the nuImages tar files and try again.")
        exit(1)

    destination_jpg_dir = Path(output_root) / set_type / 'images'
    assert (destination_jpg_dir.exists() & destination_jpg_dir.is_dir()), f"No destination directory found at {destination_jpg_dir}"

    if (origin_jpg_path.exists() & destination_jpg_dir.exists()):
        origin_jpg_path.rename(destination_jpg_dir / origin_jpg_path.name )

def move_set(set_type: str, nuim_root: Path, output_root: Path):
    nuim = NuImages(dataroot=nuim_root.resolve(), version=f"v1.0-{set_type}", verbose=False, lazy=True)
    for sample in tqdm(nuim.sample):
        move_sample(sample, set_type, nuim, nuim_root, output_root)

def get_filename_no_suffix(annotation, nuim):
    '''
    Given a NuImages.ann annotation, return the filename without suffix
    '''
    sample_data_token = annotation['sample_data_token']
    sample_data = nuim.get("sample_data", sample_data_token)
    return Path(sample_data['filename']).with_suffix('').name

def convert_annotation(annotation, nuim):
    xyXY = annotation['bbox']

    # odd dataset bug where there is no mask
    if annotation['mask'] is None:
        return None, None, None
    height = annotation['mask']['size'][0]
    width = annotation['mask']['size'][1]
    yolo_bbox = list(PxyXY_to_Nxcycwh(xyXY, width, height))

    nu_cat = nuim.get('category', annotation['category_token'])['name']

    if annotation['attribute_tokens']:
        attribute_token = annotation['attribute_tokens'][0]
        attribute = nuim.get('attribute', attribute_token)['name']
    else:
        attribute = None
    
    yolo_cat = simplify_nuimage_labels(nu_cat, attribute)

    filename_no_suffix = get_filename_no_suffix(annotation, nuim)

    return yolo_cat, yolo_bbox, filename_no_suffix

def append_txt(cat: str, bbox: list, filename_no_suffix: str, set_type: str, output_root: Path):
    pa = output_root / set_type / 'labels' 
    fi = (pa / filename_no_suffix).with_suffix('.txt')

    cat_index = NuImageSimpleCategory[cat].value

    xc, yc, w, h = bbox

    with open(fi, 'a') as f:
        f.write(f"{cat_index} {xc} {yc} {w} {h}\n")

def convert_set_ann(set_type, nuim_root: Path, output_root: Path):
    nuim = NuImages(dataroot=nuim_root.resolve(), version=f"v1.0-{set_type}", verbose=False, lazy=True)

    for annotation in tqdm(nuim.object_ann):
        cat, bbox, filename_no_suffix = convert_annotation(annotation, nuim)
        if cat is None:
            continue
        append_txt(cat, bbox, filename_no_suffix, set_type, output_root)

if __name__ == "__main__":
    argparse = ArgumentParser()
    argparse.add_argument("--nuim-root", required=True, help="Root directory of nuImages dataset where the directories 'samples', 'v1.0-train', 'v1.0-val'... are located.")
    argparse.add_argument('--output-root', required=True, help='Output directory where the converted YOLO TXT dataset will be stored.')
    argparse.add_argument('--only-images', action='store_true', help='Only move images, do not convert annotations.')
    argparse.add_argument('--only-annotations', action='store_true', help='Only convert annotations, do not move images.')

    args = argparse.parse_args()

    try:
        assert (Path(args.nuim_root).exists() & Path(args.nuim_root).is_dir()), "nuImages root directory does not exist or is not a directory."

        assert (Path(args.nuim_root) / 'samples').exists(), "nuImages samples directory does not exist."

        assert (Path(args.nuim_root) / 'v1.0-train').exists(), "nuImages train directory does not exist."

        assert (Path(args.nuim_root) / 'v1.0-val').exists(), "nuImages val directory does not exist."
    except AssertionError:
        message = '''nuImages root directory does not exist or does not contain required directories. Download nuImages dataset from https://www.nuscenes.org/nuimages#download , untar them with `tar -xvf _.tgz` and organize them thusly:

NUIM_ROOT
├── nuimages-v1.0-all-metadata.tgz
├── nuimages-v1.0-all-samples.tgz
├── samples
├── v1.0-mini
├── v1.0-test
├── v1.0-train
└── v1.0-val
'''
        logger.error(message)
        exit(1)

    if Path(args.output_root).exists():
        logger.warning("Output directory already exists. Files may be overwritten or appended.")
    
    Path(args.output_root).mkdir(parents=True, exist_ok=True)

    mkdir_output_dirs(Path(args.output_root))

    if args.only_images:
        logger.info("Only moving images.")
        for set_type in ["train", "val"]:
            move_set(set_type, Path(args.nuim_root), Path(args.output_root))
        
        logger.info(f"Done! Results in output directory: {Path(args.output_root)}")
        exit(0)

    if args.only_annotations:
        logger.info("Only converting and writing annotations.")
        for set_type in ["train", "val"]:
            convert_set_ann(set_type, Path(args.nuim_root), Path(args.output_root))
        logger.info(f"Done! Results in output directory: {Path(args.output_root)}")
        exit(0)

    for set_type in ["train", "val"]:
        logger.info(f"Moving {set_type} images...")
        move_set(set_type, Path(args.nuim_root), Path(args.output_root))
    
    for set_type in ["train", "val"]:
        logger.info(f"Converting and writing {set_type} annotations...")
        convert_set_ann(set_type, Path(args.nuim_root), Path(args.output_root))
    
    logger.info(f"Done! Results in output directory: {Path(args.output_root)}")