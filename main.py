from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import scapy.all as scapy
import socket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def scan_network():
    local_ip = get_local_ip()
    subnet = local_ip.rsplit(".", 1)[0] + ".0/24"

    arp = scapy.ARP(pdst=subnet)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = scapy.srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc,
            "status": "online"
        })

    return devices

@app.get("/devices")
def get_devices():
    return {
        "devices": scan_network()
    }
