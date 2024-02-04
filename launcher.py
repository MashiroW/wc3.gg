import subprocess

if __name__ == "__main__":
    
    print("Launcher starting")

    # Define the commands to run the scripts
    command1 = 'python ./ui_clicker.py'
    # command2 = 'python ./packets_sniffer.py'

    # Run the scripts concurrently in different shells
    process1 = subprocess.Popen(command1, shell=True)
    # process2 = subprocess.Popen(command2, shell=True)

    # Wait for both processes to finish
    process1.wait()
    # process2.wait()

    command3 = "python wc3rankedsite/manage.py load_players ./databases/"
    process3 = subprocess.Popen(command3, shell=True)
    process3.wait()