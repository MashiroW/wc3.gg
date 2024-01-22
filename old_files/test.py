import psutil

def get_ports_and_pid_for_process(process_name):
    try:
        # Find the process by name
        process = next(p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] == process_name)

        # Get the PID of the process
        process_pid = process.info['pid']

        # Get network connections associated with the process
        connections = process.connections()

        # Filter connections on 127.0.0.1
        localhost_connections = [conn for conn in connections if conn.laddr.ip == '127.0.0.1']

        # Get unique local ports
        local_ports = list(set(conn.laddr.port for conn in localhost_connections))

        return process_pid, local_ports
    except (psutil.NoSuchProcess, StopIteration):
        print(f"Process with name '{process_name}' not found.")
        return None, []

# Example usage:
process_name = "Warcraft III.exe"  # Replace with the name of your process
pid, used_ports = get_ports_and_pid_for_process(process_name)

if pid is not None and used_ports:
    print(f"Process '{process_name}' with PID {pid} is using the following ports on 127.0.0.1:")
    for port in used_ports:
        print(port)
else:
    print(f"No ports found for process '{process_name}'.")
