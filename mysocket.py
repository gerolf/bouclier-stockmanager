import socket

class Mysocket:
        '''demonstration class only
          - coded for clarity, not efficiency'''
        def __init__(self, sock=None):
            if sock is None:
                self.sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.sock = sock
        def connect(self, host, port):
            self.sock.connect((host, port))
        def mysend(self, msg):
            totalsent = 0
            while totalsent < len(msg):
                sent = self.sock.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError,"socket connection broken"
                totalsent = totalsent + sent
        def myreceive(self, size):
            msg = ''
            while len(msg) < size:
                chunk = self.sock.recv(size-len(msg))
                if chunk == '':
                    raise RuntimeError,"socket connection broken"
                msg = msg + chunk
            return msg
