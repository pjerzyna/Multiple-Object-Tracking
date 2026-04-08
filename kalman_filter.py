from filterpy.kalman import KalmanFilter
import numpy as np


def create_kalman_filter(bbox):

    kf = KalmanFilter(dim_x=6, dim_z=4)

    kf.x = np.zeros((6, 1))

    kf.x[:4] = np.array(bbox).reshape((4, 1))
    return kf
