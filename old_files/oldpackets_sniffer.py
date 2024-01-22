import socket
import re
import json
import pandas as pd
import threading
from queue import Queue
from dataframe_manager import process_leaderboard_data_and_save

# Global DataFrame to store data
data_lock = threading.Lock()
packet_queue = Queue()

def extract_specific_json(decoded_packet):
    match = re.search(r'\{.*\}', decoded_packet)
    if match:
        json_part = match.group()
        try:
            json_data = json.loads(json_part)
            if 'messageType' in json_data and json_data['messageType'] == 'UpdateLeaderboardData':
                return json_data
        except json.JSONDecodeError:
            pass
    return None

def process_packet(hex_packet):
    try:
        decoded_packet = bytes.fromhex(hex_packet.hex()).decode('utf-8', errors='replace')
        specific_json = extract_specific_json(decoded_packet)
        if specific_json:
            with data_lock:
                process_leaderboard_data_and_save(json_data=specific_json)

            print("--------DATA INSERTED----------")
        else:
            pass
    except UnicodeDecodeError:
        print("Unable to decode as UTF-8. Printing raw hex:")
        print(hex_packet)

def packet_capture_thread(sock, packet_queue):
    while True:
        pkt, _ = sock.recvfrom(65535)
        packet_queue.put(pkt)

def packet_processing_thread(packet_queue):
    while True:
        pkt = packet_queue.get()
        process_packet(pkt)
        packet_queue.task_done()

def packet_sniffer(selected_interface='127.0.0.1', num_capture_threads=1, num_processing_threads=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sock.bind((selected_interface, 0))
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # Start the packet capture threads
    capture_threads = []
    for _ in range(num_capture_threads):
        capture_thread = threading.Thread(target=packet_capture_thread, args=(sock, packet_queue), daemon=True)
        capture_threads.append(capture_thread)
        capture_thread.start()

    # Start the packet processing threads
    processing_threads = []
    for _ in range(num_processing_threads):
        processing_thread = threading.Thread(target=packet_processing_thread, args=(packet_queue,), daemon=True)
        processing_threads.append(processing_thread)
        processing_thread.start()

    try:
        print("Sniffer starting")
        # Wait for the packet capture threads to finish
        for capture_thread in capture_threads:
            capture_thread.join()
        # Wait for the processing threads to finish
        for processing_thread in processing_threads:
            processing_thread.join()
    except KeyboardInterrupt:
        # Turn off promiscuous mode on KeyboardInterrupt
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == "__main__":
    packet_sniffer(num_capture_threads=100, num_processing_threads=40)

