import subprocess
import socket
import struct
import os
import time

SSID = "LAPTOP_AP"
PASSWORD = "12345678"

CAM_IP = "10.42.0.128"
CAM_URL = "http://10.42.0.128:81/stream"

UDP_IP = "10.42.0.111"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def ping_cam():
    while True:
        response = os.system(f"ping -c 1 {CAM_IP} > /dev/null 2>&1")
        if response == 0:
            print("ESP32-CAM online")
            return
        print(".", end="")
        time.sleep(1)

def startHotspot():
    print("Starting Hotspot")
    subprocess.run([
        "nmcli",
        "device",
        "wifi",
        "hotspot",
        "ssid", SSID,
        "password", PASSWORD
    ], check=True)


def stopHotspot():
    print("Stopping Hotspot")
    subprocess.run([
        "nmcli",
        "connection",
        "down",
        "Hotspot-1",
    ], check=False)


def sendUDP(direction: float):
    sock.sendto(struct.pack('<H', direction), (UDP_IP, UDP_PORT))

