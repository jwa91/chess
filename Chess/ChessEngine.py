"""
Deze class gaat verantwoordelijk zijn voor het bewaren van alle informatie over de huidige status van het spel.
het gaat ook verantwoordelijk zijn voor het bepalen van de geldige zetten, en hij heeft ie een move log.
"""


class GameState():
    def __init__(self):
        # bord is een 8x8 2d list. Elk element op de lijst heeft 2 karakters.
        # het 1e karakter is de kleur, 'b' or 'w'.
        # the 2e karakter is het type stuk, 'K', 'Q', 'R', 'B', 'N' of 'p'.
        # "--" - voor lege vakken.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    '''
    neemt een zet als een parameter en voert hem uit. (gaat niet werken voor rokkade, promotie en passant)
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)  # log de zet, voor ongedaan maken en naspelen
        self.whiteToMove = not self.whiteToMove  # verandert wie aan zet is
        #update locatie van de koning als de koning van plaats verandert.
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    '''
    maak de laatste zet ongedaan
    '''

    def undoMove(self):
        if len(self.movelog) != 0:  # is er een zet om ongedaan te maken.
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #positie van de koning
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    '''
    Alle zetten rekening houdend met schaak
    '''

    def getValidMoves(self):
        #eerst alle mogelijke zetten genereren
        moves = self.getAllPossibleMoves()
        #dan de zet maken
        for i in range(len(moves) -1, -1, -1): #handiger om achteraan te beginnen
            self.makeMove(moves[i])
            #na elke zet elke tegenstander zet genereren
            #na elke tegenstander zet kijken of die zet de koning aan valt
            self.whiteToMove = not self.whiteToMove #eerst weer terugveranderen van zetten
            if self.inCheck():
                moves.remove(moves[i]) #als ze de koning aanvallen, is het geen geldige zet
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #of schaakmat of pad
            if self.incheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    '''
    bepalen of de huidige speler schaak staat
    '''

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Bepalen of de tegenstander het vak kan aanvallen (self, r, c)
    '''

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #POV van tegenstander
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #veld onder aanval
                return True
        return False

    '''
    Alle zetten zonder rekening te houden met schaak
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # aantal rijen
            for c in range(len(self.board[r])):  # aantal kolommen in een bepaalde rij
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # called de movefunction die past bij het stuk
        return moves

    '''
    Get alle pion zetten voor de pion op een bepaalde rij, call en add deze zetten op de lijst.
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # witte pion zetten
            if self.board[r - 1][c] == "--":  # 1 vak pion zetten
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 vak pion zetten
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # je kunt niet slaan buiten het bord, dit zijn slagen naar links
                if self.board[r - 1][c - 1][0] == 'b':  # er staat een zwart stuk linksvoor het witte stuk
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # slagen naar rechts
                if self.board[r - 1][c + 1][0] == 'b':  # er staat een zwart stuk rechtsvoor het witte stuk
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # blackpawnmoves
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
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]

                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    '''
    zelfde voor de loper zetten
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # top-left, top-right, bottom-left, bottom-right
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]

                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    '''
    zelfde voor de Dame zetten
    '''

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

        '''
        zelfde voor de Paard zetten
        '''

    def getKnightMoves(self, r, c, moves):
        knightmoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightmoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    zelfde voor de Koning zetten
    '''

    def getKingMoves(self, r, c, moves):
        kingmoves = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Alle richtingen
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingmoves[i][0]
            endCol = c + kingmoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


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
