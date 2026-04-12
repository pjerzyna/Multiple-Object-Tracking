# Multiple-Object-Tracking

A Python implementation of **SORT** (Simple Online Realtime Tracking) - a multiple object tracking algorithm based on predefined detections.

## Quick Start

```bash
cd source
python main.py --mode tracker
```

This generates tracking results for all test sequences (MOT_01, MOT_06, MOT_07) in `../data/`.

## What is This Project?

This project implements multi-object tracking to:
- Track multiple objects across video frames
- Maintain consistent object IDs
- Evaluate tracking performance using MOTA metric
- Visualize tracking results

## Key Features

- ✅ **SORT Algorithm** - Combination of Kalman Filter + Hungarian Algorithm
- ✅ **MOTA Evaluation** - Standard MOT metric for tracking quality assessment
- ✅ **Multiple Modes** - Training, testing, evaluation, and visualization
- ✅ **Video Visualization** - Real-time frame-by-frame viewing with optional video output

## Installation

1. Install Python 3.7+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

See [README_pl.md](README_pl.md) for detailed documentation in Polish.

### Available Modes:

```bash
cd source

# Process test sequences (MOT_01, MOT_06, MOT_07)
python main.py --mode tracker

# Process training sequences for validation (MOT_02-05)
python main.py --mode test_tracker

# Evaluate results using MOTA metric
python main.py --mode evaluation

# Visualize tracking results
python main.py --mode visualization --sequence MOT_02
```

## Project Structure

```
Multiple-Object-Tracking/
├── source/                  # Source code
│   ├── main.py             # Main entry point
│   ├── tracker.py          # Multi-object tracker
│   ├── track.py            # Individual track class
│   ├── kalman_filter.py    # Kalman filter implementation
│   ├── association.py      # Track-detection association
│   ├── iou.py              # Intersection over Union
│   ├── dataset.py          # Data loading utilities
│   ├── evaluation.py       # MOTA metric computation
│   └── visualization.py    # Visualization tools
├── data/                   # Output tracking results
├── evs_mot-test/          # Test sequences (MOT_01, 06, 07)
└── evs_mot-train/         # Training sequences (MOT_02-05)
```

## Algorithm Overview

**SORT** (Simple Online Realtime Tracking):

1. **Prediction** - Kalman filter predicts next object position
2. **Association** - Hungarian algorithm matches detections to tracks using IoU
3. **Update** - Matched tracks are updated, new detections create new tracks
4. **Management** - Tracks without detections for >50 frames are deleted

## Performance

Test results on training sequences:
- MOT_02: 14.41% MOTA
- MOT_03: -293.54% MOTA
- MOT_04: -73.90% MOTA
- MOT_05: -497.42% MOTA
- **Average: -212.61% MOTA**

(Performance varies by sequence difficulty; variations in precision/recall reflect detector quality)

## Requirements

- Python 3.7+
- numpy >= 1.19.0
- scipy >= 1.5.0
- filterpy >= 1.4.2
- opencv-python >= 4.5.0

See [requirements.txt](requirements.txt) for details.

## References

- SORT: Simple Online and Realtime Tracking (Bewley et al., 2016)
- MOT Challenge: http://motchallenge.net/
