import cv2 as cv
import time
import os
import connect as cnt
import pygame

DEBUG_MODE = False

def videoLoop():
    while True and not DEBUG_MODE:
        response = os.system(f"ping -c 1 {cnt.CAM_IP} > /dev/null 2>&1")
        if response == 0:
            print("ESP32-CAM online")
            break
        print(".", end="")
        time.sleep(1)

    cap = cv.VideoCapture(0 if DEBUG_MODE else cnt.CAM_URL)
    if not cap.isOpened():
        print("Cannot open camera")
        exit(1)

    pygame.init()
    _ = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Vehicle Control")

    clock = pygame.time.Clock()
    running = True

    cap.set(cv.CAP_PROP_BUFFERSIZE, 1)

    last_send = 0

    while running:
        for _ in range(2):
            cap.read()

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.resize(frame, (320, 240))
        cv.imshow("ESP32CAM", frame)
        cv.waitKey(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            val = 511
        elif keys[pygame.K_d]:
            val = 1
        elif keys[pygame.K_w]:
            val = 256
        else:
            cnt.badUDP()
            clock.tick(60)
            continue

        if time.time() - last_send > 0.02:
            cnt.sendUDP(val)
            last_send = time.time()

        clock.tick(60)

    pygame.quit()
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    try:
        cnt.startHotspot()
        time.sleep(2)

        videoLoop()
    finally:
        cnt.stopHotspot()
