# -*- coding:utf-8 -*-
"""Script for Tkinter GUI VimReversi."""
from threading import Thread
import tkinter as tk
import socket
import select
import sys
import pickle
import copy

from vr_board import Board

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
readfds = set([server_sock])
host = '127.0.0.1' # server host
port = 4000 # port number
bufsize = 4096 # buffer size
backlog = 2 # max queue number


def server_core(board,):
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
                    """ receive """
                    msg = sock.recv(bufsize)
                    msg = pickle.loads(msg)
                    player_turn = None
                    placeloc = None
                    cand_move = board.getCanPlace(board.turn)

                    if not hasattr(server_core, "pass_counter"): # pass counter
                        server_core.pass_counter = 0  # it doesn't exist yet, so initialize it
                    
                    print(msg) # print recv message

                    # if receive message is valid
                    player_turn = msg['turn']
                    placeloc = msg['placeloc']

                    # set player name
                    board.setName(player_turn, msg['software_name'])

                    # place disc
                    if(player_turn == board.turn):
                        if(board.reverseDisc(player_turn, placeloc) == True):
                            board.newest_place = placeloc # last placed disc

                            # draw game info on the listbox
                            board.addList(player_turn, placeloc)
                            board.turn_count += 1

                            board.switch_turn()
                            cand_move = board.getCanPlace(board.turn)
                            server_core.pass_counter = 0

                        elif(msg['pass_flg'] == True): # player passes play
                            board.switch_turn()
                            cand_move = board.getCanPlace(board.turn)
                            server_core.pass_counter += 1

                    """ send """
                    server_info = {}
                    server_info['clicked_index'] = board.clicked_index
                    server_info['board'] = copy.deepcopy(board.discs)
                    server_info['candidate_move'] = cand_move
                    server_info['turn'] = board.turn
                    server_info['turn_count'] = board.turn_count
                    snd_msg = pickle.dumps(server_info) # dump pickle
                    sock.send(snd_msg)

                    if(board.turn_count > 60 or server_core.pass_counter >= 2): # finish the game.
                        print('game finished! gg!')
                        for rdd in readfds:
                            rdd.close()
                        return 
    finally:
        for sock in readfds:
            sock.close()


def main():
    root = tk.Tk()  # create root window
    root.title("VimRev")  # window title
    root.geometry("960x720")  # window size 960x720
    root.resizable(0, 0)  # Prohibit change of window size

    board = Board(root)
    server_thread = Thread(target=server_core, name='server_thread', args=(board,))
    server_thread.start()

    # left click callback
    root.bind("<Button-1>", board.click)

    root.after(10, board.draw)
    root.mainloop()  # Starts GUI execution.


if __name__ == '__main__':
    main()