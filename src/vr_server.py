# -*- coding:utf-8 -*-
"""Script for Tkinter GUI VimReversi."""
from threading import Thread
import tkinter as tk
import socket
import select
import sys
import pickle


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
readfds = set([server_sock])
host = '127.0.0.1' # server host
port = 4000 # port number
bufsize = 1024 # buffer size
backlog = 2 # max queue number


def server_core(root, ):
    try:
        server_sock.bind((host, port))
        server_sock.listen(backlog)

        while True:
            rready, wready, xready = select.select(readfds, [], [])
            for sock in rready:
                if sock is server_sock:
                    conn, address = server_sock.accept()
                    readfds.add(conn)
                else:
                    msg = sock.recv(bufsize)
                    msg = pickle.loads(msg)
                    print(msg)

                    s = tk.Label(text=msg)
                    s.pack()

                    snd_msg = pickle.dumps(msg) # dump pickle
                    sock.send(snd_msg)
                    if(msg == 'quit'):
                        sock.close()
                        readfds.remove(sock)
                    elif(msg == 'shutdown'):
                        for rdd in readfds:
                            rdd.close()
                        print('server shutdown. good bye!')
                        sys.exit()
    finally:
        for sock in readfds:
            sock.close()


def main():
    root = tk.Tk()  # create root window
    root.title("VimRev")  # window title
    root.geometry("960x720")  # window size 960x720
    root.resizable(0, 0)  # Prohibit change of window size

    server_thread = Thread(target=server_core, name='server_thread', args=(root,))
    server_thread.start()
    root.mainloop()  # Starts GUI execution.


if __name__ == '__main__':
    main()