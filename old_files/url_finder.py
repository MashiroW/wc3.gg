import inspect
import psutil
import requests
import textwrap
from mitmproxy import http, ctx
from mitmproxy.tools.main import mitmdump
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_pid_and_ports(process_name):
    pid = None
    ports = []

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            pid = process.info['pid']
            break

    if pid is not None:
        try:
            connections = psutil.Process(pid).connections()
            ports = [conn.laddr.port for conn in connections]
        except psutil.NoSuchProcess as e:
            print(f"Error: {e}")
            return None, []

    return pid, ports

def find_webserver_port(ports, endpoint="/webui/Portraits/p111.png", timeout=5):
    for port in ports:
        print(port)
        url = f"http://127.0.0.1:{port}{endpoint}"
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                print(f"Port {port} is in use. URL: {url}")
                return port
            else:
                print(f"Port {port} is in use, but the response status code is {response.status_code}. URL: {url}")
        except requests.ConnectionError:
            # Connection error, the port is likely not in use
            print(f"Port {port} is not in use.")
        except requests.Timeout:
            # Request timed out
            print(f"Port {port} timed out. URL: {url}")

    print("Web server URL not found.")
    return None










if __name__ == "__main__":

    # Example usage:
    process_name = "Warcraft III.exe"  # Replace with the actual process name
    pid, ports = get_pid_and_ports(process_name)

    if pid is not None:
        print(f"PID: {pid}")
        print(f"Ports: {ports}")
    else:
        print(f"No process found with the name '{process_name}'.")


    target_port = find_webserver_port(ports=ports)
    print("Port: ", target_port)



    from scapy.arch.windows import get_windows_if_list
    
    all_adapters = get_windows_if_list()
    names = [entry['name'] for entry in all_adapters]

    #print(names)

    from scapy.all import *
    from scapy.all import sniff
    
    conf.use_pcap = True
    conf.use_npcap = True

    """

    def packet_callback(packet):
        print(packet.summary())

    selected_interface = "Loopback Pseudo-Interface 1"
    sniff(iface=selected_interface, prn=packet_callback, store=0)
    """

    def myFunction(pkt):
        print(pkt)

    sniff(filter="host 127.0.0.1", prn=myFunction, iface="lo")