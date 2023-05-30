
import os
import socket
import _thread
import time
import uuid
import hashlib, binascii
from collections import deque

import sys
import serial
import lewansoul_lx16a


class ArtNet:
    
    def __init__(self):

        self.port = 6454
        self.debug = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except Exception as e:
            print("REUSEADDR, did not work for OSX after binding other apps could not use the port:")
            print(e)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
        
        _thread.start_new_thread(self.udp_reader_loop,())
        self.debug_stack = deque([],maxlen=16)
        self.sock.bind(('0.0.0.0',self.port))
        self.lastpackage = None
    
    
    def udp_reader_loop(self):
        '''loop that manages incoming packets'''
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                if len(data) > 0:
                    # keep previous packages for debuging purposes
                    self.debug_stack.append(data)
                    
                    # If the answer is properly formated with Art-Net header
                    if data[:7].decode() =='Art-Net':
                        # check for color package opcode
                        if int.from_bytes(data[8:10], byteorder='little') == 0x5000:
                            universe = int.from_bytes(data[14:16], byteorder='little')
                            length = int.from_bytes(data[16:18], byteorder='little')
                            # get universe
                            # convert data into int tuple
                            self.lastpackage = (universe, length, data[18:])
                                
                    if self.debug:
                        print(str(addr) + " - " + str(data))
                                
                time.sleep(0.001)
            # if the packae is not artnet or not possible to convert to string
            except Exception as e:
                if self.debug:
                    print(e)
                else:
                    pass
                
offset = 0
last_pos = 0

def set_pos(pos_in):
    global last_pos, offset
    actual_motor_position = ctrl.get_position(1)
    offset = actual_motor_position - last_pos
    if pos_in != last_pos:
        ctrl.move(1, pos_in + offset)
        time.sleep(2)
        # maybe need to limit the last post to account for offset
        last_pos = pos_in
        # Switch motor off
        ctrl.motor_off(1)
ctrl.move(1, 0) 
