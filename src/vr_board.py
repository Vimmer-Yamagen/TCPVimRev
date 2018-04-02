#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk


class Board(object):

    def __init__(self, ):
        self.discs = [] # disc on the board
        self.turn = 'Black' # game turn
        self.pass_count = 0 # pass count
        self.turn_count = 1 # game count
        self.newest_place = -1 # last placed disc index

        # Initialize the board
        self.Initialize()


    # Initialize the board
    '''
    Ban : out of the board.
    Space : Free space on the board.
    Black : Place where black disc is placed.
    White Place where white disc is placed.
    CanPlace : Place where player can place disc on this turn.
    '''
    def Initialize(self, ):
        for i in range(100):
            self.discs.append('Space')

        for i in range(0, 10):
            self.discs[i] = 'Ban'
            self.discs[i + 90] = 'Ban'
        for i in range(10, 81, 10):
            self.discs[i] = 'Ban'
            self.discs[i + 9] = 'Ban'
        for i in range(0, 90):
            if(int(i / 10) == 0 or int(i % 10) == 0 or int(i % 10) == 9):
                continue
            else:
                self.discs[i] = 'Space'

        self.discs[45] = self.discs[54] = 'Black'
        self.discs[44] = self.discs[55] = 'White'
        self.discs[34] = self.discs[43] = self.discs[56] = self.discs[65] = 'CanPlace'


    # if place index is valid, reverseDisc and return True. else return False
    def reverseDisc(self, turn, index):

        if(self.discs[index] != 'CanPlace'):
            return False
        
        list_reverse = []
        direction = [-11, -10, -9, -1, +1, +9, +10, +11] # 8 direction search
        myDisc = "Black" if (turn == "Black") else "White"
        yourDisc = "Black" if (turn == "White") else "White"

        for d in direction:
            j = index + d
            while(True):
                if(self.discs[j] == yourDisc):
                    list_reverse.append(j)
                elif(self.discs[j] == myDisc):
                    for rev in list_reverse:
                        self.discs[rev] = myDisc
                    break
                elif(self.discs[j] == "Space" or self.discs[j] == "CanPlace" or self.discs[j] == "Ban"):
                    list_reverse = []
                    break
                j += d

        self.discs[index] = myDisc
        return True


    # switch game turn
    def switch_turn(self, ):
        if(self.turn == 'Black'):
            self.turn = 'White'
        elif(self.turn == 'White'):
            self.turn = 'Black'


    # Return a list of places you can place after marking on the board
    def getCanPlace(self, turn):

        # delete all mark
        for index, disc in enumerate(self.discs):
            if(disc == "CanPlace"):
                self.discs[index] = "Space"

        list_canplace = []
        direction = [-11, -10, -9, -1, +1, +9, +10, +11] # 8 direction search
        myDisc = "Black" if (turn == "Black") else "White"
        yourDisc = "Black" if (turn == "White") else "White"

        for index, disc in enumerate(self.discs):
            if (disc == "Space"):
                for d in direction:
                    if (self.discs[index + d] == yourDisc):
                        k = index + d * 2
                        while(True):
                            if(self.discs[k] == "Ban" or self.discs[k] == "Space" or self.discs[k] == "CanPlace"):
                                break
                            elif(self.discs[k] == myDisc):
                                self.discs[index] = "CanPlace"
                                list_canplace.append(index)
                                break
                            k += d
        return list_canplace


    # return disc number
    def getDiscNum(self, turn):
        number = 0
        for disc in self.discs:
            if(disc == turn):
                number += 1
        return number
