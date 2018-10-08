import socket,time,numpy,cv2,io
from PIL import Image

host = '127.0.0.1'
port = 2222
soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
soc.bind((host,port))


name,addr1 = soc.recvfrom(1024)

print(name,' added to server')
name,addr2 = soc.recvfrom(1024)

print(name,' added to server')

def frame_recv(soc):
    t_recv = 0
    m_recv = 0
    msg = []
    chunk,addr = soc.recvfrom(8)
    
    length = int(str(chunk,'utf-8'))
    print(length)
    f = open('hacS','wb')
    while t_recv < length:
        chunk,addr = soc.recvfrom(length-t_recv)
        f.write(chunk)
        t_recv += len(chunk)
    f.close()

def frame_send():
    frame_bytes = open('hacS','rb').read()
    t_sent = 0
    t=0
    m_sent = 0
    length = len(frame_bytes)
    lengthstr = str(length).zfill(8)
    sent = soc.sendto(bytes(lengthstr,'utf-8'),addr1)
    while t_sent < length:
        sent = soc.sendto(frame_bytes[t_sent:],addr1)
        t_sent += sent

    sent = soc.sendto(bytes(lengthstr,'utf-8'),addr2)
    while t_sent < length:
        sent = soc.sendto(frame_bytes[t_sent:],addr2)
        t_sent += sent




while True:
    frame_recv(soc)
    frame_send()
