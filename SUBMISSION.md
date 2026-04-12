# Submission Format

This document explains the submission structure required for the MOT challenge.

## Submission Requirements

### Output Format

Tracking results must be in MOT format. Each line represents one tracked object instance:

```
<frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,1,-1,-1,-1
```

Where:
- `<frame>` - Frame number (1-indexed)
- `<id>` - Unique track ID for this object within the sequence
- `<bb_left>` - Left coordinate of bounding box (pixels)
- `<bb_top>` - Top coordinate of bounding box (pixels)
- `<bb_width>` - Width of bounding box (pixels)
- `<bb_height>` - Height of bounding box (pixels)
- `1` - Confidence (fixed at 1)
- `-1,-1,-1` - Reserved fields (fixed at -1)

### Example

```
1,1,125.50,234.75,50.25,80.50,1,-1,-1,-1
1,2,456.00,345.25,48.75,79.50,1,-1,-1,-1
2,1,128.00,237.00,50.50,80.75,1,-1,-1,-1
2,2,458.50,348.00,49.00,79.75,1,-1,-1,-1
```

## Submission Package Structure

Submissions must be provided as a single `.zip` file with the following structure:

```
submission.zip
└── submission/
    ├── data/
    │   ├── MOT_01.txt
    │   ├── MOT_06.txt
    │   └── MOT_07.txt
    └── source/
        ├── main.py
        ├── dataset.py
        ├── tracker.py
        ├── track.py
        ├── kalman_filter.py
        ├── association.py
        ├── iou.py
        ├── evaluation.py
        ├── visualization.py
        ├── requirements.txt
        └── __pycache__/
```

### Description

- **data/** - Contains tracking results for test sequences
  - Must include MOT_01.txt, MOT_06.txt, MOT_07.txt
  
- **source/** - Contains complete source code
  - All Python files required to generate results
  - requirements.txt for dependencies
  - Complete implementation of the tracking algorithm

## How to Create Submission

### Step 1: Generate Results

```bash
cd source
python main.py --mode tracker
```

This creates output files in `../data/`:
- MOT_01.txt
- MOT_06.txt
- MOT_07.txt

### Step 2: Create Submission Structure

```bash
# Create submission directory structure
mkdir -p submission/data submission/source

# Copy tracking results
cp data/MOT_*.txt submission/data/

# Copy source code
cp source/* submission/source/
```

### Step 3: Create ZIP File

```bash
# Windows (PowerShell)
Compress-Archive -Path "submission" -DestinationPath "submission.zip" -Force

# macOS/Linux
zip -r submission.zip submission/
```

### Step 4: Verify ZIP Contents

Before submitting, verify the structure:

```bash
# Windows (PowerShell)
Get-ChildItem -Path "submission" -Recurse

# macOS/Linux
unzip -l submission.zip
```

Ensure all required files are present:
- submission/data/MOT_01.txt
- submission/data/MOT_06.txt
- submission/data/MOT_07.txt
- submission/source/main.py
- submission/source/[all other .py files]

## Validation Checklist

Before submitting:

- [ ] ✅ All three test sequences have output files (MOT_01.txt, MOT_06.txt, MOT_07.txt)
- [ ] ✅ Output files follow MOT format
- [ ] ✅ All source code files are included
- [ ] ✅ requirements.txt is present and complete
- [ ] ✅ Code runs successfully with `python main.py --mode tracker`
- [ ] ✅ ZIP file is properly structured

## Result File Format Validation

Check that each output file is correctly formatted:

```bash
# Example: Check MOT_01.txt
head -5 submission/data/MOT_01.txt
```

Expected output:
```
1,<id>,<x>,<y>,<w>,<h>,1,-1,-1,-1
1,<id>,<x>,<y>,<w>,<h>,1,-1,-1,-1
...
```

## Notes

- Track IDs can be arbitrary but must be unique within each sequence
- Floating-point coordinates are allowed
- Files should use Unix line endings (LF, not CRLF)
- ZIP file should be named `submission.zip`
