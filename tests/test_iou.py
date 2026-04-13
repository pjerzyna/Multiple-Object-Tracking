import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))
from source.iou import compute_iou

def test_iou_perfect_overlap():
    box = [100, 100, 50, 50]
    assert compute_iou(box, box) == 1.0

def test_iou_no_overlap():
    box1 = [0, 0, 10, 10]
    box2 = [20, 20, 10, 10]
    assert compute_iou(box1, box2) == 0.0

def test_iou_partial_overlap():
    box1 = [100, 100, 50, 50]
    box2 = [125, 125, 50, 50]
    # Little tollerance for float numbers
    assert compute_iou(box1, box2) == pytest.approx(0.1428, abs=1e-3)