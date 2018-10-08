import socket,time,numpy,cv2,io
from PIL import Image

host = '172.17.57.209'
port = 2222
soc = socket.socket()
soc.connect((host,port))
cam = cv2.VideoCapture(0)

while True:
    ret,frame = cam.read()
    cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    pile_im = Image.fromarray(cv2_im)
    b = io.BytesIO()
    pile_im.save(b,'jpeg')
    im_bytes = b.getvalue()
    t_sent = 0
    m_sent = 0
    length = len(im_bytes)
    length_s = str(length).zfill(8)
    soc.send(bytes(length_s,'utf-8'))
    while t_sent < length:
        sent = soc.send(im_bytes[t_sent:])
        t_sent += sent
    t_recv = 0
    m_recv = 0
    msg = []
    length = int(str(soc.recv(8),'utf-8'))
    frame=b''
    while t_recv < length:
        chunk = soc.recv(length-t_recv)
        frame+=chunk
        t_recv += len(chunk)
    pil_bytes = io.BytesIO(frame)
    pil_image = Image.open(pil_bytes)
    cv_image = cv2.cvtColor(numpy.array(pil_image),cv2.COLOR_RGB2BGR)
    cv2.imshow('Client',cv_image)
    cv2.waitKey(1)

