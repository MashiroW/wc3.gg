import scapy.all as scapy

def sniff_on_port(port):
    # Define the capture filter
    capture_filter = f"port {port}"

    # Start sniffing
    captured_packets = scapy.sniff(filter=capture_filter, count=70)

    # Print captured packets and their payloads
    for packet in captured_packets:
        print(f"Packet Summary: {packet.summary()}")
        
        # Check if the packet has a payload
        if packet.haslayer(scapy.Raw):
            # Extract and print the payload
            payload = packet[scapy.Raw].load
            print(f"Payload: {payload.hex()}")  # Prints the payload in hexadecimal format

        print("=" * 40)

# Replace <your_port_number> with the actual port you want to sniff
sniff_on_port(23775)