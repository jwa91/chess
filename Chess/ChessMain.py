"""
Dit is onze main driver file. Verantwoordelijk voor de user input en het weergeven van de current GameState object.
"""

import pygame as p
from Chess import ChessEngine


WIDTH = HEIGHT = 512  # pixels hoogte en breedte, niet hoger dan 512 ivm. het feit dat images dan vaag worden
DIMENSION = 8  # een schaakbord is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # voor animaties al vast.
IMAGES = {}

'''
Initieer een global dictionary van de plaatjes van de stukken. Deze halen we maar 1x op in de main. 
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'wp', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note: we can access an image by saying 'IMAGES['wp']'

'''
Dit is de main driver van de code. Deze zal de user input afhandelen en de graphics updaten. 
'''
def main():
    p.init()
    screen      = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable voor als er een zet is gedaan
    loadImages() # doe dit maar 1x, voor de while loop.
    running = True
    sqSelected = () # geen square is geselecteerd initieel, houdt de last click van de user bij,tuple: row, colum)
    playerClicks = [] # houdt de player clicks bij (twee tuples: [(6,4), (4,4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) locatie van de muis
                col = location [0]//SQ_SIZE
                row = location [1]//SQ_SIZE
                if sqSelected == (row, col): # de user klikte 2x op zelfde vak
                    sqSelected = () # deselect
                    playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append voor zowel 1e als 2e clicks
                if len(playerClicks) == 2: #was na 2e click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # maak zet ongedaan wanneer 'z'  is ingedrukt
                    gs.undoMove()
                    validMoves = gs.getValidMoves()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState (screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Verantwoordelijk voor alle graphics binnen de huidige gamestate.
'''
def drawGameState(screen, gs):
    drawBoard(screen) # teken de vakken op het bord
    #teken in stukken, highlighting en zet suggesties
    drawPieces(screen, gs.board) # teken de stukken boven op de vakken

'''
Teken de vakken op het bord. linksboven is altijd wit. 
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Teken de stukken op het bord, voortbordurend op de huidige GameState.board.
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
























