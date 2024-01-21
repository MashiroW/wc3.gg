import subprocess

# Define the commands to run the scripts
command1 = ['python', "./websocket_listener.py"]
command2 = ['python', "./ui-clicker.py"]

# Run the scripts concurrently
process1 = subprocess.Popen(command1)
process2 = subprocess.Popen(command2)

# Wait for both processes to finish
process1.wait()
process2.wait()