import subprocess
import socket

SSID = "LAPTOP_AP"
PASSWORD = "12345678"

CAM_IP = "10.42.0.128"
CAM_URL = "http://10.42.0.128:81/stream"

UDP_IP = "10.42.0.111"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
    message = str(int(direction * 255) + 1)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))


def badUDP():
    bad = "1000"
    sock.sendto(bad.encode(), (UDP_IP, UDP_PORT))
