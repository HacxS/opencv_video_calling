import socket,time,numpy,cv2,io
from PIL import Image

host = '0.0.0.0'
port = 2222
soc = socket.socket()
soc.bind((host,port))
soc.listen(5)
cli,addr=soc.accept()
cam = cv2.VideoCapture(0)

while True:
    t_recv = 0
    m_recv = 0
    msg = []
    length = int(str(cli.recv(8),'utf-8'))
    frame = b''
    while t_recv < length:
        chunk = cli.recv(length-t_recv)
        frame+=chunk
        t_recv += len(chunk)
    frame_bytes = frame
    pil_bytes = io.BytesIO(frame_bytes)
    pil_image = Image.open(pil_bytes)
    cv_image = cv2.cvtColor(numpy.array(pil_image),cv2.COLOR_RGB2BGR)
    cv2.imshow('Client',cv_image)
    cv2.waitKey(1)
    ret,frame = cam.read()
    cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    pile_im = Image.fromarray(cv2_im)
    b = io.BytesIO()
    pile_im.save(b,'jpeg')
    im_bytes = b.getvalue()
    t_sent = 0
    m_sent = 0
    length = len(im_bytes)
    length_s = str(len(im_bytes)).zfill(8)
    cli.send(bytes(length_s,'utf-8'))
    while t_sent < length:
        sent = cli.send(im_bytes[t_sent:])
        t_sent += sent
