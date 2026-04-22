# Autonómne riadenie malého vozidla s detekciou prekážky
Autor: Rudolf Tisoň


## 📌 Popis projektu
Tento projekt sa zameriava na autonómne riadenie malého vozidla pomocou počítačového videnia. Vozidlo dokáže sledovať jazdný pruh (čiaru) a zároveň detegovať prekážky v reálnom čase.

Na spracovanie obrazu sa využíva knižnica OpenCV a model YOLO, pričom riadenie vozidla zabezpečuje mikrokontrolér Arduino Nano ESP32 v kombinácii s kamerovým modulom ESP32-CAM.


## ⚙️ Použité technológie
🐍 Python

👁️ OpenCV

🤖 YOLO (You Only Look Once)

🔌 Arduino Nano ESP32

📷 ESP32-CAM


## 🚀 Funkcionalita
Detekcia jazdného pruhu (line following)

Detekcia prekážok pomocou YOLO

Rozhodovanie:

pokračovanie v jazde

zastavenie pri prekážke

Spracovanie obrazu v reálnom čase

Komunikácia medzi PC a mikrokontrolérom


## 🧠 Princíp fungovania
ESP32-CAM streamuje obraz do počítača

Python skript spracováva obraz:

OpenCV → detekcia jazdného pruhu

YOLO → detekcia prekážok

Na základe detekcie sa vypočíta:

- smer (steering)

- stav (jazda / stop)

Príkazy sa odošlú do Arduino Nano ESP32

Vozidlo reaguje na riadiace signály


## 🛠️ Inštalácia
1. Klonovanie repozitára
```bash
git clone https://github.com/ruddpj/BP-AutonomousVehicle.git
cd BP-AutonomousVehicle
```
2. Inštalácia závislostí
```bash
pip install opencv-python ultralytics numpy
```


## ▶️ Spustenie
```bash
python Python/main.py
```


## 🔌 Hardvér
- Arduino Nano ESP32

- ESP32-CAM + OV2640

- DRV8833

- HC-SR04

- 2x 3V 300RPM DC motory

- Buck menič nepätia

- Napájanie (batéria)


## 📂 Štruktúra projektu
```
.
├── Arduino/
├── Model/
├── Python/
├── Thesis/
├── .gitignore
├── LICENSE
├── README.md
└── yolov8n.pt
```


## 🎓 Účel projektu
Projekt bol vytvorený ako súčasť štúdia (bakalárska práca) a slúži na demonštráciu využitia počítačového videnia v autonómnych systémoch.


## 📜 Licencia
Tento projekt je licencovaný pod GNU GPL-3.0
