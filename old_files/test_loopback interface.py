import socket
import struct

def extract_ips_and_payload(packet):
    eth_header_length = 14
    ip_start = eth_header_length + 12

    # Check if the packet is at least as long as the expected IP header length
    if len(packet) < ip_start + 20:
        print("Incomplete packet received.")
        return None

    src_mac = packet[6:12]
    dst_mac = packet[0:6]
    src_ip = struct.unpack("!4B", packet[ip_start + 12:ip_start + 16])
    dst_ip = struct.unpack("!4B", packet[ip_start + 16:ip_start + 20])

    src_ip_decimal = '.'.join(str(byte) for byte in src_ip)
    dst_ip_decimal = '.'.join(str(byte) for byte in dst_ip)

    # Parse the IP header to get the protocol number
    ip_header = packet[ip_start:ip_start + 20]
    protocol = struct.unpack("!B", ip_header[9:10])[0]

    if protocol == 6:  # TCP protocol
        tcp_start = ip_start + (struct.unpack("!B", ip_header[0:1])[0] & 0x0F) * 4
        src_port, dst_port = struct.unpack("!HH", packet[tcp_start:tcp_start + 4])
        payload = packet[tcp_start + 4:]

        return src_mac, dst_mac, src_ip_decimal, dst_ip_decimal, src_port, dst_port, payload, protocol

    else:
        print("Non-TCP packet received.")
        return src_mac, dst_mac, src_ip_decimal, dst_ip_decimal, None, None, None, protocol

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
        data = extract_ips_and_payload(pkt)
        if data is not None:
            src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port, payload, protocol = data
            print("Source MAC: {}, Destination MAC: {}".format(src_mac.hex(), dst_mac.hex()))
            print("Source IP: {}, Destination IP: {}".format(src_ip, dst_ip))
            print("Source Port: {}, Destination Port: {}".format(src_port, dst_port))
            print("Protocol: {}".format(protocol))
            
            if protocol == 6:  # TCP
                print("Payload: {}\n".format(payload.hex()))
            else:
                print("Non-TCP Packet\n")

except KeyboardInterrupt:
    # Turn off promiscuous mode on KeyboardInterrupt
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
