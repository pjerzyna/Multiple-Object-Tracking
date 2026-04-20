from scipy.optimize import linear_sum_assignment
import numpy as np
from iou import compute_iou


IOU_THRESHOLD = 0.4

def associate_detections_to_tracks(detections, tracks):
    """
        This function performs the association between the current frame detections and existing tracks
        using the Hungarian algorithm.
    """

    if len(tracks) == 0:
        return [], list(range(len(detections))), []


    cost_matrix = np.zeros((len(tracks), len(detections)))


    for t, track in enumerate(tracks):
        for d, det in enumerate(detections):
            cost_matrix[t, d] = 1 - compute_iou(track.bbox.tolist(), det[:4])


    track_idx, det_idx = linear_sum_assignment(cost_matrix)
    
    matches = []
    unmatched_tracks = list(set(range(len(tracks))) - set(track_idx))
    unmatched_detections = list(set(range(len(detections))) - set(det_idx))

    for t, d in zip(track_idx, det_idx):
        if cost_matrix[t, d] < (1 - IOU_THRESHOLD):
            matches.append((t, d))
        else:
            unmatched_tracks.append(t)
            unmatched_detections.append(d)


    return matches, unmatched_detections, unmatched_tracks