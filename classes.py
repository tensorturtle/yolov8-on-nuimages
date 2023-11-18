from enum import Enum, auto

# Single level categories like YOLO
class NuImageSimpleCategory(Enum):
    pedestrian = 0 # standing, walking
    non_pedestrian = auto() # sitting, lying down
    cyclist = auto() # person on two-wheeled, pedal-powered (or assisted) vehicle
    car = auto() # family car, SUV under 9 seats
    large_car = auto() # truck, bus, etc.
    scooter = auto() # standing two-wheeled, non-pedal-powered electric vehicle
    bicycle = auto() # the bike only with no person riding it
    motorcyclist = auto() # person on two-wheeled, motor-powered vehicle with no pedals
    motorcycle = auto() # the motorbike only with no person riding it

# Convert nuImages category & attibute to YOLO-like category (above)
attribute_aware_class_mapping = {
    'animal': None,
    'human.pedestrian.adult': {
        'pedestrian.sitting_lying_down': 'non_pedestrian',
        'pedestrian.moving': 'pedestrian',
        'pedestrian.standing': 'pedestrian',
    },
    'human.pedestrian.child': {
        'pedestrian.sitting_lying_down': 'non_pedestrian',
        'pedestrian.moving': 'pedestrian',
        'pedestrian.standing': 'pedestrian',
    },
    'human.pedestrian.construction_worker': 'pedestrian',
    'human.pedestrian.personal_mobility': 'scooter',
    'human.pedestrian.police_officer': 'pedestrian',
    'human.pedestrian.stroller': None,
    'human.pedestrian.wheelchair': 'non_pedestrian',
    'movable_object.barrier': None,
    'movable_object.pushable_pullable': None,
    'movable_object.debris': None,
    'movable_object.trafficcone': None,
    'static_object.bicycle_rack': None,
    'vehicle.bicycle': {
        'cycle.with_rider': 'cyclist',
        'cycle.without_rider': 'bicycle',
    },
    'vehicle.bus.bendy': 'large_car',
    'vehicle.bus.rigid': 'large_car',
    'vehicle.car': 'car',
    'vehicle.construction': None,
    'vehicle.ego': None,
    'vehicle.emergency.ambulance': 'large_car',
    'vehicle.emergency.police': 'car',
    'vehicle.motorcycle': {
        'cycle.with_rider': 'motorcyclist',
        'cycle.without_rider': 'motorcycle',
    },
    'vehicle.trailer': 'large_car',
    'vehicle.truck': 'large_car'
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
