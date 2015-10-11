#!/usr/bin/python
import movingsign
import socket
import serial
import time

ip = '10.0.0.110'
port1 = 10001
port2 = 10002

ser_port1 = '/dev/ttyS1'
ser_port2 = '/dev/ttyS2'
baud = 9600
#message = '[8/8] [UUUUUUUU]'
#message = '275G used of 2.8T'

sign = movingsign.MovingSign()
sign.set_text_mode(b'C')

def send_message_socket(message, sign_ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((sign_ip, port))
	s.send(message)
	s.close()

#def open_serial(port):
ser1 = serial.Serial(ser_port1, baud, timeout=1)
ser1.open()
ser2 = serial.Serial(ser_port2, baud, timeout=1)
ser2.open()

def write_serial(text, ser):
	message = sign.cmd_txt(bytearray(text))
	ser.write(message)

def send_text(text, sign_ip, port):
	message = sign.cmd_txt(bytearray(text))
	send_message(message, sign_ip, port)

def get_mdadm():
	status = open('/proc/mdstat').read()
	lines = status.split('\n')
	words = lines[2].split('[')
	final_status = '[%s [%s' % (words[1], words[2])
	return final_status

def get_disk_space():
	import subprocess
	df = subprocess.Popen(["df", "-h", "/dev/bcache0"], stdout=subprocess.PIPE)
	output = df.communicate()[0]
	device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
	return '%s used of %s' % (used, available)

def clear_sign(sign_ip, port):
    send_message(sign.clear(), sign_ip, port)

#clear_sign(ip, port1)
#clear_sign(ip, port2)
#open_serial(ser_port1)
#open_serial(ser_port2)
while True:
	#send_text('Raid Array Health', ip, port1)
	#send_text(get_mdadm(), ip, port2)
	write_serial('Raid Array Health', ser1)
	write_serial(get_mdadm(), ser2)
	time.sleep(7)

	#send_text('File Server Disk Usage', ip, port1)
	#send_text(get_disk_space(), ip, port2)
	write_serial('File Server Disk Usage', ser1)
	write_serial(get_disk_space(), ser2)
	time.sleep(7)
