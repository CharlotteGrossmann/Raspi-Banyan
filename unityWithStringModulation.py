#!/usr/bin/env python3

import logging
import argparse
import traceback
import signal
import sys
import time
from python_banyan.banyan_base import BanyanBase

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

BANYAN_IP="192.168.2.103" #change this to your backplane IP or type " -b >>your backplane IP<<" when you run the script

#this script is based on the "test_unity_sender_cube.py" that is available here: https://github.com/NoahMoscovici/banyanunity

class test(BanyanBase):

    #connect to the backplane
    def __init__(self, back_plane_ip_address=BANYAN_IP,
                 process_name=None, com_port="None", baud_rate=115200, log=False, quiet=False, loop_time="0.1"):
        
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)/ the pin for the analog input
        cs = digitalio.DigitalInOut(board.D5)

        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)
        
        noteOn=0
        
        # initialize the base class
        super().__init__(back_plane_ip_address,  process_name=process_name, numpy=True)


        # Loop sending messages to unitygateway
        while True:
            

            # read values
            xAxis = AnalogIn(mcp, MCP.P1).value/64 #creates values from 0- ~1000 
            yAxis = AnalogIn(mcp, MCP.P2).value/64 #creates values from 0- ~1000 


            try:
                if(xAxis>600 or xAxis<400 or yAxis>600 or yAxis<400):  #if joystick is moved
                    # Define the Unity message to be sent
                    unity_message = {"action":"StringPitch", "info": xAxis, "value": yAxis, "target":"Cube"}

                    # Send the message
                    self.send_unity_message(unity_message)
                    noteOn=1

                elif(noteOn == 1):                                                                  # maybe change this
                    # Define the Unity message to be sent
                    unity_message = {"action":"StringPitch", "info": 500, "value": 500, "target":"Cube"}

                    # Send the message
                    self.send_unity_message(unity_message)
                
                    noteOn=0
                
                
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


