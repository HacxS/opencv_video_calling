import socket,time,numpy,cv2,io
from PIL import Image

host = '127.0.0.1'
port = 2222

soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

soc.sendto(bytes('Client2','utf-8'),(host,port))
time.sleep(5)

def frame_send(cam,soc):
    ret,frame = cam.read()
    cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    pile_im = Image.fromarray(cv2_im)
    b = io.BytesIO()
    pile_im.save(b,'jpeg')
    im_bytes = b.getvalue()
    t_sent = 0
    m_sent = 0
    length = len(im_bytes)
    lengthstr = str(length).zfill(8)
    while m_sent < 8:
        sent = soc.sendto(bytes(lengthstr,'utf-8'),(host,port))
        m_sent += sent
    while t_sent < length:
        sent = soc.sendto(im_bytes[t_sent:],(host,port))
        t_sent += sent

def frame_recv(soc):
    t_recv = 0
    m_recv = 0
    metaArray = []
    msg = []
    chunk,addr = soc.recvfrom(8-m_recv)
    length = int(str(chunk,'utf-8'))
    f = open('hacC3','wb')
    while t_recv < length:
        chunk,addr = soc.recvfrom(length-t_recv)
        f.write(chunk)
        print(t_recv)
        t_recv += len(chunk)
    f.close()
    frame_bytes = open('hacC3','rb').read()
    pil_bytes = io.BytesIO(frame_bytes)
    pil_image = Image.open(pil_bytes)
    cv_image = cv2.cvtColor(numpy.array(pil_image),cv2.COLOR_RGB2BGR)
    cv2.imshow('Client2',cv_image)
    cv2.waitKey(1)


total = 0
while True:
    frame_recv(soc)
