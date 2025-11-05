import cv2
import numpy as np
import socket

# IP kamery v AP mode
CAM_URL = "http://192.168.4.1/stream"

# UDP konfigurácia (kam sa pošle výsledok)
UDP_IP = "192.168.4.255"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

cap = cv2.VideoCapture(CAM_URL)

if not cap.isOpened():
    print("Nepodarilo sa otvoriť stream")
    exit(1)

print("Stream pripojený")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Žiadny frame, čakám...")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    msg = f"Brightness:{brightness:.2f}"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    print(msg)

    cv2.imshow("ESP32CAM Stream", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC -> ukonči
        break

cap.release()
cv2.destroyAllWindows()
