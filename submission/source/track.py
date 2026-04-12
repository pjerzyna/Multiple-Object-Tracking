import numpy as np

class Track():
    """
    This class is used to track the position of the object, it contains:

    - id (the unique identifier of the object)
    - bbox (the bounding box of the object)
    - age (the number of frames since the object was first detected)
    - hits (the number of times the object has been detected) 
    - kalman_filter (it is used to predict the next position of the object, it contains: state and covariance)
    - time_since_update (the number of frames since the object was last detected)
    """
    
    def __init__(self, id, bbox, kalman_filter):

         
        self.id = id
        self.bbox = bbox

        
        self.kalman_filter = kalman_filter

        self.age = 1
        self.hits = 1
        self.time_since_update = 0

    def predict(self):

        # This method should use the Kalman filter to predict the next 
        # position of the object and update the bbox attribute accordingly
        self.kalman_filter.predict()
        
        self.bbox = self.kalman_filter.x[:4].reshape(-1)

        self.age += 1
        self.time_since_update += 1


    def update(self, bbox):

        self.kalman_filter.update(np.array(bbox).reshape((4, 1)))
        self.bbox = self.kalman_filter.x[:4].reshape(-1)
        
        self.hits += 1
        self.time_since_update = 0

    def get_position(self):
        return self.bbox