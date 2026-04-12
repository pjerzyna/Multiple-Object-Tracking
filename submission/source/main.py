import argparse
import os
import glob
from dataset import load_detections, load_seqinfo
from iou import compute_iou
from tracker import MultiObjectTracker
from evaluation import evaluate_sequences
from visualization import visualize_dataset_sequence

# Narazie dla testow czy dziala jako tako, operuje na jednym pliku zrodlowym MOT_01
PATH_MOT1_DET_TEST = "../evs_mot-test/MOT_01/det/det.txt"
PATH_IMG1_TEST = "../evs_mot-test/MOT_01/img1/"
PATH_SEQINFO_TEST = "../evs_mot-test/MOT_01/seqinfo.ini"


parser = argparse.ArgumentParser(description="MOT dataset parser")
parser.add_argument(
    "--mode",
    choices=["det", "seqinfo", "iou", "tracker", "single_tracker", "test_tracker", "evaluation", "visualization"],
    required=True
)
parser.add_argument(
    "--sequence",
    type=str,
    default="MOT_02",
    help="Sequence to visualize (default: MOT_02). Examples: MOT_01, MOT_02, MOT_03, etc."
)
parser.add_argument(
    "--data-dir",
    type=str,
    default="../data_test",
    help="Directory with tracking results (default: ../data_test)"
)
parser.add_argument(
    "--output-video",
    type=str,
    default=None,
    help="Optional path to save output video (e.g., ../output.mp4)"
)
args = parser.parse_args()



if __name__ == "__main__":
    # Narazie to testowanie poszczególnych funkcji i klas mozna zostawic tak, ale pozniej wypadaloby to uporzadkowac
    if args.mode == "det":
        # Przetestowanie parsowania danych z det.txt
        detections = load_detections(PATH_MOT1_DET_TEST)

        print("Frame 1 detections:")
        print(detections[1])



    elif args.mode == "seqinfo":
        # Przetestowanie parsowania danych z seqinfo.ini
        seqinfo = load_seqinfo(PATH_SEQINFO_TEST)

        print(seqinfo)



    elif args.mode == "iou":
        # Przetestowanie funkcji compute_iou (0 < IoU < 1)

        # wynik = A + B - czesc wspolna
        box1 = [100, 100, 50, 80]
        box2 = [110, 120, 50, 80]

        print("IoU:", compute_iou(box1, box2))

    elif args.mode == "tracker":
        # Ensure data directory exists
        os.makedirs("../data", exist_ok=True)
        
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
            
            output_path = f"../data/{dataset_name}.txt"

            with open(output_path, "w") as f:
                for frame in sorted(detections.keys()):
                    tracker.update(detections[frame])
                    
                    for track_id, bbox in tracker.get_tracked_objects():
                        # Format: frame, id, x, y, w, h, conf, class, visibility, unused
                        # Zgodnie z poleceniem: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,1,-1,-1,-1
                        line = f"{frame},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1\n"
                        f.write(line)
            
            print(f"✓ {dataset_name} - Wynik zapisany w {output_path}")
        
        print("Przetwarzanie wszystkich zbiorów danych zakończone.")

    elif args.mode == "single_tracker":
        # Ensure data directory exists
        os.makedirs("../data", exist_ok=True)
        
        # Extract dataset name from the path (e.g., "MOT_01" from "evs_mot-test/MOT_01/det/det.txt")
        dataset_name = PATH_MOT1_DET_TEST.split('/')[2]
        
        print(f"Processing {dataset_name}...")
        
        detections = load_detections(PATH_MOT1_DET_TEST)
        tracker = MultiObjectTracker()
        
        output_path = f"../data/{dataset_name}.txt"

        with open(output_path, "w") as f:
            for frame in sorted(detections.keys()):
                tracker.update(detections[frame])
                
                for track_id, bbox in tracker.get_tracked_objects():
                    # Format: frame, id, x, y, w, h, conf, class, visibility, unused
                    # Zgodnie z poleceniem: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,1,-1,-1,-1
                    line = f"{frame},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1\n"
                    f.write(line)
        
        print(f"✓ {dataset_name} - Wynik zapisany w {output_path}")

    elif args.mode == "test_tracker":
        # Ensure data_test directory exists
        os.makedirs("../data_test", exist_ok=True)
        
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
            
            output_path = f"../data_test/{dataset_name}.txt"

            with open(output_path, "w") as f:
                for frame in sorted(detections.keys()):
                    tracker.update(detections[frame])
                    
                    for track_id, bbox in tracker.get_tracked_objects():
                        # Format: frame, id, x, y, w, h, conf, class, visibility, unused
                        # Zgodnie z poleceniem: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,1,-1,-1,-1
                        line = f"{frame},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1\n"
                        f.write(line)
            
            print(f"✓ {dataset_name} - Wynik zapisany w {output_path}")
        
        print("Przetwarzanie wszystkich danych treningowych zakończone.")

    elif args.mode == "evaluation":
        # Evaluate test_tracker results using MOTA metric
        print("Evaluating tracker results using MOTA metric...\n")
        
        data_test_dir = "../data_test"
        gt_base_dir = "../evs_mot-train"
        
        evaluate_sequences(data_test_dir, gt_base_dir)

    elif args.mode == "visualization":
        # Visualize tracking results
        print("Visualizing tracking results...\n")
        
        sequence_name = args.sequence
        data_dir = args.data_dir
        gt_base_dir = "../evs_mot-train"
        img_base_dir = "../evs_mot-train"
        output_video = args.output_video
        
        visualize_dataset_sequence(sequence_name, data_dir, gt_base_dir, img_base_dir, output_video)