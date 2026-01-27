import scapy.all as scapy
import threading
from services.deviceServices import device_cache, cache_lock

# Global session tracking: device_id -> set of session keys
device_sessions = {}

def packet_handler(packet):
    try:
        if not packet.haslayer(scapy.Ether):
            return

        src_mac = packet[scapy.Ether].src.lower()
        dst_mac = packet[scapy.Ether].dst.lower()
        size = len(packet)

        src_ip = packet[scapy.IP].src if packet.haslayer(scapy.IP) else None
        dst_ip = packet[scapy.IP].dst if packet.haslayer(scapy.IP) else None

        # Skip if no IP info (can't track sessions without IP)
        if not src_ip or not dst_ip:
            return

        # Protocol and ports for session keys
        protocol = packet[scapy.IP].proto
        if packet.haslayer(scapy.TCP):
            src_port = packet[scapy.TCP].sport
            dst_port = packet[scapy.TCP].dport
        elif packet.haslayer(scapy.UDP):
            src_port = packet[scapy.UDP].sport
            dst_port = packet[scapy.UDP].dport
        else:
            # Other protocols: treat ports as None
            src_port = None
            dst_port = None

        # Compose device keys
        src_key = f"{src_ip}_{src_mac}"
        dst_key = f"{dst_ip}_{dst_mac}"

        # Create a bidirectional session key (IPs and ports sorted)
        ip_pair = tuple(sorted([src_ip, dst_ip]))
        port_pair = tuple(sorted([src_port, dst_port])) if src_port and dst_port else (None, None)
        session_key = (ip_pair, protocol, port_pair)

        with cache_lock:
            # Update packet and byte counts for source device
            if src_key in device_cache:
                dev = device_cache[src_key]
                dev["bytes_sent"] += size
                dev["packets_sent"] += 1

                # Initialize sessions set if missing
                if src_key not in device_sessions:
                    device_sessions[src_key] = set()
                # Add session key if new
                if session_key not in device_sessions[src_key]:
                    device_sessions[src_key].add(session_key)
                dev["sessions"] = len(device_sessions[src_key])

            # Update packet and byte counts for destination device
            if dst_key in device_cache:
                dev = device_cache[dst_key]
                dev["bytes_recv"] += size
                dev["packets_recv"] += 1

                # Initialize sessions set if missing
                if dst_key not in device_sessions:
                    device_sessions[dst_key] = set()
                # Add session key if new
                if session_key not in device_sessions[dst_key]:
                    device_sessions[dst_key].add(session_key)
                dev["sessions"] = len(device_sessions[dst_key])

    except Exception as e:
        print("Packet handler error:", e)


def start_sniffer(interface=None):
    print(f"Sniffer started on interface: {interface}")
    scapy.sniff(
        iface=interface,
        prn=packet_handler,
        store=False,
        promisc=True
    )


def start_traffic_sniffer(interface=None):
    threading.Thread(
        target=start_sniffer,
        kwargs={"interface": interface},
        daemon=True
    ).start()
