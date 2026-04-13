from filterpy.kalman import KalmanFilter
import numpy as np


def create_kalman_filter(bbox):
    """
    State: [x, y, w, h, vx, vy] (position, size, velocity)
    Measurement: [x, y, w, h] (position and size only)
    """
    kf = KalmanFilter(dim_x=6, dim_z=4)
    
    # State transition matrix (constant velocity model)
    # x' = x + vx*dt, y' = y + vy*dt, etc. (assuming dt=1)
    dt = 1.0
    kf.F = np.array([
        [1, 0, 0, 0, dt, 0],
        [0, 1, 0, 0, 0, dt],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1]
    ], dtype=np.float32)
    
    # Measurement matrix: we only measure position and size, not velocity
    kf.H = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0]
    ], dtype=np.float32)
    
    # Measurement noise: higher values = trust model more than measurements
    kf.R = np.eye(4, dtype=np.float32) * 5.0
    
    # Process noise: lower values = expect smooth motion
    kf.Q = np.eye(6, dtype=np.float32) * 0.1
    kf.Q[4:, 4:] *= 0.01  # Even less process noise on velocity
    
    # State covariance: initial uncertainty
    kf.P = np.eye(6, dtype=np.float32)
    kf.P[4:, 4:] *= 1000.0  # High uncertainty on velocity initially
    
    # Initialize state
    kf.x = np.zeros((6, 1), dtype=np.float32)
    kf.x[:4] = np.array(bbox).reshape((4, 1))
    
    return kf