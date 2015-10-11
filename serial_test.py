#!/usr/bin/python
import movingsign
import serial

port = '/dev/ttyUSB0'
baud = 9600
message = '[8/8] [UUUUUUUU]'
message = '275G used of 2.8T'

sign = movingsign.MovingSign()
sign.set_text_mode(b'C')

ser = serial.Serial(port, baud, timeout=1)
ser.open()
ser.write(sign.cmd_txt(bytearray(message)))
ser.close()
