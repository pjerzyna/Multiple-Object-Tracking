"""
Multiple Object Tracking (MOT) - Main Entry Point

This module provides the main command-line interface for the SORT tracking algorithm.
Supports multiple modes: tracking, evaluation, visualization, and component testing.
"""

# !!! Kalman to chyba w nim jest problem z odlatywaniem ramek !!!

import argparse
import os
import glob
from dataset import load_detections
from tracker import MultiObjectTracker
from evaluation import evaluate_sequences
from visualization import visualize_dataset_sequence


parser = argparse.ArgumentParser(
    description="MOT dataset parser",
    epilog="""
Modes:
  tracker          - Process all test sequences (MOT_01, MOT_06, MOT_07)
  single_tracker   - Process single test sequence (MOT_01)
  train_tracker    - Process all training sequences (MOT_02-05) for validation
  evaluation       - Evaluate results using MOTA metric
  visualization    - Visualize tracking results on video frames

Examples:
  python main.py --mode tracker
  python main.py --mode single_tracker
  python main.py --mode train_tracker
  python main.py --mode evaluation
  python main.py --mode visualization --sequence MOT_02
  python main.py --mode visualization --sequence MOT_01 --output-video output.mp4
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument(
    "--mode",
    choices=["tracker", "single_tracker", "train_tracker", "evaluation", "visualization"],
    required=True,
    help="Operation mode to execute"
)
parser.add_argument(
    "--sequence",
    type=str,
    default="MOT_02",
    help="Sequence name for visualization (e.g., MOT_01, MOT_02, MOT_06)"
)
parser.add_argument(
    "--data-dir",
    type=str,
    default="../data_train",
    help="Directory with tracking results (default: ../data_train)"
)
parser.add_argument(
    "--output-video",
    type=str,
    default=None,
    help="Optional path to save output video (e.g., ../output.mp4)"
)
args = parser.parse_args()



if __name__ == "__main__":
    if args.mode == "tracker":
        # Ensure data directory exists
        os.makedirs("../data_test", exist_ok=True)
        
        # Find all MOT_* directories in evs_mot-test
        mot_dirs = sorted(glob.glob("../evs_mot-test/MOT_*"))
        
        for mot_dir in mot_dirs:
            dataset_name = os.path.basename(mot_dir)  # Extract "MOT_01", "MOT_06", etc.
            
            det_path = f"{mot_dir}/det/det.txt"
            
            # Check if det.txt exists
            if not os.path.exists(det_path):
                print(f"Warning: {det_path} not found, skipping {dataset_name}")
                continue
            
            print(f"Processing {dataset_name}...")
            
            detections = load_detections(det_path)
            tracker = MultiObjectTracker()
            
            output_path = f"../data_test/{dataset_name}.txt"

            with open(output_path, "w") as f:
                for frame in sorted(detections.keys()):
                    tracker.update(detections[frame])
                    
                    for track_id, bbox in tracker.get_tracked_objects():
                        # Format: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,1,-1,-1,-1
                        line = f"{frame},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1\n"
                        f.write(line)
            
            print(f"✓ {dataset_name} - Result is saved at {output_path}")
        
        print("Processing of the data is done.")

    elif args.mode == "single_tracker":
        # Ensure data directory exists
        os.makedirs("../data_test", exist_ok=True)
        
        # Extract dataset name from the path (e.g., "MOT_01" from "evs_mot-test/MOT_01/det/det.txt")
        PATH_MOT1_DET_TEST = "../evs_mot-test/MOT_01/det/det.txt"
        dataset_name = PATH_MOT1_DET_TEST.split('/')[2]
        
        print(f"Processing {dataset_name}...")
        
        detections = load_detections(PATH_MOT1_DET_TEST)
        tracker = MultiObjectTracker()
        
        output_path = f"../data_test/{dataset_name}.txt"

        with open(output_path, "w") as f:
            for frame in sorted(detections.keys()):
                tracker.update(detections[frame])
                
                for track_id, bbox in tracker.get_tracked_objects():
                    # Format: frame, id, x, y, w, h, conf, class, visibility, unused
                    #<detection_confidence> - miara pewności detektora co do detekcji (w zakresie 0 - 1)
                    #<eval_flag> - flaga informująca, czy dany obiekt jest traktowany jako wzorcowy i powinien być brany pod uwagę w ewaluacji (0 - nie, 1 - tak)
                    #<class> - klasa obiektu, interesuje nas klasa 1, czyli sylwetki ludzi, którzy nie są wewnątrz budynków i nie są odbiciami (np w szybach budynków/samochodów).
                    #<visibility> - liczba w zakresie (0 - 1] informująca, jaka część obiektu jest widoczna w danej klatce
                    line = f"{frame},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1\n"
                    f.write(line)
        
        print(f"✓ {dataset_name} - Result saved at {output_path}")

    elif args.mode == "train_tracker":
        # Ensure data_test directory exists
        os.makedirs("../data_train", exist_ok=True)
        
        # Find all MOT_* directories in evs_mot-train
        mot_dirs = sorted(glob.glob("../evs_mot-train/MOT_*"))
        
        for mot_dir in mot_dirs:
            dataset_name = os.path.basename(mot_dir)  # Extract "MOT_02", "MOT_03", etc.
            
            det_path = f"{mot_dir}/det/det.txt"
            
            # Check if det.txt exists
            if not os.path.exists(det_path):
                print(f"Warning: {det_path} not found, skipping {dataset_name}")
                continue
            
            print(f"Processing {dataset_name}...")
            
            detections = load_detections(det_path)
            tracker = MultiObjectTracker()
            
            output_path = f"../data_train/{dataset_name}.txt"

            with open(output_path, "w") as f:
                for frame in sorted(detections.keys()):
                    tracker.update(detections[frame])
                    
                    for track_id, bbox in tracker.get_tracked_objects():
                        # Format: frame, id, x, y, w, h, conf, class, visibility, unused
                        # Zgodnie z poleceniem: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,1,-1,-1,-1
                        line = f"{frame},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1\n"
                        f.write(line)
            
            print(f"✓ {dataset_name} - Result saved at {output_path}")
        
        print("Processing of the data is done.")

    elif args.mode == "evaluation":
        # Evaluate test_tracker results using MOTA metric
        print("Evaluating tracker results using MOTA metric...\n")
        
        data_test_dir = "../data_train"
        gt_base_dir = "../evs_mot-train"
        
        evaluate_sequences(data_test_dir, gt_base_dir)

    elif args.mode == "visualization":
        print(f"Visualizing tracking results for {args.sequence}...\n")
        seq = args.sequence
        
        # TEST dataset:
        if seq in ["MOT_01", "MOT_06", "MOT_07"]:
            data_dir = "../data_test"
            base_dir = "../evs_mot-test"
            gt_base_dir = None
        
        # TRAINING dataset: MOT_02, MOT_03, MOT_04, MOT_05
        else:
            data_dir = args.data_dir
            base_dir = "../evs_mot-train"
            gt_base_dir = "../evs_mot-train"

        img_base_dir = base_dir
        
        visualize_dataset_sequence(
            sequence_name=seq, 
            data_dir=data_dir, 
            gt_base_dir=gt_base_dir, 
            img_base_dir=img_base_dir, 
            output_video=args.output_video
        )