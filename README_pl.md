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

## Struktura projektu

```
Multiple-Object-Tracking/
├── source/                      # Wszystkie pliki źródłowe
│   ├── main.py                 # Główny skrypt
│   ├── dataset.py              # Parser det.txt --> dict[int frame_id] = list[detections]
│   ├── tracker.py              # Tracker wieloobiektowy
│   ├── track.py                # Klasa Track do śledzenia pojedynczego obiektu
│   ├── kalman_filter.py        # Implementacja filtra Kalmana
│   ├── association.py          # Dopasowanie detections <-> tracks
│   ├── iou.py                  # Funkcja Intersection over Union
│   ├── evaluation.py           # [Pusty] Do implementacji metryk ewaluacji
│   └── visualization.py        # [Pusty] Do implementacji wizualizacji
├── data/                        # Wyjściowe pliki z wynikami (.txt)
├── evs_mot-test/               # Dane testowe (MOT_01, MOT_06, MOT_07)
├── evs_mot-train/              # Dane treningowe (MOT_02-MOT_05)
└── codabench/                  # Dane konkursu
```

## Jak uruchomić?

Najpierw przejdź do katalogu `source`:
```bash
cd source
```

### Tryby działania:

1. **single_tracker** - przetwarzanie jednego zbioru danych (MOT_01)
   ```bash
   python main.py --mode single_tracker
   ```
   Wynik: `../data/MOT_01.txt`

2. **tracker** - przetwarzanie wszystkich zbiorów z `evs_mot-test`
   ```bash
   python main.py --mode tracker
   ```
   Wynik: `../data/MOT_01.txt`, `../data/MOT_06.txt`, `../data/MOT_07.txt`

3. **det** - test parsowania pliku det.txt
   ```bash
   python main.py --mode det
   ```

4. **seqinfo** - test parsowania pliku seqinfo.ini
   ```bash
   python main.py --mode seqinfo
   ```

5. **iou** - test funkcji IoU
   ```bash
   python main.py --mode iou
   ```

6. **test_tracker** - przetwarzanie danych treningowych do walidacji
   ```bash
   python main.py --mode test_tracker
   ```
   Wynik: `../data_test/MOT_02.txt`, `../data_test/MOT_03.txt`, `../data_test/MOT_04.txt`, `../data_test/MOT_05.txt`

7. **evaluation** - ewaluacja wyników z `test_tracker` przy użyciu metryki MOTA
   ```bash
   python main.py --mode evaluation
   ```
   Porównuje pliki z `../data_test/` z plikami ground truth z `../evs_mot-train/`

8. **visualization** - wizualizacja wyników śledzenia na klatkach wideo
   ```bash
   python main.py --mode visualization --sequence MOT_02
   ```
   
   Parametry opcjonalne:
   - `--sequence` - wybór sekwencji do wizualizacji (domyślnie: MOT_02)
   - `--data-dir` - katalog z wynikami śledzenia (domyślnie: ../data_test)
   - `--output-video` - ścieżka do zapisania wideo (np. ../output.mp4)
   
   Przykłady:
   ```bash
   # Wizualizuj MOT_03 (wyniki z data_test)
   python main.py --mode visualization --sequence MOT_03
   
   # Wizualizuj MOT_04 i zapisz do wideo
   python main.py --mode visualization --sequence MOT_04 --output-video ../result.mp4
   ```
   
   Sterowanie podczas wizualizacji:
   - **Spacja** - pauza/wznowienie
   - **Q** - wyjście

## Format wyjścia

Pliki wyjściowe w `data/` są w formacie MOT:
```
<frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,<confidence>,<class>,<visibility>,<unused>
```

Przykład:
```
1,1,123.45,234.56,50.00,80.00,1,-1,-1,-1
1,2,456.78,345.67,45.00,75.00,1,-1,-1,-1
2,1,125.00,236.00,50.00,80.00,1,-1,-1,-1
```

## Metryka MOTA (Multiple Object Tracking Accuracy)

MOTA = 1 - (FN + FP + IDSW) / GT

Gdzie:
- **FN** - False Negatives (liczba nieomytych obiektów ze wzorca)
- **FP** - False Positives (liczba fałszywych detekcji)
- **IDSW** - ID Switches (liczba zmian ID dla tego samego obiektu)
- **GT** - łączna liczba obiektów ze wzorca

Dodatkowe metryki:
- **Recall** - udział detekcji obiektów: (GT - FN) / GT
- **Precision** - precyzja detekcji: (GT - FP) / (GT - FP + FP)

## Workflow testowania

1. Uruchom test_tracker na danych treningowych:
   ```bash
   python main.py --mode test_tracker
   ```

2. Ewaluuj wyniki:
   ```bash
   python main.py --mode evaluation
   ```

3. Przeanalizuj wyniki i dostosuj parametry algorytmu jeśli potrzeba

4. Gdy jesteś zadowolony z wyników, uruchom tracker na danych testowych:
   ```bash
   python main.py --mode tracker
   ```

## Wizualizacja wyników

Po uruchomieniu trackera możesz zobaczyć wyniki w formie wideo:

```bash
# Wizualizuj wyniki z data_test dla MOT_02
python main.py --mode visualization --sequence MOT_02

# Wizualizuj i zapisz do pliku
python main.py --mode visualization --sequence MOT_03 --output-video ../MOT_03_tracked.mp4
```

### Cechy wizualizacji:

- ✅ Wyświetlanie oramiowane **obiekty śledzone** (identyfikatory z algorytmu)
- ✅ Porównanie z **ground truth** (cienkie ramki)
- ✅ Numery klatek
- ✅ Interaktywne sterowanie (pauza, wyjście)
- ✅ Opcja zapisania do pliku wideo

### Kolory w wizualizacji:

- **Grube ramki kolorowe** - wyniki śledzenia (tracking results)
- **Cienkie jasne ramki** - ground truth (punkty odniesienia)
- **ID: XXX** - identyfikator przypisany przez tracker

## Struktura kodu

```
source/
├── main.py              # Główny skrypt z wszystkimi modami
├── dataset.py           # Parser danych MOT
├── tracker.py           # Wieloobiektowy tracker (SORT)
├── track.py             # Klasa reprezentująca pojedynczy track
├── kalman_filter.py     # Filtr Kalmana dla predykcji
├── association.py       # Dopasowanie detections ↔ tracks (metoda węgierska)
├── iou.py               # Intersection over Union
├── evaluation.py        # MOTA metric i ewaluacja
└── visualization.py     # Wizualizacja wyników
```

## Algorytm: SORT (Simple Online Realtime Tracking)

Pipeline:
1. **Predykcja** - Filtr Kalmana przewiduje pozycję każdego tracku
2. **Asocjacja** - Metoda węgierska dopasowuje detekcje do tracków na podstawie IoU
3. **Update** - Dopasowane tracki są aktualizowane, nowe detekcje tworzą nowe tracki
4. **Zarządzanie** - Tracki bez detekcji przez >50 klatek są usuwane