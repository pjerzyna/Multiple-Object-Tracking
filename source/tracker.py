from track import Track
from kalman_filter import create_kalman_filter
from association import associate_detections_to_tracks

class MultiObjectTracker:
    """
    Tracker Motion Model - A class to manage multiple object trackers. It's methods:
    - predict()
    - associate()
    - update()
    - create_tracks()
    - delete_tracks()
    """

    def __init__(self):
        self.trackers = []
        self.next_id = 1

    def add_tracker(self, tracker):
        # This method should add a new tracker to the list of trackers
        self.trackers.append(tracker)

    def update(self, detections):
        # 1. Prediction step
        self.predict()

        # 2. Association step
        matches, unmatched_dets, unmatched_tracks = associate_detections_to_tracks(detections, self.trackers)

        # 3. Update matched trackers with assigned detections
        for t, d in matches:
            bbox_only = detections[d][:4]
            self.trackers[t].update(bbox_only)

        # 4. Increase time_since_update for unmatched trackers
        for t in unmatched_tracks:
            self.trackers[t].time_since_update += 1

        # 5. Create new trackers for unmatched detections
        for d in unmatched_dets:
            bbox = detections[d][:4]
            kf = create_kalman_filter(bbox)
            self.trackers.append(Track(self.next_id, bbox, kf))
            self.next_id += 1

        # 6. Delete trackers that have not been updated for a certain number of frames
        # Keep tracks alive longer to reduce ID switches caused by temporary occlusions
        self.trackers = [
            t for t in self.trackers
            if t.time_since_update <= 50
        ]
    
    def predict(self):
        for tracker in self.trackers:
            tracker.predict()
    
    def associate(self, detections):
        # This method should implement the association logic between detections and existing trackers
        pass

    def create_tracks(self, detections):
        # This method should create new trackers for unmatched detections
        pass

    def delete_tracks(self):
        # This method should delete trackers that have not been updated for a certain number of frames
        pass

    def get_tracked_objects(self):
        return [(t.id, t.get_position()) for t in self.trackers]