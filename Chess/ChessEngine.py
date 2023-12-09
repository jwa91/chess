"""
Deze class gaat verantwoordelijk zijn voor het bewaren van alle informatie over de huidige status van het spel.
het gaat ook verantwoordelijk zijn voor het bepalen van de geldige zetten, en hij heeft ie een move log.
"""

class GameState():
    def __init__(self):
        #bord is een 8x8 2d list. Elk element op de lijst heeft 2 karakters.
        #het 1e karakter is de kleur, 'b' or 'w'.
        #the 2e karakter is het type stuk, 'K', 'Q', 'R', 'B', 'N' or 'p'.
        #"--" - voor lege vakken.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                            'B': self.getBishopMoves,  'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.movelog = []

    '''
    neemt een zet als een parameter en voert hem uit. (gaat niet werken voor rokkade, promotie en passant)
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) # log de zet, voor ongedaan maken en naspelen
        self.whiteToMove = not self.whiteToMove #verandert wie aan zet is

    '''
    maak de laatste zet ongedaan
    '''

    def undomove(self):
        if len(self.movelog) !=0: # is er een zet om ongedaan te maken.
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not  self.whiteToMove

    '''
    Alle zetten rekening houdend met schaak
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() #voor nu houden we geen rekening met checks, fixen we later.

    '''
    Alle zetten zonder rekening te houden met schaak
    '''
    def getAllPossibleMoves(self):
        moves = [Move]
        for r in range(len(self.board)): #aantal rijen
            for c in range(len(self.board[r])): #aantal kolommen in een bepaalde rij
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #called de movefunction die past bij het stuk
        return moves

    '''
    Get alle pion zetten voor de pion op een bepaalde rij, call en add deze zetten op de lijst.
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #witte pion zetten
            if self.board[r-1][c] == "--": # 1 vak pion zetten
                moves.append(Move((r, c),(r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 vak pion zetten
                    moves.append(Move((r, c),(r-2,c), self.board))
            if c-1 >= 0: #je kunt niet slaan buiten het bord, dit zijn slagen naar links
                if self.board[r-1][c-1][0] == 'b': #er staat een zwart stuk linksvoor het witte stuk
                    moves.append(Move((r, c),(r-1,c-1), self.board))
            if c+1 <= 7: #slagen naar rechts
                if self.board[r-1][c+1][0] == 'b': #er staat een zwart stuk rechtsvoor het witte stuk
                    moves.append(Move((r, c),(r-1,c+1), self.board))
        else: #blackpawnmoves
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # Capture to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''
    zelfde voor de toren zetten
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # omhoog, links, omlaag, rechts

        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == "--":  # Leeg vak, geldige zet
                        moves.append(Move((r, c), (nr, nc), self.board))
                    else:
                        if self.board[nr][nc][0] != self.board[r][c][0]:  # Capture tegenstander's stuk
                            moves.append(Move((r, c), (nr, nc), self.board))
                        if self.board[nr][nc][0] == 'w' and self.board[r][c][0] == 'w':
                            break  # Stop witte torenbeweging na het bereiken van een eigen wit stuk
                        elif self.board[nr][nc][0] == 'b' and self.board[r][c][0] == 'b':
                            break  # Stop zwarte torenbeweging na het bereiken van een eigen zwart stuk
                        else:
                            moves.append(Move((r, c), (nr, nc), self.board))
                            break  # Stop na het blokkeren van het pad door een ander stuk
                else:
                    break  # Stop in deze richting als buiten het bord

    '''
    zelfde voor de Paard zetten
    '''

    def getKnightMoves(self, r, c, moves):
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == "--" or self.board[nr][nc][0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (nr, nc), self.board))

    '''
    zelfde voor de loper zetten
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Diagonale richtingen
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == "--":  # Leeg vak, geldige zet
                        moves.append(Move((r, c), (nr, nc), self.board))
                    else:
                        if self.board[nr][nc][0] != self.board[r][c][0]:  # Capture tegenstander's stuk
                            moves.append(Move((r, c), (nr, nc), self.board))
                        break  # Stop na het vangen, want verdere beweging wordt geblokkeerd door een stuk
                    if self.whiteToMove and self.board[nr][nc][0] == 'w':
                        break  # Stop witte loperbeweging na het bereiken van een eigen wit stuk
                    elif not self.whiteToMove and self.board[nr][nc][0] == 'b':
                        break  # Stop zwarte loperbeweging na het bereiken van een eigen zwart stuk
                else:
                    break  # Stop in deze richting als buiten het bord

    '''
    zelfde voor de Dame zetten
    '''

    def getQueenMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  # Alle richtingen
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == "--":  # Leeg vak, geldige zet
                        moves.append(Move((r, c), (nr, nc), self.board))
                    else:
                        if self.board[nr][nc][0] != self.board[r][c][0]:  # Capture tegenstander's stuk
                            moves.append(Move((r, c), (nr, nc), self.board))
                        break  # Stop na het vangen, want verdere beweging wordt geblokkeerd door een stuk
                    if self.whiteToMove and self.board[nr][nc][0] == 'w':
                        break  # Stop witte damebeweging na het bereiken van een eigen wit stuk
                    elif not self.whiteToMove and self.board[nr][nc][0] == 'b':
                        break  # Stop zwarte damebeweging na het bereiken van een eigen zwart stuk
                else:
                    break  # Stop in deze richting als buiten het bord

    '''
    zelfde voor de Koning zetten
    '''

    def getKingMoves(self, r, c, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Alle richtingen
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == "--" or self.board[nr][nc][0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (nr, nc), self.board))


class Move():
    # mapt keys naar waardes
    # key : waarde
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        '''
        Overriden van de equals method
        '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # moet nog iets verbeterd worden voor echte schaak notatie.
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]