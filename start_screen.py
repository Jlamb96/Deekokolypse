from graphics import start_logo
import tkinter as tk
from tkinter import *
import sys
from game_menu import GameStats
import pygame
pygame.mixer.init()
class intro():
    def __init__(self):
        self.FONT_NAME = "Courier"

        self.window = Tk()
        self.window.title("Deekokolypse")
        self.window.iconbitmap("favicon.ico")
        self.window.config(bg="black")
        self.continue_button = Button(text="Continue", command=self.start_game, font=18)
        self.continue_button.grid(column=1, row=3)
        self.help_button = Button(text="Help", font=18)
        self.help_button.grid(column=0, row=3)
        self.exit_button = Button(text="Exit(coward)", command=self.exit_game, font=18)
        self.exit_button.grid(column=2, row=3)
        self.logo_label = Label(text=start_logo, font=("Courier", 10), fg="green", bg="black")
        self.logo_label.grid(column=1, row=1)
        self.logo_label.config(width=100, height=20, padx=100, pady=100)
        self.hello = Label(text="You have been stranded alone. You have 2 weeks.\n A game by Jeremy",
                         font=("Courier", 15, "bold"), pady=40, bg="black", fg="white")
        self.hello.grid(column=1, row=2)
        self.window.mainloop()


    def start_game(self):
        self.window.destroy()
        GameStats()
        return True


    def exit_game(self):
        sys.exit()




