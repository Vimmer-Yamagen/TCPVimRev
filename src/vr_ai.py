# -*- coding:utf-8 -*-
import socket
from contextlib import closing
import pickle
import time
import random
import argparse

from vr_board import Board

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1' # server host
port = 4000 # port number
bufsize = 4096


def client_core(turn, software_name):
    with closing(sock):
        sock.connect((host, port))

        name = software_name
        board = None
        place_candidates = []
        game_turn = None
        turn_count = 0
        my_turn = turn
        placeloc = -1
        pass_flg = False

        while True:

            time.sleep(0.5) # sleep 0.5 seconds

            """ send """
            try:
                if(game_turn == my_turn):
                    if(not place_candidates): # player passes the game
                        pass_flg = True
                        print('pass!')

                    random.shuffle(place_candidates) # select the place location
                    placeloc = place_candidates[0]
                else:
                    # print('not my turn')
                    placeloc = -1 # not my turn
            except:
                # print('catch exceptions')
                placeloc = -1 # catch exceptions
            finally:
                snd_msg = {}
                snd_msg['software_name'] = name
                snd_msg['turn'] = my_turn
                snd_msg['placeloc'] = placeloc
                snd_msg['pass_flg'] = pass_flg
                snd_msg = pickle.dumps(snd_msg) # dump pickle
                sock.send(snd_msg)
                pass_flg = False

            """ receive """
            try:
                msg = sock.recv(bufsize)
                msg = pickle.loads(msg)
                # print(msg['candidate_move'], msg['turn']) # print recv message

                board = msg['board']
                place_candidates = msg['candidate_move']
                game_turn = board.turn
                turn_count = board.turn_count
            except:
                print('good bye!')
                sock.close()
                return

def main():
    # parser
    parser = argparse.ArgumentParser(description='VimRev')
    parser.add_argument('-m', '--move', help='configure first move or passive move.', choices=['Black', 'White'], required=True)
    parser.add_argument('-n', '--name', help='configure software name', default='No Name')

    # parse command-line args
    args = parser.parse_args()
    client_core(args.move, args.name)


if __name__ == '__main__':
    main()