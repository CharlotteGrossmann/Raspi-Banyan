#!/usr/bin/env python3

import logging
import argparse
import traceback
import signal
import sys
import time
from python_banyan.banyan_base import BanyanBase

import RPi.GPIO as GPIO


BANYAN_IP="192.168.2.103" #change this to your backplane IP or type " -b >>your backplane IP<<" when you run the script

#this script is based on the "test_unity_sender_cube.py" that is available here: https://github.com/NoahMoscovici/banyanunity

class test(BanyanBase):
    
    #connect to backplane
    def __init__(self, back_plane_ip_address=BANYAN_IP,
                 process_name=None, com_port="None", baud_rate=115200, log=False, quiet=False, loop_time="0.1"):
        
        lastNote = -1
        note = -1
        # initialize the base class
        super().__init__(back_plane_ip_address,  process_name=process_name, numpy=True)

        # Loop sending messages to unitygateway
        while True:
            #define the button pins
            C1 = 12
            B = 16
            A = 18
            G = 22
            F = 32
            E = 36
            D = 38
            C = 40

            #setup raspberry to handle the buttons
            GPIO.setmode(GPIO.BOARD)
            
            GPIO.setup(C1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(B,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(A,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(G,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(F,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(E,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(D,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(C,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            
           
            try:
                #connect one button to one note
                if (GPIO.input(C1)==0):
                    note=54
                elif (GPIO.input(B)==0):
                    note=53
                elif (GPIO.input(A)==0):
                    note=51
                elif (GPIO.input(G)==0):
                    note=49
                elif (GPIO.input(F)==0):
                    note=47
                elif (GPIO.input(E)==0):
                    note=46
                elif (GPIO.input(D)==0):
                    note=44
                elif (GPIO.input(C)==0):
                    note=42
                else:
                    note=-1
                    
                #send a message when the pressed button changes
                if(note!= lastNote):
                    #define the message
                    unity_message = {"action":"StringMelody", "info":"blue", "value": note, "target":"Cube"}    

                    #send message
                    self.send_unity_message(unity_message)
                    lastNote=note

            except KeyboardInterrupt:
                self.clean_up()

        

    def send_unity_message(self, unity_message):

        # Set the topic so the unitygateway picks up the message.
        topic = "send_to_unity"

        # Send off the message!
        self.publish_payload(unity_message, topic)

    def clean_up(self):
        
        #Clean up before exiting 
        self.publisher.close()
        self.subscriber.close()
        self.context.term()
        sys.exit(0)

def unity_test():

    #get additional arguments from the console
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                         help="None or IP address used by Back Plane")
    parser.add_argument("-n", dest="process_name", default="Unity Sender",
                         help="Set process name in banner")
    parser.add_argument("-t", dest="loop_time", default=".1",
                         help="Event Loop Timer in seconds")

    args = parser.parse_args()
    kw_options = {}

    if args.back_plane_ip_address != "None":
        kw_options["back_plane_ip_address"] = args.back_plane_ip_address

    kw_options["process_name"] = args.process_name
    kw_options["loop_time"] = float(args.loop_time)

    my_test = test(**kw_options)

    # signal handler function called when Control-C occurs

    def signal_handler(sig, frame):
        print("Control-C detected. See you soon.")

        my_test.clean_up()
        sys.exit(0)

    # listen for SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    unity_test()
