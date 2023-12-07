"""
This class is going to be responsible for storing all the information about the current state of a chess game.
It will also be responsible for determiting the valid moves at the current state. It will also keep a move log.
"""

class GameState():
    def __init__(self):
        #board is an 8x8 2d list. Each element of the list has 2 characters.
        #the first character represents the color of the piece, 'b' or 'w'.
        #the second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'p'.
        #"--" - represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whitetomove = True
        self.movelog = []