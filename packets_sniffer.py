import pyshark
import psutil
import json
import time
from dataframe_manager import *

def get_pid_by_name(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    return None

def get_ports_by_pid(pid):
    try:
        connections = psutil.Process(pid).connections()
        # Extract listening ports from connections
        listening_ports = [conn.laddr.port for conn in connections if conn.status == psutil.CONN_LISTEN]
        return listening_ports
    except psutil.NoSuchProcess:
        return []

def decode_hex_payload(hex_payload):
    # Remove colons and convert the modified hex_payload to bytes
    byte_payload = bytes.fromhex(hex_payload.replace(":", ""))

    # Decode the bytes to a string using UTF-8 encoding
    decoded_payload = byte_payload.decode('utf-8')

    return decoded_payload

def packet_callback(pkt):

    if 'IP' in pkt and 'TCP' in pkt:
        #source_port = pkt.tcp.srcport
        #print(f"Source Port: {source_port}")

        try:
            payload = json.loads(decode_hex_payload(pkt.tcp.payload))
            save_to_json(json_data=payload)
            #process_leaderboard_data_and_save(json_data=payload)
            print("Saved packet !")

        except:
            pass
    else:
        print("No TCP layer found in the packet.")

def sniff_packets(interface='Adapter for loopback traffic capture', source_ports=None):
    if source_ports is None:
        source_ports = []

    # Convert all source_ports to strings
    source_ports = list(map(str, source_ports))

    # Construct the BPF filter for multiple source ports
    bpf_filter = 'tcp src port ' + ' or '.join(source_ports)

    capture = pyshark.LiveCapture(interface=interface, bpf_filter=bpf_filter)
    capture.apply_on_packets(packet_callback, packet_count=0)

if __name__ == "__main__":

    process_name = "Warcraft III.exe"

    # Wait for the process to start
    while True:
        pid = get_pid_by_name(process_name)
        if pid is not None:
            print("Warcraft III process found. PID:", pid)
            break
        else:
            print("Waiting for Warcraft III process to start...")
            time.sleep(1)

    # Get the initial ports
    ports = get_ports_by_pid(pid)
    print("Initial Warcraft III ports in use:", ports)

    # Start sniffing packets
    stop_capturing = False
    sniff_packets(source_ports=ports)

    # Keep the program running until the process exits
    while psutil.pid_exists(pid):
        time.sleep(1)

    print("Warcraft III process has exited. Stopping packet sniffing.")
    stop_capturing = True