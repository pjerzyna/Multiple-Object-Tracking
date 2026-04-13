# API Documentation

## Core Classes

### MultiObjectTracker

Main tracker class that manages multiple tracking tasks.

```python
from tracker import MultiObjectTracker

tracker = MultiObjectTracker()
tracker.update(detections)  # Update with new detections
results = tracker.get_tracked_objects()  # Get current tracks
```

**Methods:**
- `update(detections)` - Process new frame detections
  - **Input:** List of detections: `[[x, y, w, h, conf], ...]`
  - **Description:** Associates detections to tracks, updates existing tracks, creates new tracks
  
- `predict()` - Predict next positions
  - **Description:** Uses Kalman filter to predict next position for each track
  
- `get_tracked_objects()` - Get current tracked objects
  - **Output:** List of tuples: `[(track_id, bbox), ...]`
  - **bbox:** `[x, y, w, h]`

### Track

Represents a single tracked object.

```python
from track import Track
from kalman_filter import create_kalman_filter

bbox = [100, 200, 50, 80]
kf = create_kalman_filter(bbox)
track = Track(id=1, bbox=bbox, kalman_filter=kf)

track.predict()  # Predict next position
track.update(new_bbox)  # Update with detection
position = track.get_position()  # Get current position
```

**Attributes:**
- `id` - Unique track identifier
- `bbox` - Current bounding box `[x, y, w, h]`
- `age` - Frames since track creation
- `hits` - Number of times track was updated with detection
- `time_since_update` - Frames since last detection

**Methods:**
- `predict()` - Predict next position using Kalman filter
- `update(bbox)` - Update track with new detection
- `get_position()` - Return current bounding box

## Data Loading

### dataset.py

```python
from dataset import load_detections, load_seqinfo, get_total_frames

# Load detections from det.txt
detections = load_detections("path/to/det.txt")
# Returns: {frame_id: [[x, y, w, h, conf], ...], ...}

# Load sequence info
seqinfo = load_seqinfo("path/to/seqinfo.ini")
# Returns: {"width": "1920", "height": "1080", ...}

# Get total number of frames
total_frames = get_total_frames(seqinfo)
```

## Evaluation

### evaluation.py

```python
from evaluation import (
    load_ground_truth, 
    load_predictions, 
    compute_mota, 
    evaluate_sequences
)

# Evaluate single sequence
gt_data = load_ground_truth("gt.txt")
pred_data = load_predictions("results.txt")
metrics = compute_mota(gt_data, pred_data)

print(f"MOTA: {metrics['MOTA']:.2%}")
print(f"Recall: {metrics['Recall']:.2%}")
print(f"Precision: {metrics['Precision']:.2%}")

# Evaluate all sequences
results = evaluate_sequences("../data_test", "../evs_mot-train")
```

**Metrics Returned:**
- `MOTA` - Multiple Object Tracking Accuracy (main metric)
- `Recall` - Detection rate
- `Precision` - False positive rate inverse
- `FN` - False negatives count
- `FP` - False positives count
- `IDSW` - ID switches count
- `GT` - Total ground truth objects

## Visualization

### visualization.py

```python
from visualization import visualize_dataset_sequence

# Visualize tracking results
visualize_dataset_sequence(
    sequence_name="MOT_02",
    data_dir="../data_test",
    gt_base_dir="../evs_mot-train",
    img_base_dir="../evs_mot-train",
    output_video=None  # Optional: save to video file
)
```

**Interactive Controls During Visualization:**
- **Spacebar** - Pause/Resume
- **Q** - Quit

## Utilities

### iou.py

```python
from iou import compute_iou

box1 = [100, 200, 50, 80]  # [x, y, w, h]
box2 = [110, 210, 50, 80]

iou = compute_iou(box1, box2)
print(f"IoU: {iou:.3f}")  # Returns value between 0 and 1
```

### kalman_filter.py

```python
from kalman_filter import create_kalman_filter

bbox = [100, 200, 50, 80]
kf = create_kalman_filter(bbox)

# Kalman filter object with:
# - State: [x, y, w, h, vx, vy] (position and velocity)
# - Measurement: [x, y, w, h]
# - Prediction using constant-velocity motion model
```

### association.py

```python
from association import associate_detections_to_tracks

detections = [[x, y, w, h, conf], ...]
tracks = [Track(...), ...]

matches, unmatched_dets, unmatched_tracks = associate_detections_to_tracks(
    detections, 
    tracks,
    iou_threshold=0.2
)

# matches: [(track_idx, det_idx, iou), ...]
# unmatched_dets: [det_idx, ...]
# unmatched_tracks: [track_idx, ...]
```

## Command-Line Interface

### Main Entry Point

```bash
cd source
python main.py --mode <mode> [OPTIONS]
```

**Modes:**

| Mode | Purpose | Command |
|------|---------|---------|
| tracker | Process test sequences | `python main.py --mode tracker` |
| single_tracker | Process single sequence | `python main.py --mode single_tracker` |
| test_tracker | Process training sequences | `python main.py --mode test_tracker` |
| evaluation | Evaluate results | `python main.py --mode evaluation` |
| visualization | Visualize results | `python main.py --mode visualization --sequence MOT_02` |
| det | Test detection loading | `python main.py --mode det` |
| seqinfo | Test sequence info loading | `python main.py --mode seqinfo` |
| iou | Test IoU function | `python main.py --mode iou` |

**Visualization Options:**

```bash
python main.py --mode visualization \
    --sequence MOT_02 \
    --data-dir ../data_test \
    --output-video ../result.mp4
```

- `--sequence` - Sequence to visualize (default: MOT_02)
- `--data-dir` - Directory with tracking results (default: ../data_test)
- `--output-video` - Optional: save visualization to video file

## Algorithm Parameters

Key parameters that can be tuned:

### tracker.py
- **Track survival threshold** (line ~32): `time_since_update <= 50`
  - Increase to keep tracks longer
  - Decrease for more aggressive deletion

### association.py
- **IoU matching threshold** (line ~6): `IOU_THRESHOLD = 0.2`
  - Increase for stricter matching
  - Decrease for more flexible matching

### kalman_filter.py
- **Measurement noise** (line ~39): `kf.R = np.eye(4) * 5.0`
  - Higher = trust model more
  - Lower = trust measurements more
  
- **Process noise** (line ~42): `kf.Q = np.eye(6) * 0.1`
  - Higher = expect more motion variation
  - Lower = expect smooth motion

## Example Workflow

```python
import glob
from dataset import load_detections
from tracker import MultiObjectTracker

# Load detections
det_path = "../evs_mot-test/MOT_01/det/det.txt"
detections = load_detections(det_path)

# Initialize tracker
tracker = MultiObjectTracker()

# Process all frames
results = []
for frame_id in sorted(detections.keys()):
    tracker.update(detections[frame_id])
    for track_id, bbox in tracker.get_tracked_objects():
        results.append(f"{frame_id},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1")

# Save results
with open("output.txt", "w") as f:
    f.write("\n".join(results))
```
