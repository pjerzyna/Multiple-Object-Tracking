Do tego problemu zastosowano podejście:

SORT (Simple Online Realtime Tracking)
1. inicjalizacja tracków
2. dopasowanie detekcji do tracków
3. przewidywanie pozycji
4. usuwanie tracków
5. obsługa nowych tracków

SORT = Filtr_Kalmana + Metoda Węgierska
- każdy obiekt posiada pozycję i prędkość:
  state = [x, y, h, w, vx, vy] 
pipeline:
1) Filtr Kalmana --> predict next position
2) liczenie IoU --> track bbox vs detection bbox
3) Metoda Węgierska --> dopasowanie pomiędzy detections a tracks
4) analiza tracku:
matched --> update Kalman filter
unmatched detection --> create new track
unmatched track --> increase age
age > threshold --> delete track

Matching function (większy overlap--> mniejszy match): cost = 1 - IoU

Struktura kodu:
source/
dataset.py           det.txt --> dict[int frame_id] = list[detections]
tracker.py
track.py
kalman_filter.py
association.py
iou.py
main.py
evaluation.py
visualization.py