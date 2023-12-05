import subprocess
import threading
import queue
import ngrok
import time
import pygame  # Import pygame graphics library
import os  # for OS calls
import sys
import RPi.GPIO as GPIO
import time
import subprocess
from pygame.locals import * #for event MOUSE variables


time_lim = 120
start_time=time.time()

run_flag=True
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
quit_size=20
stop_center=160,120
stop_radius=40
screen=pygame.display.set_mode((320,240))

my_font=pygame.font.Font(None,25)
my_font2=pygame.font.Font(None,20)
my_font2.set_bold(False)
my_buttons={'start':(160,120), 'quit':(300,220), 'stop':(160,120)}


start_flag=False


while not start_flag and run_flag and time.time()-start_time<time_lim:
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
        pygame.draw.circle(screen,GREEN,stop_center,stop_radius)
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





class ServerThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        self.process = subprocess.Popen(self.command, shell=True)
        self.process.communicate()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

command = "make run" 
server_thread = ServerThread(command)
server_thread.start()




while run_flag and time.time()-start_time<time_lim:
    # draw STOP btn
    pygame.draw.circle(screen,RED,stop_center,stop_radius)
    text="STOP"
    text_surface=my_font.render(text, True,WHITE)
    rect=text_surface.get_rect(center=(160, 120))
    screen.blit(text_surface, rect)
    text2="Server established at:"
    text2_surface=my_font2.render(text2, True,WHITE)
    rect2=text2_surface.get_rect(center=(160, 180))
    screen.blit(text2_surface, rect2)
    text3=f"{listener.url()}"
    text3_surface=my_font2.render(text3, True,WHITE)
    rect3=text3_surface.get_rect(center=(160, 200))
    screen.blit(text3_surface, rect3)
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            print(pos)
            x,y=pos
            if my_buttons['start'][0]-quit_size<=x<=my_buttons['start'][0]+quit_size and my_buttons['start'][1]-quit_size<=y<=my_buttons['start'][1]+quit_size:
                run_flag=False
    pygame.display.flip()

# Stop the server
server_thread.stop()

# Wait for the command threads to finish 
pygame.quit()


