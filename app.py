from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import scapy.all as scapy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def scan_network():
    arp = scapy.ARP(pdst="192.168.1.0/24")  # adjust subnet if needed
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    answered = scapy.srp(broadcast / arp, timeout=2, verbose=False)[0]

    devices = []
    for _, recv in answered:
        devices.append({
            "ip": recv.psrc,
            "mac": recv.hwsrc
        })
    return devices

@app.get("/devices")
def devices():
    return scan_network()
