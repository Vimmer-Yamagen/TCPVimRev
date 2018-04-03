# -*- coding:utf-8 -*-
"""Script for Tkinter GUI VimReversi."""
from threading import Thread
import tkinter as tk
import socket
import select
import pickle
import copy

from vr_board import Board
from vr_gui import GUI


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
readfds = set([server_sock])
host = '127.0.0.1' # server host
port = 4000 # port number
bufsize = 4096 # buffer size
backlog = 2 # max queue number


def server_core(board, gui,):

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
                    """ end receive """

                    print(msg) # print recv message

                    # if receive message is valid
                    player_turn = msg['turn']
                    placeloc = msg['placeloc']
                    cand_move = board.getCanPlace(board.turn)
                    next_turn_flg = False

                    # set player name
                    gui.setName(player_turn, msg['software_name'])

                    # place disc
                    if(player_turn == board.turn):
                        if(board.reverseDisc(player_turn, placeloc) == True): # Successfully placed the disc
                            # set last placed disc
                            board.newest_place = placeloc
                            # go next turn
                            next_turn_flg = True
                            # draw game info on the listbox
                            gui.addList(player_turn, board.turn_count, placeloc)
                            # switch game turn(Black to White or White to Black)
                            board.switch_turn()
                            # get candidate place list
                            cand_move = board.getCanPlace(board.turn)
                            # record the board.
                            gui.record[board.turn_count] = {'Board':copy.deepcopy(board.discs), 'newest_place':board.newest_place}
                            # reset pass count
                            board.pass_count = 0

                        # player can't place the disc in this turn.
                        elif(msg['pass_flg'] == True):
                            # switch game turn(Black to White or White to Black)
                            board.switch_turn()
                            # get candidate place list
                            cand_move = board.getCanPlace(board.turn)
                            # pass count +1
                            board.pass_count += 1

                    # finish the game or server shutdown command is pressed.
                    if(board.pass_count >= 2):
                        print('game finished! gg!')
                        return
                    if(gui.end_flg):
                        print('server shutdown!')
                        return

                    # go next turn
                    if(next_turn_flg):
                        gui.record_count += 1 if(gui.record_count == board.turn_count and board.turn_count < 60) else 0
                        board.turn_count += 1 if(board.turn_count < 60) else 0

                    """ send """
                    server_info = {}
                    server_info['clicked_index'] = gui.clicked_index
                    server_info['board'] = copy.deepcopy(board)
                    server_info['candidate_move'] = cand_move

                    # the game hasn't start yet
                    if(not gui.start_flg):
                        server_info['board'].turn = 'None'
                        server_info['candidate_move'] = []

                    # dump pickle
                    snd_msg = pickle.dumps(server_info)
                    sock.send(snd_msg)
                    """ end send """
    finally:
        for sock in readfds:
            sock.close()
        return


def main():

    root = tk.Tk()  # create root window
    root.title("VimRev")  # window title
    root.geometry("960x720")  # window size 960x720
    root.resizable(0, 0)  # Prohibit change of window size

    board = Board()
    gui = GUI(root, board)
    server_thread = Thread(target=server_core, name='server_thread', args=(board, gui,))
    server_thread.start()

    # left click callback
    root.bind("<Button-1>", gui.click)

    # key press callback
    root.bind("<Control-s>", gui.key) # start the game.
    root.bind("<Control-q>", gui.key) # end the game.
    root.bind("<Control-c>", gui.key) # end the game.

    root.after(100, gui.draw, board)
    root.mainloop()  # Starts GUI execution.


if __name__ == '__main__':
    main()