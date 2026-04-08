import argparse
from dataset import load_detections, load_seqinfo
from iou import compute_iou
from tracker import MultiObjectTracker

# Narazie dla testow czy dziala jako tako, operuje na jednym pliku zrodlowym MOT_01
PATH_MOT1_DET_TEST = "evs_mot-test/MOT_01/det/det.txt"
PATH_IMG1_TEST = "evs_mot-test/MOT_01/img1/"
PATH_SEQINFO_TEST = "evs_mot-test/MOT_01/seqinfo.ini"


parser = argparse.ArgumentParser(description="MOT dataset parser")
parser.add_argument(
    "--mode",
    choices=["det", "seqinfo", "iou", "tracker"],
    required=True
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
        detections = load_detections(PATH_MOT1_DET_TEST)
        tracker = MultiObjectTracker()

        # testowa sciezka wynikkwa
        output_path = "test.txt"

        with open(output_path, "w") as f:
            for frame in sorted(detections.keys()):
                tracker.update(detections[frame])
                
                for track_id, bbox in tracker.get_tracked_objects():
                    # Format: frame, id, x, y, w, h, conf, class, visibility, unused
                    # Zgodnie z poleceniem: <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,1,-1,-1,-1
                    line = f"{frame},{track_id},{bbox[0]:.2f},{bbox[1]:.2f},{bbox[2]:.2f},{bbox[3]:.2f},1,-1,-1,-1\n"
                    f.write(line)
                    # print(line.strip()) # Opcjonalnie do podglądu w konsoli
        
        print(f"Przetwarzanie zakończone. Wynik zapisany w {output_path}")