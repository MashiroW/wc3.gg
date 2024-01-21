import socket
import re
import json  # Added import for JSON parsing

def extract_specific_json(decoded_packet):
    # Use a regular expression to find JSON-like strings in the packet
    match = re.search(r'\{.*\}', decoded_packet)
    if match:
        json_part = match.group()
        try:
            json_data = json.loads(json_part)
            # Check if the JSON has the desired messageType
            if 'messageType' in json_data and json_data['messageType'] == 'UpdateLeaderboardData':
                return json_data
        except json.JSONDecodeError:
            pass  # Ignore JSON decoding errors
    return None

def process_packet(hex_packet):
    try:
        decoded_packet = bytes.fromhex(hex_packet.hex()).decode('utf-8', errors='replace')
        specific_json = extract_specific_json(decoded_packet)
        if specific_json:
            print(specific_json)
        else:
            print("No valid JSON with 'messageType':'UpdateLeaderboardData' found in the packet.")
    except UnicodeDecodeError:
        print("Unable to decode as UTF-8. Printing raw hex:")
        print(hex_packet)

# Use loopback address directly
selected_interface = '127.0.0.1'

# Create a socket to capture packets
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
sock.bind((selected_interface, 0))

# Set promiscuous mode
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        pkt, _ = sock.recvfrom(65535)
        process_packet(pkt)
        print("---------------------------")

except KeyboardInterrupt:
    # Turn off promiscuous mode on KeyboardInterrupt
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
