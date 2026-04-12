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
        # 1. Predykcja polozenia
        self.predict()

        # 2. Asocjacja detekcji do trackerow
        matches, unmatched_dets, unmatched_tracks = associate_detections_to_tracks(detections, self.trackers)

        # 3. Aktualizacja dopasowanych trackerow
        for t, d in matches:
            bbox_only = detections[d][:4]
            self.trackers[t].update(bbox_only)

        # 4. Increment age for unmatched tracks (they may still be visible but undetected)
        for t in unmatched_tracks:
            self.trackers[t].time_since_update += 1

        # 5. Initializacja nowych trackerow dla niedopasowanych detekcji
        for d in unmatched_dets:
            bbox = detections[d][:4]
            kf = create_kalman_filter(bbox)
            self.trackers.append(Track(self.next_id, bbox, kf))
            self.next_id += 1

        # 6. Usuwanie trackerow, ktore nie byly aktualizowane przez za dluga liczbe klatek
        # Keep tracks alive longer to reduce ID switches caused by temporary occlusions
        self.trackers = [
            t for t in self.trackers
            if t.time_since_update <= 50  # Increased from 10 to 50 frames
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