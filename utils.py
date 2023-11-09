import numpy as np

def PxyXY_to_Nxcycwh(xyXY, width_pixels, height_pixels):
    '''
    Convert from pixel [x_min, y_min, x_max, y_max] to
    normalized [x_center, y_center, width, height]

    Both are left-top origin.
    '''
    # Convert input to a NumPy array
    xyXY = np.asarray(xyXY, dtype=np.float32)
    
    # Calculate the width and height of the bounding box
    box_width_height = xyXY[2:] - xyXY[:2]
    
    # Calculate the center of the bounding box
    box_center = xyXY[:2] + box_width_height / 2.0
    
    # Normalize the center coordinates and dimensions
    normalized = np.hstack((box_center / [width_pixels, height_pixels],
                            box_width_height / [width_pixels, height_pixels]))
    
    return normalized

def test_PxyWX_to_Nxcycwh():
    assert np.all(PxyXY_to_Nxcycwh([0, 0, 200, 100], 200, 100) == np.array([0.5, 0.5, 1, 1]))
    assert np.all(PxyXY_to_Nxcycwh([0, 0, 0, 0], 1920, 1080) == np.array([0., 0., 0., 0.]))
    assert np.all(PxyXY_to_Nxcycwh([2, 1, 3, 2], 5, 4) == np.array([0.5, 0.375, 0.20, 0.25]))
