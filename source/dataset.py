import os
from collections import defaultdict

"""
    Dataset parser for MOT detection files.
    Reads det.txt and groups detections into:
    det.txt fromat: <frame>,-1,<bb_left>,<bb_top>,<bb_width>,<bb_height>,<confidence>


    frame_id -> list of detections

    One particular detection format: [x, y, w, h, confidence]
    Group of detections = {
        1: [
            [x, y, w, h, conf],
            [x, y, w, h, conf]
        ],
        2: [...]
    }
"""


def load_detections(det_path):
    detections = defaultdict(list) 

    with open(det_path, "r") as f:

        for line in f:

            values = line.strip().split(",")

            frame = int(values[0])

            x = float(values[2])
            y = float(values[3])
            w = float(values[4])
            h = float(values[5])

            conf = float(values[6])

            detections[frame].append([x, y, w, h, conf])

    return detections

def load_seqinfo(seqinfo_path):
    info = {}

    with open(seqinfo_path, "r") as f:

        for line in f:

            if "=" in line:

                key, value = line.strip().split("=")

                info[key] = value

    return info

# Iterator for frames
def get_total_frames(seqinfo):
    return int(seqinfo["seqLength"])