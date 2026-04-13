import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))
from source.dataset import load_detections


def test_load_detections_format(tmp_path):
    d = tmp_path / "test_det.txt"
    # Format: <frame>,-1,<x>,<y>,<w>,<h>,<conf>
    d.write_text("1,-1,10.5,20.0,30.0,40.5,0.95\n2,-1,50.0,60.0,70.0,80.0,0.88")

    detections = load_detections(str(d))

    # Check if 2 frames were loaded
    assert len(detections) == 2
    # Check if frame 1 data is correct
    # Expected: [x, y, w, h, conf]
    assert detections[1][0] == [10.5, 20.0, 30.0, 40.5, 0.95]
    
    # Check data types (should be float)    
    assert isinstance(detections[1][0][0], float)

def test_load_detections_empty_file(tmp_path):
    d = tmp_path / "empty.txt"
    d.write_text("")
    detections = load_detections(str(d))
    assert len(detections) == 0

def test_load_detections_mot01_frame1(tmp_path):
    # Prepare path for temporary det.txt
    test_file = tmp_path / "det.txt"
    
    # Real data from MOT_01 frame 1 (7 columns format)
    # Format: <frame>,-1,<x>,<y>,<w>,<h>,<conf>
    content = (
        "1,-1,915.1,481.5,94.7,113.5,1.0\n"
        "1,-1,836.7,472.8,53.5,76.2,1.0\n"
        "1,-1,376.0,446.6,42.7,104.8,1.0\n"
        "1,-1,442.4,448.3,109.1,275.4,1.0\n"
        "1,-1,586.4,445.0,87.8,265.6,1.0\n"
        "1,-1,1340.1,415.1,166.4,376.9,1.0\n"
        "1,-1,796.5,474.9,54.9,61.6,1.0\n"
        "1,-1,1090.5,481.4,34.8,118.8,1.0\n"
        "1,-1,1055.1,485.2,38.4,107.9,1.0\n"
        "1,-1,1256.8,449.2,34.1,99.5,1.0\n"
        "1,-1,1014.4,431.1,44.4,122.4,1.0\n"
        "1,-1,1099.0,437.3,42.4,111.0,1.0\n"
        "1,-1,1463.8,414.5,120.2,353.2,0.094\n"
    )
    test_file.write_text(content)

    detections = load_detections(str(test_file))

    # ASSERTIONS
    # Was only one frame (Frame 1) loaded?    
    assert len(detections) == 1
    assert 1 in detections

    # Does the number of detections in frame 1 match the expected count (13)?
    assert len(detections[1]) == 13

    # Verify specific values for the first detection
    # Expected format: [x, y, w, h, conf]
    expected_first = [915.1, 481.5, 94.7, 113.5, 1.0]
    assert detections[1][0] == expected_first

    # Verify the last detection (low confidence case)    
    expected_last = [1463.8, 414.5, 120.2, 353.2, 0.094]
    assert detections[1][-1] == expected_last
    
    # Check data types (should be float)    
    for val in detections[1][0]:
        assert isinstance(val, float)