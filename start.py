import subprocess
import threading

# Define the command line commands to be executed
command1 = "make run"
command2 = "ngrok http 15316"

# Function to run a command and print its output
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(f"Output of '{command}': {stdout.decode().strip()}")
    else:
        print(f"Error in '{command}': {stderr.decode().strip()}")

# Create threads for each command
thread1 = threading.Thread(target=run_command, args=(command1,))
thread2 = threading.Thread(target=run_command, args=(command2,))

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()
