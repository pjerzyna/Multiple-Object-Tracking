def compute_iou(boxA, boxB):
    """
    This file contains the implementation of the Intersection over Union (IoU) function which is used to
    calculate the overlap between two bounding boxes. It is used in the association step of 
    the muliti-object tracking algorithm to determine which detections correspond to which trackers. 
    Final score is always between 0 and 1.

    Args:
        boxA: [x, y, w, h]
        boxB: [x, y, w, h]
    """
    
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])

    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    inter_width = max(0, xB - xA)
    inter_height = max(0, yB - yA)

    intersection = inter_width * inter_height

    areaA = boxA[2] * boxA[3]
    areaB = boxB[2] * boxB[3]

    union = areaA + areaB - intersection

    if union == 0:
        return 0

    return intersection / union