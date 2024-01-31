########
# Student name: Ethan Daugherty
# Course: COSC 3143 Section 01 – Pi and Python
# Assignment: Programming Assignment 3
# Filename: daugherty03_server.py
#
# Purpose: to use a server on port 9000 that listens for data from a gui to change
#          the state of a RGB LED with options to toggle and blink five times
#
# Input: button click and gui
#
# Output: RGB LED lighting up
#
# Common Cathode RGB LED 
#######
import socket
import tkinter as Tk
import RPi.GPIO as GPIO
import time

# Create a socket and bind it to port 9000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9000))

# Start listening for incoming connections
server.listen(1)

#defining pins
redPin = 11
greenPin = 13
bluePin = 15
button = 19

LEDPIN = redPin
#ON/OFF
pinOn = GPIO.HIGH
pinOff = GPIO.LOW


#GPIO setup
#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#variables
color = 0

#Assignment2 LED output functions
def assignment2():
    Start = True
    if Start == True:
            LED_Color = GPIO.output(greenPin,pinOff)
            LED_Color = GPIO.output(redPin,pinOn)
            Start = False
    GPIO.remove_event_detect(button)
    GPIO.add_event_detect(button, GPIO.FALLING, callback=button_callback, bouncetime = 300);
    connectionSocket.close()
def button_callback(channel):
    global color
    global Start
    
    if color == 0:
        LED_Color = GPIO.output(redPin, pinOff)
        LED_Color = GPIO.output(greenPin, pinOn)
        color = 1
        #print("button was pressed", color)
    elif color == 1:
        LED_Color = GPIO.output(greenPin, pinOn)
        LED_Color = GPIO.output(redPin, pinOn)
        color = 2
        #print("button was pressed", color)
    else:
        LED_Color = GPIO.output(greenPin, pinOff)
        LED_Color = GPIO.output(redPin, pinOn)
        color = 0
#Toggle state functions
def toggle_LED(channel):
    GPIO.output(LEDPIN,not(GPIO.input(LEDPIN)))
def toggle():
    GPIO.remove_event_detect(button)
    GPIO.add_event_detect(button, GPIO.FALLING, callback=toggle_LED, bouncetime = 300);
    connectionSocket.close()
#function that blinks the LED 5 times
def blink():
    GPIO.output(greenPin, pinOff)
    GPIO.output(redPin, pinOff)
    for i in range(5):
        GPIO.output(redPin, pinOn)
        time.sleep(1)
        GPIO.output(redPin, pinOff)
        time.sleep(1)
    connectionSocket.close()    
    


try:
    print("Server is running")
    while True:
        connectionSocket, addr = server.accept()
        data = connectionSocket.recv(1024)
        command = data.decode()
        
        if command == "assign2":
            assignment2()
        elif command == "toggle_state":
            toggle()
        elif command == "blink":
            blink()
        else:
            print("Did not receive command")
        
        #Close client socket
        connectionSocket.close()
        
except KeyboardInterrupt:
    print("You have ended the program")
finally:
    server.close()
    print("Server closed")
    GPIO.cleanup()
    print("GPIO cleaned up")



