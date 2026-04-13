import os
from collections import defaultdict
import numpy as np
from iou import compute_iou


def load_ground_truth(gt_path):
    """
    Format: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,<eval_flag>,<class>,<visibility>
    
    Returns:
        dict: frame_id -> list of gt objects
        Each gt object: {
            'id': int,
            'bbox': [x, y, w, h],
            'eval_flag': int,
            'class': int,
            'visibility': float
        }
    """
    gt_data = defaultdict(list)
    
    if not os.path.exists(gt_path):
        return gt_data
    
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
            obj_class = int(values[7])
            visibility = float(values[8])
            
            # Only include objects that should be evaluated
            if eval_flag == 1:
                gt_data[frame].append({
                    'id': obj_id,
                    'bbox': [bb_left, bb_top, bb_width, bb_height],
                    'class': obj_class,
                    'visibility': visibility
                })
    
    return gt_data


def load_predictions(pred_path):
    """
    Format: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,<conf>,<class>,<visibility>,<unused>
    
    Returns:
        dict: frame_id -> list of predictions
        Each prediction: {
            'id': int,
            'bbox': [x, y, w, h],
            'conf': float
        }
    """
    pred_data = defaultdict(list)
    
    if not os.path.exists(pred_path):
        return pred_data
    
    with open(pred_path, "r") as f:
        for line in f:
            values = line.strip().split(",")
            
            frame = int(values[0])
            obj_id = int(values[1])
            bb_left = float(values[2])
            bb_top = float(values[3])
            bb_width = float(values[4])
            bb_height = float(values[5])
            conf = float(values[6])
            
            pred_data[frame].append({
                'id': obj_id,
                'bbox': [bb_left, bb_top, bb_width, bb_height],
                'conf': conf
            })
    
    return pred_data


def match_detections(gt_objects, pred_objects, iou_threshold=0.5):
    """
    Match ground truth objects with predictions using IoU.
    
    Args:
        gt_objects: list of gt objects with 'id' and 'bbox'
        pred_objects: list of predictions with 'id' and 'bbox'
        iou_threshold: minimum IoU to consider a match
    
    Returns:
        matches: list of (gt_idx, pred_idx, iou) tuples
        unmatched_gt: list of unmatched gt indices
        unmatched_pred: list of unmatched pred indices
    """
    matches = []
    unmatched_gt = list(range(len(gt_objects)))
    unmatched_pred = list(range(len(pred_objects)))
    
    if len(gt_objects) == 0 or len(pred_objects) == 0:
        return matches, unmatched_gt, unmatched_pred
    
    # Calculate IoU matrix
    iou_matrix = np.zeros((len(gt_objects), len(pred_objects)))
    for g_idx, gt_obj in enumerate(gt_objects):
        for p_idx, pred_obj in enumerate(pred_objects):
            iou = compute_iou(gt_obj['bbox'], pred_obj['bbox'])
            iou_matrix[g_idx, p_idx] = iou
    
    # Greedy matching: match best IoU pairs first
    matched_pairs = []
    while True:
        # Find best unmatched pair
        best_iou = iou_threshold
        best_g_idx = -1
        best_p_idx = -1
        
        for g_idx in unmatched_gt:
            for p_idx in unmatched_pred:
                if iou_matrix[g_idx, p_idx] > best_iou:
                    best_iou = iou_matrix[g_idx, p_idx]
                    best_g_idx = g_idx
                    best_p_idx = p_idx
        
        if best_g_idx == -1:
            break
        
        matches.append((best_g_idx, best_p_idx, best_iou))
        unmatched_gt.remove(best_g_idx)
        unmatched_pred.remove(best_p_idx)
    
    return matches, unmatched_gt, unmatched_pred


def compute_mota(gt_data, pred_data, iou_threshold=0.5):
    """
    Compute Multiple Object Tracking Accuracy (MOTA).
    
    MOTA = 1 - (FN + FP + IDSW) / GT
    
    Where:
        FN = False Negatives (unmatched ground truth)
        FP = False Positives (unmatched predictions)
        IDSW = ID Switches (ID changes for same object across frames)
        GT = Total ground truth objects
    
    Args:
        gt_data: dict from load_ground_truth
        pred_data: dict from load_predictions
        iou_threshold: minimum IoU to consider a match
    
    Returns:
        dict with MOTA and detailed metrics
    """
    all_frames = set(gt_data.keys()) | set(pred_data.keys())
    
    total_gt = 0; total_fn = 0 ; total_fp = 0  ; total_idsw = 0 
    
    # Track ID mappings across frames for ID switch detection
    gt_id_to_pred_id = defaultdict(set)  # Maps gt_id to set of pred_ids seen
    
    for frame in sorted(all_frames):
        gt_objects = gt_data.get(frame, [])
        pred_objects = pred_data.get(frame, [])
        
        total_gt += len(gt_objects)
        
        # Match detections
        matches, unmatched_gt, unmatched_pred = match_detections(
            gt_objects, pred_objects, iou_threshold
        )
        
        total_fn += len(unmatched_gt)
        total_fp += len(unmatched_pred)
        
        # Count ID switches
        for gt_idx, pred_idx, _ in matches:
            gt_id = gt_objects[gt_idx]['id']
            pred_id = pred_objects[pred_idx]['id']
            gt_id_to_pred_id[gt_id].add(pred_id)
        
        # ID switches = number of different pred_ids for each gt_id - 1
        for gt_id, pred_ids in gt_id_to_pred_id.items():
            if len(pred_ids) > 1:
                total_idsw += len(pred_ids) - 1
    
    # Compute MOTA
    if total_gt == 0:
        mota = 0.0
    else:
        mota = 1.0 - (total_fn + total_fp + total_idsw) / total_gt
    
    return {
        'MOTA': mota,
        'FN': total_fn,
        'FP': total_fp,
        'IDSW': total_idsw,
        'GT': total_gt,
        'Precision': (total_gt - total_fp) / (total_gt - total_fp + total_fp) if (total_gt - total_fp + total_fp) > 0 else 0,
        'Recall': (total_gt - total_fn) / total_gt if total_gt > 0 else 0
    }


def evaluate_sequences(data_dir, gt_base_dir):
    """    
    Args:
        data_dir: directory with prediction txt files (e.g., ../data_test)
        gt_base_dir: base directory with gt files (e.g., ../evs_mot-train)
    
    Returns:
        dict with evaluation results for each sequence
    """
    results = {}
    
    # Find all txt files in data_dir
    if not os.path.exists(data_dir):
        print(f"Error: {data_dir} does not exist")
        return results
    
    pred_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    
    for pred_file in sorted(pred_files):
        sequence_name = pred_file.replace('.txt', '')
        pred_path = os.path.join(data_dir, pred_file)
        gt_path = os.path.join(gt_base_dir, sequence_name, 'gt', 'gt.txt')
        
        # Load data
        pred_data = load_predictions(pred_path)
        gt_data = load_ground_truth(gt_path)
        
        # Compute MOTA
        metrics = compute_mota(gt_data, pred_data)
        results[sequence_name] = metrics
        
        print(f"\n{sequence_name}:")
        print(f"  MOTA:      {metrics['MOTA']:.2%}")
        print(f"  Recall:    {metrics['Recall']:.2%}")
        print(f"  Precision: {metrics['Precision']:.2%}")
        print(f"  FN:        {metrics['FN']} (False Negatives)")
        print(f"  FP:        {metrics['FP']} (False Positives)")
        print(f"  IDSW:      {metrics['IDSW']} (ID Switches)")
    
    # Calculate average MOTA
    if results:
        avg_mota = np.mean([r['MOTA'] for r in results.values()])
        print(f"\n{'='*40}")
        print(f"Average MOTA: {avg_mota:.2%}")
        print(f"{'='*40}")
        results['AVERAGE'] = {'MOTA': avg_mota}
    
    return results
