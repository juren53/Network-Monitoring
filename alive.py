#!/usr/bin/python
#-----------------------------------------------------------
#  alive.py         
#      Runs in background, sounding alarm when the network
#      connection goes down and then turns off alarm when 
#      network connection is restored w date/time stamps
# Created: Thu 30 Mar 2023 08:05:33 AM CDT
# Updated: Fri 31 Mar 2023 01:41:57 AM CDT   Date/Time tweaks 
#-----------------------------------------------------------

import os
import socket
import time
import threading
from playsound import playsound
import keyboard
import datetime
import subprocess

def check_network():
    network_status = True  # assume network is up at start
    while True:
        try:
            # connect to a well-known website to check network status
            s = socket.create_connection(('www.google.com', 80))
            s.close()
            if not network_status:
                network_status = True
                #os.system('clear')  # clear the screen
                output = subprocess.check_output(['iwgetid', '-r'])
                ssid = output.decode('utf-8').strip()
                current_time = datetime.datetime.now()
                print("================================================================")
                print("Network connection re-established at:", current_time.strftime("%Y-%m-%d %H:%M:%S")," connected to ",ssid)
            # wait for 5 seconds before checking again
            time.sleep(5)
        except OSError:
            if network_status:
                network_status = False
                t = threading.Thread(target=play_alarm_sound)
                t.start()
            # keep playing sound until connection restored or escape key is pressed
            while not keyboard.is_pressed('esc') and not check_network_status():
                pass
            t.join()

def play_alarm_sound():
    #os.system('clear')  # clear the screen
    current_time = datetime.datetime.now()
    print("================================================================")
    print("Network connection lost              ", current_time.strftime("%Y-%m-%d %H:%M:%S"))
    while not keyboard.is_pressed('esc') and not check_network_status():
        playsound('sound.mp3')

def check_network_status():
    try:
        s = socket.create_connection(('www.google.com', 80))
        s.close()
        return True
    except OSError:
        return False

if __name__ == '__main__':
    #os.system('clear')  # clear the screen
    output = subprocess.check_output(['iwgetid', '-r'])
    ssid = output.decode('utf-8').strip()
    current_time = datetime.datetime.now()
    print("================================================================ v 0.7")
    print("The network is up at                 ", current_time.strftime("%Y-%m-%d %H:%M:%S")," connected to ",ssid)
    check_network()

