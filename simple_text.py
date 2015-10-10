#!/usr/bin/python
import movingsign
import socket

ip = '10.0.0.110'
port = 10001
message = '[8/8] [UUUUUUUU]'
message = '275G used of 2.8T'

sign = movingsign.MovingSign()
sign.set_text_mode(b'C')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.send(sign.cmd_txt(bytearray(message)))
s.close()
