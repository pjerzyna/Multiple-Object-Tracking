import argparse
from dataset import load_detections, load_seqinfo
from iou import compute_iou

PATH_MOT1_DET_TEST = "evs_mot-test/MOT_01/det/det.txt"
PATH_IMG1_TEST = "evs_mot-test/MOT_01/img1/"
PATH_SEQINFO_TEST = "evs_mot-test/MOT_01/seqinfo.ini"


parser = argparse.ArgumentParser(description="MOT dataset parser")
parser.add_argument(
    "--mode",
    choices=["det", "seqinfo", "iou"],
    required=True
)
args = parser.parse_args()




if __name__ == "__main__":
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
        # Przetestowanie funkcji compute_iou

        # Zamiast takich smiesznych flag, to dodac moze pytesty?!?!?
        box1 = [100, 100, 50, 80]
        box2 = [110, 120, 50, 80]

        print("IoU:", compute_iou(box1, box2))