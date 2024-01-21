import subprocess
from datetime import datetime

def log_message(message, log_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    log_file.write(log_entry + "\n")

if __name__ == "__main__":
    
    # Define the log file path
    log_file_path = "output_log.txt"

    # Open the log file in write mode with UTF-8 encoding
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        # Log start time
        log_message("Script started", log_file)

        # Define the commands to run the scripts
        command1 = ['python', "./packets_sniffer.py"]
        command2 = ['python', "./ui-clicker.py"]

        # Run the scripts concurrently, redirecting output to the log file
        process1 = subprocess.Popen(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process2 = subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            while True:
                # Read and log output from process1
                line = process1.stdout.readline()
                if not line and process1.poll() is not None:
                    break
                log_message(line.decode('utf-8', errors='replace').strip(), log_file)

                # Read and log output from process2
                line = process2.stdout.readline()
                if not line and process2.poll() is not None:
                    break
                log_message(line.decode('utf-8', errors='replace').strip(), log_file)
        except KeyboardInterrupt:
            pass

        # Wait for both processes to finish
        process1.wait()
        process2.wait()

        # Log end time
        log_message("Script finished", log_file)

    print(f"Log file created: {log_file_path}")
