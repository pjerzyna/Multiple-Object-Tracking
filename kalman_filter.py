from filterpy.kalman import KalmanFilter
import numpy as np


def create_kalman_filter(bbox):

    kf = KalmanFilter(dim_x=6, dim_z=4)

    kf.x = np.zeros((6, 1))

    kf.x[:4] = np.array(bbox).reshape((4, 1))
    return kf

# def create_kalman_filter(bbox):
#     """
#         state vector: [x, y, w, h, vx, vy]4
#     """

#     kf = KalmanFilter(dim_x=6, dim_z=4)

#     kf.x[:4] = np.array(bbox).reshape((4, 1))

#     kf.F = np.array([
#         [1,0,0,0,1,0],
#         [0,1,0,0,0,1],
#         [0,0,1,0,0,0],
#         [0,0,0,1,0,0],
#         [0,0,0,0,1,0],
#         [0,0,0,0,0,1],
#     ])

#     kf.H = np.array([
#         [1,0,0,0,0,0],
#         [0,1,0,0,0,0],
#         [0,0,1,0,0,0],
#         [0,0,0,1,0,0],
#     ])

#     kf.P *= 10

#     kf.R *= 1

#     kf.Q *= 0.01

#     return kf