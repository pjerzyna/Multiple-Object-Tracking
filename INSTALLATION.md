# Installation Guide

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Step-by-Step Installation

### 1. Clone or Download the Repository

```bash
cd Multiple-Object-Tracking
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `numpy>=1.19.0` - Numerical computations
- `scipy>=1.5.0` - Scientific algorithms (Hungarian method)
- `filterpy>=1.4.2` - Kalman filter implementation
- `opencv-python>=4.5.0` - Image/video processing

### 4. Verify Installation

Test if everything is working:

```bash
cd source
python main.py --mode iou
```

You should see an IoU test output.

## Running the Tracker

### Basic Usage (Generate Test Results)

```bash
cd source
python main.py --mode tracker
```

Output files will be created in `../data/`:
- MOT_01.txt
- MOT_06.txt
- MOT_07.txt

### Additional Modes

```bash
# Validate on training data
python main.py --mode test_tracker

# Evaluate results
python main.py --mode evaluation

# Visualize results
python main.py --mode visualization --sequence MOT_02
```

## Troubleshooting

### "Module not found" errors

Make sure you're in the correct directory and dependencies are installed:

```bash
# Verify you're in the source directory
cd source

# Reinstall dependencies
pip install -r ../requirements.txt
```

### OpenCV errors (video visualization)

If you get OpenCV display errors:

```bash
pip install --upgrade opencv-python
```

### Permission errors on Linux/Mac

```bash
chmod +x source/main.py
```

## System-Specific Notes

### Windows

- Use `.venv\Scripts\activate` to activate virtual environment
- Forward slashes (/) in paths are generally okay in Python

### macOS/Linux

- Use `python3` instead of `python` if Python 2 is also installed
- Use `source .venv/bin/activate` to activate virtual environment

## Next Steps

After installation:

1. Read [README.md](README.md) for quick start
2. See [README_pl.md](README_pl.md) for detailed documentation
3. Run examples in the [Usage Guide](README.md#usage)
