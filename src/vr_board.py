#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk


class Board(object):

    def __init__(self, root, ):
        self.root = root
        self.frame = tk.Frame(self.root, width=960, height=720)
        self.frame.place(x=0, y=0)
        self.canvas = tk.Canvas(self.frame, width=960, height=720)
        self.canvas.place(x=0, y=0)

        self.discs = [] # disc on the board
        for i in range(100):
            self.discs.append('Space')

        self.turn = 'Black' # game turn
        self.newest_place = -1 # last placed disc index

        # Initialize the board
        self.Initialize()


    # Initialize the board
    def Initialize(self, ):
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

        self.discs[45] = 'Black'
        self.discs[54] = 'Black'
        self.discs[44] = 'White'
        self.discs[55] = 'White'
        self.discs[34] = 'CanPlace'
        self.discs[43] = 'CanPlace'
        self.discs[56] = 'CanPlace'
        self.discs[65] = 'CanPlace'

    # if place index is valid, reverseDisc and return True. else return False
    def reverseDisc(self, turn, index):

        if(self.discs[index] != 'CanPlace'):
            return False
        
        list_reverse = []
        direction = [-11, -10, -9, -1, +1, +9, +10, +11] # 8方向探索
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
                j+= d

        self.discs[index] = myDisc
        return True


    # switch game turn
    def switch_turn(self, ):
        if(self.turn == 'Black'):
            self.turn = 'White'
        elif(self.turn == 'White'):
            self.turn = 'Black'


    # ボード上の着手可能場所に印を付けて着手可能場所のリストを返す
    def getCanPlace(self, turn):

        # 着手可能場所の印を全て消す
        for index, disc in enumerate(self.discs):
            if(disc == "CanPlace"):
                self.discs[index] = "Space"

        list_canplace = []
        direction = [-11, -10, -9, -1, +1, +9, +10, +11] # 8方向探索
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

    def getDiscNum(self, turn):
        number = 0
        for index, disc in enumerate(self.discs):
            if(disc == turn):
                number += 1
        return number

    # draw the board.
    def draw(self, ):

        self.canvas.delete("board") # ボードを消す
        self.canvas.delete("disc")  # ボード上の石を消す
        self.canvas.delete('info') # ゲーム情報を消す

        # ボードを描画
        self.canvas.create_rectangle(0, 0, 720, 720, fill='#1E824C', tag="board")

        # ボードのマスを描画
        for i in range(9):
            self.canvas.create_line(
                i * 90, 0, i * 90, 720, width=1.2, fill="Black", tag="board")
            self.canvas.create_line(
                0, i * 90, 720, i * 90, width=1.2, fill="Black", tag="board")

        # ボードの丸印を描画
        self.canvas.create_oval(180 - 4, 180 - 4, 180 + 4, 180 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(180 - 4, 540 - 4, 180 + 4, 540 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(540 - 4, 180 - 4, 540 + 4, 180 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(540 - 4, 540 - 4, 540 + 4, 540 + 4, fill="Black", outline="Black", tag="board")

        # 石を描画
        for index, disc in enumerate(self.discs):
            center_x = 45 + int((index-1) % 10) * 90
            center_y = 45 + int((index-10) / 10) * 90
            if(disc == "Black"):    
                self.canvas.create_oval(center_x - 43, center_y - 43, center_x + 43, center_y + 43, fill="Black", outline="Black", tag="disc")
            elif(disc == "White"):    
                self.canvas.create_oval(center_x - 44, center_y - 44, center_x + 44, center_y + 44, fill="White", outline="Black", tag="disc")
            elif(disc == "CanPlace"):    
                self.canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="OliveDrab1", outline="OliveDrab1", tag="disc")
            # 最後に打たれた石の場合、マークを付ける
            if(index == self.newest_place):
                self.canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8, fill="Red", outline="Red", tag="disc")

        # ゲーム情報を描画
        b_info = 'Black : ' + str(self.getDiscNum('Black')) + ' discs'
        w_info = 'White : ' + str(self.getDiscNum('White')) + ' discs'
        self.canvas.create_text(810, 20, text=b_info, font = ('Helvetica', 16), tag='info')
        self.canvas.create_text(810, 50, text=w_info, font = ('Helvetica', 16), tag='info')

        self.canvas.pack()
        self.root.after(10, self.draw)