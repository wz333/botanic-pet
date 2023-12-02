import subprocess
from threading import Thread

def run_command(command, result):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    result.append((output, error))

# Commands to run in parallel
command1 = ["echo", "make run"]
command2 = ["echo", "ngrok http 15316"]

# List to store the results
results = []

# Create threads for each command
thread1 = Thread(target=run_command, args=(command1, results))
thread2 = Thread(target=run_command, args=(command2, results))

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

# Print the results
for i, (output, error) in enumerate(results):
    print(f"Command {i + 1} Output:")
    print(output)
    print(f"Command {i + 1} Error:")
    print(error)
    print("=" * 30)
