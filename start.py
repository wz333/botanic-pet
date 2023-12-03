import subprocess
import threading
import queue
import ngrok

listener = ngrok.connect("localhost:15316", authtoken_from_env=True)

print(f"Ingress established at: {listener.url()}");

def run_command(command, output_queue):
    """Run a command and put its output into a queue."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Continuously read output from the process
    for line in iter(process.stdout.readline, ''):
        output_queue.put((command, line))

    # After the command finishes, check for any errors
    stderr = process.stderr.read()
    if stderr:
        output_queue.put((command, f"ERROR: {stderr}"))

# Function to print output from the queue
def print_output(output_queue):
    while True:
        command, line = output_queue.get()
        if line is None:  # Sentinel value to break the loop
            break
        print(f"Output from {command}: {line}", end='')

# Create a queue to share output between threads
output_queue = queue.Queue()

# Define commands
command1 = "make run"
# command2 = "ngrok http 15316"

# Start the command threads
thread1 = threading.Thread(target=run_command, args=(command1, output_queue))
# thread2 = threading.Thread(target=run_command, args=(command2, output_queue))
thread1.start()
# thread2.start()

# # Start a thread to print output
# print_thread = threading.Thread(target=print_output, args=(output_queue,))
# print_thread.start()

# Wait for the command threads to finish (you might want to add a timeout here)
thread1.join()
# thread2.join()

# # Signal the print thread to stop
# output_queue.put((None, None))
# print_thread.join()
