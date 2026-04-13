# Multiple-Object-Tracking


## SORT (Simple Online Realtime Tracking) framework
This is multiple object tracking algorithm based on predefined detections relies on two main components: Kalman Filtering for motion prediction and the Hungarian Algorithm for data association.:


Each tracked object is modeled using a linear constant velocity motion model. The state vector of each track is defined as:
```
state = [x, y, h, w, vx, vy]
```

## Tracking pipeline

1. **Prediction**: The Kalman Filter predicts the location of each tracked object in the current frame based on its previous state.

2. **Cost Calculation**: An assignment cost matrix is computed using Intersection over Union (IoU) between predicted track positions and newly received detections.
  ```bash
  Distance Metric: Cost=1−IoU
  ```
3. **Data Association**: The Hungarian Algorithm (Linear Assignment) is used to optimally match detections with existing tracks based on the cost matrix.

4. **Track Management**:

- Matched Tracks: The Kalman Filter state is updated using the matched detection.

- Unmatched Detections: A new track is initialized for each unmatched detection.

- Unmatched Tracks: The track age is increased and tracks that remain unmatched for more than a predefined threshold (e.g., 50 frames) are removed.



## Usage & Workflow
0. Install dependencies, it is worth to create dedicated environment:
```bash
pip install -r requirements.txt
```

1. Process training sequences to generate tracking data:

2. Evaluate results:

3. Analyze & Fine-tune: Adjust algorithm parameters based on the evaluation output.

4. Final Run: Once satisfied, process the test sequences:

## Modes
```bash
cd source

# Process training sequences for validation (MOT_02-05)
python main.py --mode test_tracker

# Evaluate results using MOTA metric
python main.py --mode evaluation

# Process test sequences (MOT_01, MOT_06, MOT_07)
python main.py --mode tracker

# Visualize tracking results
python main.py --mode visualization --sequence MOT_02
```

Apart form the visualization of the tracking results you can also save the video using the following command:

```bash
# Visualize results and save the video
python main.py --mode visualization --sequence MOT_03 --output-video ../MOT_03_tracked.mp4
```

####  Legend:
- **Thick colored boxes** - Tracker results (assigned IDs)
- **Thin light boxes** - Ground truth (reference points)
- **ID: XXX** - Unique identifier assigned by the tracker



## Project Structure

```
Multiple-Object-Tracking/
├── source/                  # Source code
│   ├── main.py              # Main entry point
│   ├── tracker.py           # Multi-object tracker
│   ├── track.py             # Individual track class
│   ├── kalman_filter.py     # Kalman filter implementation
│   ├── association.py       # Track-detection association
│   ├── iou.py               # Intersection over Union
│   ├── dataset.py           # Data loading utilities
│   ├── evaluation.py        # MOTA metric computation
│   └── visualization.py     # Visualization tools
├── tests/                   # Pytests
├── data_tets/               # Output test tracking results
├── data_train/              # Output train tracking results
├── evs_mot-test/            # Test sequences (MOT_01, 06, 07)
└── evs_mot-train/           # Training sequences (MOT_02, 03, 04, 05)
```

## Performance

Test results on training sequences:
- MOT_01: ???% MOTA
- MOT_02: ???% MOTA
- MOT_03: ???% MOTA
- MOT_04: ???% MOTA
- MOT_05: ???% MOTA
- MOT_06: ???% MOTA
- MOT_07: ???% MOTA
- **Average: ???% MOTA**


## References

- SORT: Simple Online and Realtime Tracking (Bewley et al., 2016)
- MOT Challenge: http://motchallenge.net/
