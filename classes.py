from enum import Enum, auto

# Single level categories like YOLO
class NuImageSimpleCategory(Enum):
    pedestrian = 0
    cyclist = auto()
    car = auto()
    bus = auto()
    truck = auto()
    ambulance = auto()
    uprightmobility = auto()
    stroller = auto()
    wheelchair = auto()
    bicycle = auto()
    motorcyclist = auto()
    motorcycle = auto()

# Convert nuImages category & attibute to YOLO-like category (above)
attribute_aware_class_mapping = {
    'animal': None,
    'human.pedestrian.adult': {
        'pedestrian.sitting_lying_down': None,
        'pedestrian.moving': 'pedestrian',
        'pedestrian.standing': 'pedestrian',
    },
    'human.pedestrian.child': {
        'pedestrian.sitting_lying_down': None,
        'pedestrian.moving': 'pedestrian',
        'pedestrian.standing': 'pedestrian',
    },
    'human.pedestrian.construction_worker': 'pedestrian',
    'human.pedestrian.personal_mobility': 'uprightmobility',
    'human.pedestrian.police_officer': 'pedestrian',
    'human.pedestrian.stroller': 'stroller',
    'human.pedestrian.wheelchair': 'wheelchair',
    'movable_object.barrier': None,
    'movable_object.pushable_pullable': None,
    'movable_object.debris': None,
    'movable_object.trafficcone': None,
    'static_object.bicycle_rack': None,
    'vehicle.bicycle': {
        'cycle.with_rider': 'cyclist',
        'cycle.without_rider': 'bicycle',
    },
    'vehicle.bus.bendy': 'bus',
    'vehicle.bus.rigid': 'bus',
    'vehicle.car': 'car',
    'vehicle.construction': None,
    'vehicle.ego': None,
    'vehicle.emergency.ambulance': 'ambulance',
    'vehicle.emergency.police': None,
    'vehicle.motorcycle': {
        'cycle.with_rider': 'motorcyclist',
        'cycle.without_rider': 'motorcycle',
    },
    'vehicle.trailer': None,
    'vehicle.truck': 'truck'
}

def simplify_nuimage_labels(category, attribute):
    assert category in attribute_aware_class_mapping, f"Category: {category} not found in mapping"

    mapp = attribute_aware_class_mapping[category]

    if mapp is None:
        # ignore label
        return None
    elif isinstance(mapp, str):
        # 1-to-1 mapping
        return mapp
    elif attribute in mapp:
        return mapp[attribute]
    else:
        # rare dataset bug where categories that should have an attribute simply doesn
        return None
