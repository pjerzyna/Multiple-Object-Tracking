import os
import cv2
import numpy as np
from collections import defaultdict


def load_tracking_results(pred_path):
    """
    Load tracking results from txt file.
    
    Format: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,...
    
    Returns:
        dict: frame_id -> list of tracks
        Each track: {'id': int, 'bbox': [x, y, w, h]}
    """
    results = defaultdict(list)
    
    if not os.path.exists(pred_path):
        return results
    
    with open(pred_path, "r") as f:
        for line in f:
            values = line.strip().split(",")
            
            frame = int(values[0])
            track_id = int(values[1])
            bb_left = float(values[2])
            bb_top = float(values[3])
            bb_width = float(values[4])
            bb_height = float(values[5])
            
            results[frame].append({
                'id': track_id,
                'bbox': [int(bb_left), int(bb_top), int(bb_width), int(bb_height)]
            })
    
    return results


def load_ground_truth(gt_path):
    """
    Load ground truth data from gt.txt file.
    
    Format: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,...
    
    Returns:
        dict: frame_id -> list of gt objects
    """
    results = defaultdict(list)
    
    if not os.path.exists(gt_path):
        return results
    
    with open(gt_path, "r") as f:
        for line in f:
            values = line.strip().split(",")
            
            frame = int(values[0])
            obj_id = int(values[1])
            bb_left = float(values[2])
            bb_top = float(values[3])
            bb_width = float(values[4])
            bb_height = float(values[5])
            eval_flag = int(values[6])
            
            # Only include objects that should be evaluated
            if eval_flag == 1:
                results[frame].append({
                    'id': obj_id,
                    'bbox': [int(bb_left), int(bb_top), int(bb_width), int(bb_height)]
                })
    
    return results


def generate_colors(n_tracks):
    """Generate distinct colors for different track IDs."""
    np.random.seed(42)  # For reproducibility
    colors = {}
    for i in range(n_tracks):
        colors[i] = tuple(np.random.randint(0, 256, 3).tolist())
    return colors


def draw_bbox(frame, bbox, track_id, color, label_type="track"):
    """
    Draw a bounding box on the frame.
    
    Args:
        frame: cv2 image
        bbox: [x, y, w, h]
        track_id: ID of the track
        color: (B, G, R) tuple
        label_type: "track" or "gt"
    """
    x, y, w, h = bbox
    x2 = x + w
    y2 = y + h
    
    thickness = 2
    
    # Draw rectangle
    cv2.rectangle(frame, (x, y), (x2, y2), color, thickness)
    
    # Draw label
    label = f"{'ID' if label_type == 'track' else 'GT'}: {track_id}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    
    # Get text size for background
    text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
    
    # Draw background rectangle for text
    cv2.rectangle(
        frame,
        (x, y - text_size[1] - 4),
        (x + text_size[0] + 4, y),
        color,
        -1
    )
    
    # Draw text
    cv2.putText(
        frame,
        label,
        (x + 2, y - 2),
        font,
        font_scale,
        (255, 255, 255),
        font_thickness
    )
    
    return frame


def visualize_sequence(img_dir, tracking_results, gt_results=None, output_video=None, fps=30):
    """
    Visualize tracking results on video frames.
    
    Args:
        img_dir: Directory with image frames
        tracking_results: Dict from load_tracking_results
        gt_results: Dict from load_ground_truth (optional)
        output_video: Path to save output video (if None, displays only)
        fps: Frames per second for output video
    """
    if not os.path.exists(img_dir):
        print(f"Error: Image directory {img_dir} does not exist")
        return
    
    # Get list of image files
    img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png'))])
    
    if not img_files:
        print(f"Error: No images found in {img_dir}")
        return
    
    # Get all track IDs for color assignment
    all_ids = set()
    for tracks in tracking_results.values():
        for track in tracks:
            all_ids.add(track['id'])
    
    colors = generate_colors(len(all_ids))
    
    # Setup video writer if output path provided
    video_writer = None
    if output_video:
        first_img = cv2.imread(os.path.join(img_dir, img_files[0]))
        height, width = first_img.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    print(f"Visualizing {len(img_files)} frames...")
    
    for frame_idx, img_file in enumerate(img_files, start=1):
        img_path = os.path.join(img_dir, img_file)
        frame = cv2.imread(img_path)
        
        if frame is None:
            continue
        
        # Draw ground truth (if available) - light blue, thinner
        if gt_results and frame_idx in gt_results:
            for gt_obj in gt_results[frame_idx]:
                gt_id = gt_obj['id']
                bbox = gt_obj['bbox']
                gt_color = (200, 150, 0)  # Cyanish for ground truth
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), gt_color, 1)
        
        # Draw tracking results
        if frame_idx in tracking_results:
            for track in tracking_results[frame_idx]:
                track_id = track['id']
                bbox = track['bbox']
                color = colors.get(track_id, (0, 255, 0))
                frame = draw_bbox(frame, bbox, track_id, color, label_type="track")
        
        # Add frame number
        cv2.putText(
            frame,
            f"Frame: {frame_idx}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Display frame
        cv2.imshow("Tracking Visualization", frame)
        
        # Write to video file if output path provided
        if video_writer:
            video_writer.write(frame)
        
        # Press 'q' to quit, space to pause
        key = cv2.waitKey(33) & 0xFF  # ~30 FPS
        if key == ord('q'):
            break
        elif key == ord(' '):
            # Pause - wait for next key
            while True:
                key = cv2.waitKey(0) & 0xFF
                if key == ord(' ') or key == ord('q'):
                    break
            if key == ord('q'):
                break
    
    # Release video writer
    if video_writer:
        video_writer.release()
        print(f"Video saved to {output_video}")
    
    cv2.destroyAllWindows()
    print("Visualization complete!")


def visualize_dataset_sequence(sequence_name, data_dir, gt_base_dir, img_base_dir, output_video=None):
    """
    High-level function to visualize a specific dataset sequence.
    
    Args:
        sequence_name: e.g., "MOT_02"
        data_dir: Directory with tracking results (e.g., ../data_test)
        gt_base_dir: Base directory with ground truth (e.g., ../evs_mot-train)
        img_base_dir: Base directory with images (e.g., ../evs_mot-train)
        output_video: Optional path to save output video
    """
    # Construct paths
    pred_path = os.path.join(data_dir, f"{sequence_name}.txt")
    img_dir = os.path.join(img_base_dir, sequence_name, "img1")
    
    # For mot-test 
    gt_path = None
    if gt_base_dir is not None:
        gt_path = os.path.join(gt_base_dir, sequence_name, "gt", "gt.txt")

    # Load data
    tracking_results = load_tracking_results(pred_path)    
    if not tracking_results:
        print(f"Warning: No tracking results found for {sequence_name}")
    
    gt_results = None
    if gt_path and os.path.exists(gt_path):
        gt_results = load_ground_truth(gt_path)
    else:
        print(f"Info: Ground Truth not found or skipped for {sequence_name}")


    print(f"\nVisualizing {sequence_name}:")
    print(f"  Tracking results: {pred_path}")
    print(f"  Ground truth: {gt_path}")
    print(f"  Images: {img_dir}")
    
    if output_video:
        print(f"  Output video: {output_video}")
    
    # Visualize
    visualize_sequence(img_dir, tracking_results, gt_results, output_video)
