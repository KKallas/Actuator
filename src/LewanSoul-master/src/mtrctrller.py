import sys, time
import serial
import lewansoul_lx16a

SERIAL_PORT = 'COM9'

ctrl = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=1),
)

"""
import machine
import time

uart = machine.UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=machine.Pin(26), rx=machine.Pin(26), timeout=1000)
"""

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
