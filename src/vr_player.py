# -*- coding:utf-8 -*-
import sys
import socket
from contextlib import closing
import pickle

import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1' # server host
port = 4000 # port number
bufsize = 4096


def main():
    with closing(sock):
        sock.connect((host, port))
        while True:
            print('Message : ', end="")
            line = 'Player input'

            time.sleep(2)

            snd_msg = pickle.dumps(line) # dump pickle
            sock.send(snd_msg)

            if(line == 'shutdown'):
                sock.close()
                sys.exit()

            msg = sock.recv(bufsize)
            msg = pickle.loads(msg)
            if(msg == 'quit'):
                sock.close()
                break
            else:
                print(msg)

if __name__ == '__main__':
    main()