from piece import *
from draw import Draw
from AI import gameAI
from random import randint
import pygame
import os
from pygame.draw import rect

class mainSystem:

    def __init__(self):
        self.drawer = Draw()
        self.gameAI = gameAI()
        self.whitePieceArray = []
        self.blackPieceArray = []
        self.pieces = []
        self.checkmate = False
        self.piece = 0
        self.posArray = [['nul' for _ in range(8)] for _ in range(8)]
        self.gameArray = [['nul' for _ in range(8)] for _ in range(8)]
        self.fillWithNullObj()
        self.setInitialBoard()
        pygame.display.set_caption("chess NEA") 
        

    def gameRunner(self):
        drawred = False
        redx=0
        redy = 0
        run = True
        fps = 10
        clock = pygame.time.Clock()
        run = True
        
        while run:
            clock.tick(fps)
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #draw board
            self.drawer.drawBoard()

            
            self.updatePieces()
            
            
            #drawPieces
            self.gameArray = self.drawer.drawPieces(self.gameArray)

            self.piece = self.click()

            if self.checkmate == True:
                break

            typeOfClick = pygame.mouse.get_pressed()
            if typeOfClick[0] == True:
                mouseX, mouseY = pygame.mouse.get_pos()
                redx = int((mouseX -60 )/97.5)
                redy = int((mouseY -60 )/97.5)
                drawred = True
            if typeOfClick[2] == True:
                drawred = False
                redx = 0
                redy = 0
            

            self.drawer.drawRedBox(drawred,redx,redy)
            pygame.display.update()
        

    
    def click(self):

        typeOfClick = pygame.mouse.get_pressed()
    
        mouseX, mouseY = pygame.mouse.get_pos()
        
        x = int((mouseX -60 )/97.5)
        y = int((mouseY -60 )/97.5)

        if typeOfClick[0] == True and self.gameArray[y][x].name != 'null' and x>0 and y>0:

            self.clearPosArray()
            self.piece = self.gameArray[y][x]
            legalMoves = self.piece.possibleMoves(self.gameArray)

            legalMoves = self.getValidMoves(legalMoves,self.piece)
            self.createPositions(legalMoves)
            self.drawer.drawPositions(self.posArray)
            #possible return piece error
            self.checkmate = False
            return self.piece 
        
        #check for right click and piece has been selected
        if True == typeOfClick[2] and self.piece != 0:
            

            if self.piece.colour != 'b':
                
                #check if move is legal
                
                legalMoves = self.piece.possibleMoves(self.gameArray)
                

                legalMoves = self.getValidMoves(legalMoves,self.piece)
                
                

                if (y,x) in legalMoves:
                        
                    
                    null = nullObject(self.piece.row,self.piece.collumn,'n',0)

                    #if piece takes piece:
                    if self.gameArray[y][x].name != 'null':
                        self.pieces.remove(self.gameArray[y][x])
                        if self.gameArray[y][x].colour == 'w':
                            self.whitePieceArray.remove(self.gameArray[y][x])
                        elif self.gameArray[y][x].colour == 'b':
                            self.blackPieceArray.remove(self.gameArray[y][x])
                        self.gameArray[y][x] = nullObject(y,x,'n',0)
                    
                    #x refers to row, y refers to col
                    
                    self.gameArray[self.piece.row][self.piece.collumn] = null

                    # self.piece = new square 
                    self.piece.collumn = x
                    self.piece.row = y
                    self.gameArray[y][x] = self.piece
                    
                    self.piece = 0
                    self.clearPosArray()

                    #check for promote pawn
                    self.promotePawn()

                    # DO AI MOVE:
                    piecesToMoveStack, movesStack = self.gameAI.getBestMove(self.pieces,self.gameArray,self.blackPieceArray,self.whitePieceArray)
                    #gets a random move that ends up with the same evaluation as eachother
                    randomMoveInt = randint( 1,movesStack.size-1)
                    for _ in range(randomMoveInt):
                        move = movesStack.pop()
                        pieceToMove = piecesToMoveStack.pop()

                    legalAIMoves = self.getAllAIMoves(self.blackPieceArray)
                    pieceToMoveID = pieceToMove.id

                    #check if AI move is in legal moves

                    moveIsLegal = False
                    for legalAIMove in legalAIMoves:
                        if legalAIMove[len(legalAIMove)-1] == pieceToMoveID:
                            if move in legalAIMove:
                                moveIsLegal = True
                    if moveIsLegal:
                        self.gameAI.makeAiMove(pieceToMove,move,self.gameArray,self.pieces,self.blackPieceArray,self.whitePieceArray)
                    else:
                        k = 0
                        while moveIsLegal != True:

                            pieceToMove, move = self.gameAI.getRandomMove(self.blackPieceArray,self.gameArray)
                            legalAIMoves= self.getAllAIMoves(blackPieceArray)
                            pieceToMoveID = pieceToMove.id

                            #check if AI move is in legal moves

                            
                            moveIsLegal = False
                            for legalAIMove in legalAIMoves:
                                if legalAIMove[len(legalAIMove)-1] == pieceToMoveID:
                                    if move in legalAIMove:
                                        moveIsLegal = True
                            k+=1
                            if k >= 100:
                                self.checkmate = True
                                print('checkmate')
                                break
                        if moveIsLegal:
                            self.gameAI.makeAiMove(pieceToMove,move,self.gameArray,self.pieces,self.blackPieceArray,self.whitePieceArray)
                        
                    return self.piece
        self.checkmate = False
        return self.piece

    def getAllAIMoves(self, colourPieceArray):
        allMovesArray = []
        for piece in colourPieceArray:
            movesForCurrentPiece = piece.possibleMoves(self.gameArray)
            movesForCurrentPiece= self.getValidMoves(movesForCurrentPiece,piece)
            movesForCurrentPiece.append(piece.id)
            allMovesArray.append(movesForCurrentPiece)
        return allMovesArray

    def clearPosArray(self):
        for i in range(8):
                for j in range(8):
                    null = nullObject(i, j, 'n', -1)
                    self.addToGameArray(self.posArray, null)


    def promotePawn(self):
        for i in range(8):
            if self.gameArray[0][i].name == 'Pawn':
                self.whitePieceArray.remove(self.gameArray[0][i])
                self.pieces.remove(self.gameArray[0][i])
                self.gameArray[0][i] = Queen(i,0,'w','w_queen'+str(i))
                self.whitePieceArray.append(self.gameArray[0][i])
                self.pieces.append(self.gameArray[0][i])
            if self.gameArray[7][i].name == 'Pawn':
                self.blackPieceArray.remove(self.gameArray[7][i])
                self.pieces.remove(self.gameArray[0][i])
                self.gameArray[7][i] = Queen(i,7,'b','b_queen'+str(i))
                self.blackPieceArray.append(self.gameArray[7][i])
                self.pieces.append(self.gameArray[0][i])
       

    def setInitialBoard(self):
        b_bishop1 = Bishop(2,0,'b', 'b_bishop1')
        b_bishop2 = Bishop(5,0,'b','b_bishop2')
        w_bishop1 = Bishop(2,7,'w', 'w_bishop1')
        w_bishop2 = Bishop(5,7,'w', 'w_bishop2')

        b_knight1 = Knight(1,0,'b', 'b_knight1')
        b_knight2 = Knight(6,0,'b', 'b_knight2')
        w_knight1 = Knight(1,7,'w', 'w_knight1')
        w_knight2 = Knight(6,7,'w', 'w_knight2')

        b_rook1 = Rook(0,0,'b','b_rook1')
        b_rook2 = Rook(7,0,'b','b_rook2')
        w_rook1 = Rook(0,7,'w','w_rook1')
        w_rook2 = Rook(7,7,'w','w_rook2')
        
        b_queen = Queen(3,0,'b','b_queen')
        w_queen = Queen(3,7,'w', 'w_queen')

        b_king = King(4,0,'b', 'b_king')
        w_king = King(4,7,'w','w_king')

        b_pawn1 = Pawn(0,1,'b','b_pawn1')
        b_pawn2 = Pawn(1,1,'b','b_pawn2')
        b_pawn3 = Pawn(2,1,'b','b_pawn3')
        b_pawn4 = Pawn(3,1,'b','b_pawn4')
        b_pawn5 = Pawn(4,1,'b','b_pawn5')
        b_pawn6 = Pawn(5,1,'b','b_pawn6')
        b_pawn7 = Pawn(6,1,'b','b_pawn7')
        b_pawn8 = Pawn(7,1,'b','b_pawn8')
        
        w_pawn1 = Pawn(0,6,'w','w_pawn1')
        w_pawn2 = Pawn(1,6,'w','w_pawn2')
        w_pawn3 = Pawn(2,6,'w','w_pawn3')
        w_pawn4 = Pawn(3,6,'w','w_pawn4')
        w_pawn5 = Pawn(4,6,'w','w_pawn5')
        w_pawn6 = Pawn(5,6,'w','w_pawn6')
        w_pawn7 = Pawn(6,6,'w','w_pawn7')
        w_pawn8 = Pawn(7,6,'w','w_pawn8')
        
        self.whitePieceArray = [w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7, w_pawn8,w_rook1, w_rook2,w_bishop1, w_bishop2,w_knight1, w_knight2,w_king, w_queen]
        self.blackPieceArray = [b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7, b_pawn8,b_rook1, b_rook2,b_bishop1, b_bishop2,b_knight1, b_knight2,b_king, b_queen]
        self.pieces = [w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7, w_pawn8, b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7, b_pawn8, w_rook1, w_rook2, b_rook1, b_rook2, w_bishop1, w_bishop2, b_bishop1, b_bishop2, w_knight1, w_knight2, b_knight1, b_knight2, w_king, b_king, w_queen, b_queen]
        

        #set all object pieces on board

    def fillWithNullObj(self):
                #null object fill game array     
        for i in range(8):
            for j in range(8):
                null = nullObject(i, j, 'n', -1)
                self.addToGameArray(self.gameArray, null)
        #null object fill posArray
        for i in range(8):
            for j in range(8):
                null = nullObject(i, j, 'n', -1)
                self.addToGameArray(self.posArray, null)

#set all object pieces on board
    def updatePieces(self):
        for i in self.pieces:
            self.addToGameArray(self.gameArray, i)

    def addToGameArray(self, array, object):
        array[object.row][object.collumn] = object

    def getValidMoves(self, legalMoves,piece):
        #generate all possible moves for the
        moves = legalMoves
        #for each move make the move
        
        for i in range(len(moves)-1,-1,-1): # we have to go backwards to avoid error 
            originalPosition, currentPosition, pieceForUndo, takenPiece = self.makeMove(moves[i], piece)
            
        #for each of your opponents moves see if they attack your king
            if self.inCheck(piece.colour):
                moves.remove(moves[i]) #if they do then its not a valid move
            self.undoMove(originalPosition, currentPosition, pieceForUndo,takenPiece) #undo move
        
        return moves

    def makeMove(self,move,pieceToMove):
    
        null = nullObject(pieceToMove.row, pieceToMove.collumn,'n',0)
        #if piece takes piece:
        y = move[0]
        x = move[1] 
        takenPiece = None
        if self.gameArray[y][x].name != 'null':
            takenPiece = self.gameArray[y][x]
            self.pieces.remove(self.gameArray[y][x])
            if self.gameArray[y][x].colour == 'w':
                self.whitePieceArray.remove(self.gameArray[y][x])
            elif self.gameArray[y][x].colour == 'b':
                self.blackPieceArray.remove(self.gameArray[y][x])
            self.gameArray[y][x] = nullObject(y,x,'n',0)
            
        originalPosition = (pieceToMove.row , pieceToMove.collumn)
        self.gameArray[pieceToMove.row][pieceToMove.collumn] = null
        self.gameArray[move[0]][move[1]] = pieceToMove
        pieceToMove.collumn = move[0]
        pieceToMove.row = move[1]
        pieceForUndo = self.gameArray[move[0]][move[1]]
        currentPosition = (move[0], move[1])

        return originalPosition, currentPosition, pieceForUndo, takenPiece 

    def undoMove(self, originalPosition,currentPosition,pieceToMove, takenPiece):
        if takenPiece is not None:
            objToAdd = takenPiece
            if takenPiece.colour == 'w':
                self.whitePieceArray.append(takenPiece)
            else:
                self.blackPieceArray.append(takenPiece)
            self.pieces.append(takenPiece)
        else: 
            objToAdd = nullObject(currentPosition[0], currentPosition[1],'n',-1)
        self.gameArray[currentPosition[0]][currentPosition[1]] = objToAdd
        self.gameArray[originalPosition[0]][originalPosition[1]] = pieceToMove
        pieceToMove.row = originalPosition[0]
        pieceToMove.collumn = originalPosition[1]

    def createPositions(self,legalMoves):
        
        moves = legalMoves

        for move in moves:
            pos = positionObject(move[1],move[0])
            self.posArray[move[0]][move[1]] = pos
        
    #sees if the nemy can attack the square i, j
    def squareUnderAttack(self, y,x):
        if self.gameArray[y][x].colour == 'b':
            checkColour = 'w'
        if self.gameArray[y][x].colour == 'w':
            checkColour = 'b'
        
        attackMoves = []

        for i in range(8):
            for j in range(8):
                if self.gameArray[i][j].colour == checkColour:
                    attackMoves.append(self.gameArray[i][j].possibleMoves(self.gameArray))
        attackMoves = self.flatten(attackMoves)
        #attackMoves)
        
        kingUnderAttack = False
        for move in attackMoves:
            if move == (y,x):
                kingUnderAttack = True

        return kingUnderAttack


    #to make a 2d list a 1d list
    def flatten(self, input):
        new_list = []
        for i in input:
            if i != None:
                for j in i:
                    new_list.append(j)
        return new_list

    def getValidSingularMove(self, legalMove,piece):
        #generate all possible moves for the
        move = legalMove
        inCheckBool = False
        #for each move make the move
        originalPosition, currentPosition, pieceForUndo, takenPiece = self.makeMove(move, piece)
        
        #for each of your opponents moves see if they attack your king
        if self.inCheck(piece.colour):
            inCheckBool = True #if they do then its not a valid move
        self.undoMove(originalPosition, currentPosition, pieceForUndo,takenPiece) #undo move

        return inCheckBool
    

    #sees if the current player is in check
    def inCheck(self, colourToMove):
        kingLocation = self.getKingLocation(colourToMove)
        
        return self.squareUnderAttack(kingLocation[0],kingLocation[1])


    #gets the location on the game array of the king of the specified colour
    def getKingLocation(self, colour):
        for i in range(8):
            for j in range(8):
                
                if self.gameArray[i][j].name == 'King' and self.gameArray[i][j].colour == colour:
                    return i,j

    def index2D(myList, v):
        for i, x in enumerate(myList):
            if v in x:
                return (i, x.index(v))

if __name__ == '__main__':
    newGame = mainSystem()
    checkmate = newGame.gameRunner()