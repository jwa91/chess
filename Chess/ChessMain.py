"""
This is our main driver file. It wil be responsible for user input and displaying the current GameState object.
"""

import pygame as p
from Chess import ChessEngine


WIDTH = HEIGHT = 512  # pixels hoogte en breedte, niet hoger dan 512 ivm. het feit dat images dan vaag worden
DIMENSION = 8  # een schaakbord is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # voor animaties al vast.
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main. 
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'wp', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note: we can access an image by saying 'IMAGES['wp']'

'''
This will  be the main driver of our code. this will handle user input and updating the graphics. 
'''
def main():
    p.init()
    screen      = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() # only do this once, before the while loop.
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState (screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current gamestate
'''
def drawGameState(screen, gs):
    drawBoard(screen) # draw the squares on the board.
    #draw in piece highlighting and move suggestions
    drawPieces(screen, gs.board) # draw the pieces on top of the squares

'''
Draw the squares on the board. The topleft square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board.
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
























