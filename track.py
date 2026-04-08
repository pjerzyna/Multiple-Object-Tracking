class Track():
    """
    This class is used to track the position of the object, it contains:

    - id (the unique identifier of the object)
    - bbox (the bounding box of the object)
    - age (the number of frames since the object was first detected)
    - hits (the number of times the object has been detected) 
    - kalman_filter (it is used to predict the next position of the object, it contains: state and covariance)
    """
    
    pass