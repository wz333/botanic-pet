import subprocess
import threading
import queue
import ngrok
import time
import pygame  # Import pygame graphics library
import os  # for OS calls
import RPi.GPIO as GPIO
import time
import subprocess
from pygame.locals import * #for event MOUSE variables

time_lim = 300
start_time=time.time()

run_flag=False
global x,y
x,y=None,None

GPIO.setmode(GPIO.BCM)   # Set for GPIO (bcm) numbering not pin numbers...
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def quit_callback(channel):
    global run_flag
    run_flag=False


GPIO.add_event_detect(17,GPIO.FALLING, callback=quit_callback, bouncetime=300)

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on PiTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
WHITE=255,255,255
BLACK=0,0,0
RED = 255,0,0
GREEN = 0,255,0
screen=pygame.display.set_mode((320,240))

my_font=pygame.font.Font(None,25)
my_buttons={'start':(160,120), 'quit':(300,220), 'stop':(160,120)}


start_flag=False
while not start_flag:
    time.sleep(0.01)
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            print(pos)
            x,y=pos
            if my_buttons['start'][0]-quit_size<=x<=my_buttons['start'][0]+quit_size and my_buttons['start'][1]-quit_size<=y<=my_buttons['start'][1]+quit_size:
                start_flag=True
    if not start_flag:
        screen.fill(BLACK)
        text="Start"
        text_surface=my_font.render(text, True,WHITE)
        rect=text_surface.get_rect(center=(160, 120))
        screen.blit(text_surface, rect)
        pygame.display.flip()
    else:
        break


run_flag=True

token="2SdWPJwnHdEBykmoCaXMG46eHyN_4F76ySnCkRVERtJonM1rf"
ngrok.set_auth_token(token)
listener = ngrok.connect("localhost:15316")

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

# Wait for the command threads to finish 
thread1.join()

while run_flag:
    # draw STOP btn
    pygame.draw.circle(screen,RED,stop_center,stop_radius)
    text="STOP"
    text_surface=my_font.render(text, True,WHITE)
    rect=text_surface.get_rect(center=(160, 120))
    screen.blit(text_surface, rect)
    text2=f"Ingress established at: {listener.url()}"
    text2_surface=my_font.render(text, True,WHITE)
    rect2=text_surface.get_rect(center=(160, 120))
    screen.blit(text2_surface, rect2)
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            print(pos)
            x,y=pos
            if my_buttons['start'][0]-quit_size<=x<=my_buttons['start'][0]+quit_size and my_buttons['start'][1]-quit_size<=y<=my_buttons['start'][1]+quit_size:
                run_flag=False

