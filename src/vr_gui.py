#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk


class GUI(object):

    def __init__(self, root,):
        self.root = root
        self.frame = tk.Frame(self.root, width=960, height=720)
        self.frame.place(x=0, y=0)
        self.canvas = tk.Canvas(self.frame, width=960, height=720)
        self.canvas.place(x=0, y=0)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.frame, width=40, height=30, yscrollcommand=self.scrollbar.set)
        self.listbox.place(x=700, y=200)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.b_name = None # black player name
        self.w_name = None # white player name

        self.clicked_index = -1 # board index which human player clicked


    def click(self, mouse):
        # out of the board
        if(40 > mouse.x or mouse.x > 680 or 40 > mouse.y or mouse.y > 680):
            return
        self.clicked_index = int((mouse.y - 40) / 80 + 1) * 10 + int((mouse.x - 40) / 80 + 1)


    def setName(self, turn, name):
        if(turn == 'Black' and self.b_name is None):
            self.b_name = name
        elif(turn == 'White' and self.w_name is None):
            self.w_name = name


    def addList(self, turn, turn_count, placeloc):
        alphabet = [chr(i) for i in range(65, 65 + 8)]
        # game_info = str(turn_count) + '. ' + turn + '       ' + str(alphabet[placeloc % 10 - 1]) + str(int(placeloc / 10))
        game_info = '{:0>2}{:>8}{:>3}'.format(str(turn_count) + '.', turn + ' :', str(alphabet[placeloc % 10 - 1]) + str(int(placeloc / 10)))
        self.listbox.insert(tk.END, game_info)

    # draw the board.
    def draw(self, board,):

        self.canvas.delete("board") # delete objects with "board" tag
        self.canvas.delete("disc")  # delete objects with "disc" tag
        self.canvas.delete('info') # delete objects with "info" tag

        # draw the board
        self.canvas.create_rectangle(40, 40, 680, 680, fill='#1E824C', tag="board")

        # draw squares on the board
        for i in range(9):
            self.canvas.create_line(
                i * 80 + 40, 40, i * 80 + 40, 680, width=1.2, fill="Black", tag="board")
            self.canvas.create_line(
                40, i * 80 + 40, 680, i * 80 + 40, width=1.2, fill="Black", tag="board")

        # draw circles on the board
        self.canvas.create_oval(200 - 4, 200 - 4, 200 + 4, 200 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(200 - 4, 520 - 4, 200 + 4, 520 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(520 - 4, 200 - 4, 520 + 4, 200 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(520 - 4, 520 - 4, 520 + 4, 520 + 4, fill="Black", outline="Black", tag="board")

        # draw discs
        for index, disc in enumerate(board.discs):
            center_x = 40 + int((index-1) % 10) * 80 + 40
            center_y = 40 + int((index-10) / 10) * 80 + 40
            if(disc == "Black"):    
                self.canvas.create_oval(center_x - 38, center_y - 38, center_x + 38, center_y + 38, fill="Black", outline="Black", tag="disc")
            elif(disc == "White"):    
                self.canvas.create_oval(center_x - 39, center_y - 39, center_x + 39, center_y + 39, fill="White", outline="Black", tag="disc")
            elif(disc == "CanPlace"):
                self.canvas.create_oval(center_x - 4, center_y - 4, center_x + 4, center_y + 4, fill="OliveDrab1", outline="OliveDrab1", tag="disc")
            # In case of the last placed disc, mark it
            if(index == board.newest_place):
                self.canvas.create_oval(center_x - 6, center_y - 6, center_x + 6, center_y + 6, fill="Red", outline="Red", tag="disc")

        # A ~ H, 1 ~ 8
        alphabet_list = [chr(i) for i in range(65, 65 + 8)]
        for index, alphabet in enumerate(alphabet_list):
            self.canvas.create_text(80 + index * 80, 20, text=alphabet, font = ('Helvetica', 12), tag='info')
            self.canvas.create_text(20, 80 + index * 80, text=str(index + 1), font = ('Helvetica', 12), tag='info')

        # draw the game info
        self.canvas.create_text(760, 50, text='Black : ', font = ('Helvetica', 12), justify=tk.LEFT, tag='info')
        self.canvas.create_text(760, 80, text='White : ', font = ('Helvetica', 12), justify=tk.LEFT, tag='info')
        self.canvas.create_text(820, 50, text=str(board.getDiscNum('Black')), font = ('Helvetica', 12), justify=tk.LEFT, tag='info')
        self.canvas.create_text(820, 80, text=str(board.getDiscNum('White')), font = ('Helvetica', 12), justify=tk.LEFT, tag='info')
        self.canvas.create_text(860, 50, text='discs', font = ('Helvetica', 12), justify=tk.LEFT, tag='info')
        self.canvas.create_text(860, 80, text='discs', font = ('Helvetica', 12), justify=tk.LEFT, tag='info')

        # draw player names
        self.canvas.create_oval(740 - 12, 130 - 12, 740 + 12, 130 + 12, fill="Black", outline="Black", tag='info')
        self.canvas.create_oval(740 - 12, 160 - 12, 740 + 12, 160 + 12, fill="White", outline="White", tag='info')
        self.canvas.create_text(820, 130, text=self.b_name, font = ('Helvetica', 12), justify=tk.LEFT, tag='info')
        self.canvas.create_text(820, 160, text=self.w_name, font = ('Helvetica', 12), justify=tk.LEFT, tag='info')

        self.canvas.pack()
        self.root.after(100, self.draw, board)