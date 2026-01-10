import cv2 as cv
import connect as cnt

cap = cv.VideoCapture(cnt.CAM_URL)
if not cap.isOpened():
    print("Cannot open stream")
    exit(1)

print("Stream connected")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # zmenši pre rýchlosť
    frame = cv.resize(frame, (320, 240))
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (7, 7), 0)

    # detekcia tmavších objektov (prekážky)
    _, thresh = cv.threshold(blurred, 80, 255, cv.THRESH_BINARY_INV)

    # nájdi kontúry
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    direction = "FORWARD"

    if contours:
        largest = max(contours, key=cv.contourArea)
        area = cv.contourArea(largest)

        if area > 500:  # len ak je dosť veľká prekážka
            x, y, w, h = cv.boundingRect(largest)
            cx = x + w // 2

            # zakresli obrys
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv.line(frame, (cx, 0), (cx, 240), (255, 0, 0), 2)

            # rozhodovanie
            if cx < 120:
                direction = "RIGHT"   # prekážka vľavo → otoč doprava
            elif cx > 200:
                direction = "LEFT"    # prekážka vpravo → otoč doľava
            else:
                direction = "STOP"

    # pošli smer cez UDP
    cnt.sendUDP(direction)
    cv.putText(frame, direction, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv.imshow("Obstacle Detection", frame)
    if cv.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv.destroyAllWindows()
