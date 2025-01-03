from tkinter import Tk, Button
from tkinter.font import Font
import time
from state import *
from alphaBeta import *

level = 1
first = "h"
start = time.time()

class GUI:
    def __init__(self):
        self.stats = SearchStats()
        self.game = State(nextPlayer=human_player)
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.geometry("300x450")  
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=16)  
        self.buttons = {}

        self.app.configure(bg="#333333")
        self.button_bg = "#555555"
        self.button_fg = "#FFFFFF"

        for x, y in self.game.table:
            handler = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=handler, font=self.font, width=4, height=2,
                            bg=self.button_bg, fg=self.button_fg)
            button.grid(row=x, column=y, padx=5, pady=5)  
            self.buttons[x, y] = button

        reset_button = Button(self.app, text='Reset', command=self.reset, 
                              bg=self.button_bg, fg=self.button_fg)
        reset_button.grid(row=size + 1, column=0, columnspan=size, sticky='WE', padx=5, pady=5)

        self.update()
        if first == "c":
            self.game.nextPlayer = computer_player
            self.computer_move()

    def reset(self):
        self.stats.reset()
        self.game = State(nextPlayer=human_player)
        self.update()
        self.app.destroy() 
        Select().mainloop()  

    def move(self, x, y):
        global level
        self.app.config(cursor="watch")
        self.app.update()
        self.game.table[x, y] = human_player
        self.game.nextPlayer = computer_player
        self.update()
        if TERMINAL_TEST(self.game)[0]:
            return
        self.computer_move()

    def computer_move(self):
        if level == 3:
            self.game.depth = 0
            self.stats.maxDepth = 5
            # self.game = minimax_no_pruning(self.game, time.time(), self.stats, 3)
            self.game = alpha_beta_search_pruning(self.game, time.time(), self.stats, 3)
            self.stats.print()
            self.stats.reset()
        elif level == 2:
            self.game.depth = 0
            self.stats.maxDepth = 2
            # self.game = minimax_no_pruning(self.game, time.time(), self.stats, 2)
            self.game = alpha_beta_search_pruning(self.game, time.time(), self.stats, 2)
            self.stats.print()
            self.stats.reset()
        elif level == 1:
            self.game.depth = 0
            self.stats.maxDepth = 1
            # self.game = minimax_no_pruning(self.game, time.time(), self.stats, 1)
            self.game = alpha_beta_search_pruning(self.game, time.time(), self.stats, 1)
            self.stats.print()
            self.stats.reset()
        self.update()
        self.app.config(cursor="")

    def update(self):
        for (x, y) in self.game.table:
            text = self.game.table[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'black'
            self.buttons[x, y]['state'] = 'normal' if text == empty else 'disabled'
        winning = TERMINAL_TEST(self.game)[0]
        if winning:
            winner = self.game.won(player=other_player(self.game.nextPlayer))
            if winner:
                for x, y in winner:
                    self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        for (x, y) in self.game.table:
            self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()


class SearchStats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cutOffOccured = False
        self.maxDepthReached = 0
        self.totalNodes = 0
        self.pruningMax = 0
        self.pruningMin = 0
        self.maxDepth = 5

    def print(self):
        print("-----------------------")
        print("Statistics of the Move")
        print(f"Cutoff Occured: {self.cutOffOccured}")
        print(f"Maximum Depth Reached: {self.maxDepthReached}")
        print(f"Total number of nodes generated: {self.totalNodes}")
        print(f"Number of times pruning occurred within Max-Value: {self.pruningMax}")
        print(f"Number of times pruning occurred within Min-Value: {self.pruningMin}")


class Select:
    def __init__(self):
        self.app = Tk()
        self.app.title('Select Who Goes First')
        self.app.geometry("300x200")  
        self.font = Font(family="Helvetica", size=16)

        self.app.configure(bg="#333333")
        self.button_bg = "#555555"
        self.button_fg = "#FFFFFF"
        
        question_label = Button(self.app, text="Select who goes first", font=self.font, 
                                bg="#333333", fg="#FFFFFF", relief="flat", activeforeground="#FF3333", 
                                width=20, height=2)
        question_label.grid(row=0, column=0, columnspan=2, pady=20)  

        computer_handle = lambda: self.choose("c")
        human_handle = lambda: self.choose("h")

        b1 = Button(self.app, text='Computer', command=computer_handle, 
                    bg=self.button_bg, fg=self.button_fg, width=10, height=2)
        b1.grid(row=1, column=0, padx=10, pady=10)  

        b2 = Button(self.app, text='Human', command=human_handle, 
                    bg=self.button_bg, fg=self.button_fg, width=10, height=2)
        b2.grid(row=1, column=1, padx=10, pady=10)  

    def choose(self, selected_first):
        global first
        first = selected_first
        self.app.destroy()
        SelectLevel().mainloop()

    def mainloop(self):
        self.app.mainloop()

class SelectLevel:
    def __init__(self):
        self.app = Tk()
        self.app.title('Select Difficulty Level')
        self.app.geometry("300x300") 
        self.font = Font(family="Helvetica", size=16)

        self.app.configure(bg="#333333")
        self.button_bg = "#555555"
        self.button_fg = "#FFFFFF"
        
        question_label = Button(self.app, text="Select Difficulty Level", font=self.font, 
                                bg="#333333", fg="#FFFFFF", relief="flat", activeforeground="#FF3333", 
                                width=20, height=2)
        question_label.grid(row=0, column=0, columnspan=2, pady=20) 

        easy_handle = lambda: self.choose_level(1)
        medium_handle = lambda: self.choose_level(2)
        hard_handle = lambda: self.choose_level(3)

        button_easy = Button(self.app, text='Easy', command=easy_handle, 
                             bg=self.button_bg, fg=self.button_fg, width=10, height=2)
        button_easy.grid(row=1, column=0, padx=10, pady=10)  

        button_medium = Button(self.app, text='Medium', command=medium_handle, 
                               bg=self.button_bg, fg=self.button_fg, width=10, height=2)
        button_medium.grid(row=1, column=1, padx=10, pady=10) 

        button_hard = Button(self.app, text='Hard', command=hard_handle, 
                             bg=self.button_bg, fg=self.button_fg, width=10, height=2)
        button_hard.grid(row=2, column=0, columnspan=2, padx=10, pady=10)  

    def choose_level(self, selected_level):
        global level
        level = selected_level
        self.app.destroy()
        GUI().mainloop()

    def mainloop(self):
        self.app.mainloop()


Select().mainloop()
