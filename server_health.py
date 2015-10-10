#!/usr/bin/python
import movingsign
import socket
import time

ip = '10.0.0.110'
port = 10001
#message = '[8/8] [UUUUUUUU]'
#message = '275G used of 2.8T'

sign = movingsign.MovingSign()
sign.set_text_mode(b'C')

def send_message(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(sign.cmd_txt(bytearray(message)))
    s.close()

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


while True:
    send_message('File Server Health')
    time.sleep(5)
    send_message(get_mdadm())
    time.sleep(10)
    send_message(get_disk_space())
    time.sleep(10)
