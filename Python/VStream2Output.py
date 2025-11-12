import cv2
import socket

CAM_URL = "http://192.168.4.1/stream"

UDP_IP = "192.168.4.255"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

cap = cv2.VideoCapture(CAM_URL)
if not cap.isOpened():
    print("Cannot open stream")
    exit(1)

print("Stream connected")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # zmenši pre rýchlosť
    frame = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # detekcia tmavších objektov (prekážky)
    _, thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)

    # nájdi kontúry
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    direction = "FORWARD"

    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area > 500:  # len ak je dosť veľká prekážka
            x, y, w, h = cv2.boundingRect(largest)
            cx = x + w // 2

            # zakresli obrys
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.line(frame, (cx, 0), (cx, 240), (255, 0, 0), 2)

            # rozhodovanie
            if cx < 120:
                direction = "RIGHT"   # prekážka vľavo → otoč doprava
            elif cx > 200:
                direction = "LEFT"    # prekážka vpravo → otoč doľava
            else:
                direction = "STOP"

    # pošli smer cez UDP
    sock.sendto(direction.encode(), (UDP_IP, UDP_PORT))
    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Obstacle Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
