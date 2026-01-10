import socket

CAM_URL = "http://192.168.4.1/stream"

UDP_IP = "192.168.4.255"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def sendUDP(direction: str):
    sock.sendto(direction.encode(), (UDP_IP, UDP_PORT))
