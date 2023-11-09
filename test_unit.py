from classes import *

def test_simplify_nuimage_labels():
    assert simplify_nuimage_labels('vehicle.bicycle', 'cycle.without_rider') == 'bicycle'
    assert simplify_nuimage_labels('vehicle.bicycle', 'cycle.with_rider') == 'cyclist'
    assert simplify_nuimage_labels('vehicle.truck', None) == 'truck'


from utils import *

def test_PxyWX_to_Nxcycwh():
    assert np.all(PxyXY_to_Nxcycwh([0, 0, 200, 100], 200, 100) == np.array([0.5, 0.5, 1, 1]))
    assert np.all(PxyXY_to_Nxcycwh([0, 0, 0, 0], 1920, 1080) == np.array([0., 0., 0., 0.]))
    assert np.all(PxyXY_to_Nxcycwh([2, 1, 3, 2], 5, 4) == np.array([0.5, 0.375, 0.20, 0.25]))