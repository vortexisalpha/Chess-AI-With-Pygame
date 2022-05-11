import random
from piece import *

class gameAI:

    #evaluate the current possition of the board
    def getScore(self, gameArray):
        score = 0
        pieceScore = {
        'King': 0,
        'Quee': 10,
        'Rook': 5,
        'Bish': 3,
        'Knig': 3,
        'Pawn': 1
        }   

        #checkMate = 1000
        #staleMate = 0

        for i in range(8):
            for j in range(8):
                if gameArray[i][j].colour == 'w':
                    score += pieceScore[gameArray[i][j].name]
                if gameArray[i][j].colour == 'b':
                    score -= pieceScore[gameArray[i][j].name]

        return score



    def getMovesThatAreNotNull(self,array):
        tempArray = []
        for moves in array:
            if len(moves) != 1:
                tempArray.append(moves)
        array = tempArray
        return array
        
    def getAllColourMoves(self,colourPieceArray,gameArray):
        allMovesArray = []
        for piece in colourPieceArray:
            movesForCurrentPiece = piece.possibleMoves(gameArray)
            movesForCurrentPiece.append(piece.id)
            allMovesArray.append(movesForCurrentPiece)
            
        return allMovesArray

    #find piece recursive function 
    def findPieceRecursive(self,gameArray,pieceID,j):
        for i in range(8):
            if gameArray[j][i].id == pieceID:
                return gameArray[j][i]
        
        return self.findPieceRecursive(gameArray,pieceID, j+1)

    #evaluate the best move to do in a situation
    def getBestMove(self,pieces,gameArray,blackPieceArray,whitePieceArray):
        

        maxScoreArray = []
        bestMoveArray = []
        bestMovePieceArray = []
        
        #getAllAiMoves:
        allBlackMoves = self.getAllColourMoves(blackPieceArray, gameArray)

        #condition array get rid of pieces with no moves.
        allBlackMoves = self.getMovesThatAreNotNull(allBlackMoves)
        
        
        # loop through black moves and get move then make move for each possible black move
        for aiMove in allBlackMoves:
            pieceID = aiMove[len(aiMove)-1]
            #finds the piece we are moving from the piece ID
            pieceToMove = self.findPieceRecursive(gameArray,pieceID,0)

            for i in range(len(aiMove)-1):
                currentAiMove = aiMove[i]
                
                
                #does move
                prevMove,prevPiece,pieceTaken,pieces,blackPieceArray, whitePieceArray, = self.makeAiMove(pieceToMove, currentAiMove, gameArray,pieces,blackPieceArray,whitePieceArray)
                
                #at this point we want to get the maximum score white can get in this position.
                #get All opponent return Moves:
                allWhiteMoves = self.getAllColourMoves(whitePieceArray,gameArray)
                #condition array get rid of pieces with no moves.
                allWhiteMoves = self.getMovesThatAreNotNull(allWhiteMoves)
            
                for oppMove in allWhiteMoves:
                    maxScore = -1000  
                    pieceOppID = oppMove[len(oppMove)-1]
                    #finds the piece we are moving from the piece ID
                    for a in range(8):
                        for b in range(8):
                            if gameArray[a][b].id == pieceOppID:
                                pieceOppToMove = gameArray[a][b]
                                break
                    for opp in range(len(oppMove)-1):
                        currentOppMove = oppMove[opp]
                        #does the opponent move
                        prevOppMove,prevOppPiece,pieceOppTaken,pieces,blackPieceArray, whitePieceArray, = self.makeAiMove(pieceOppToMove, currentOppMove, gameArray,pieces,blackPieceArray,whitePieceArray)


                
                        #evaluates the score of this sequence of moves
                        score = self.getScore(gameArray)
                        
                        #get the maximum score for the opponent
                        if score > maxScore:
                            maxScore = score
                            bestMove = currentAiMove
                            bestMovePiece = pieceToMove
                        currentOppPosition = (pieceOppToMove.row,pieceOppToMove.collumn)
                        gameArray,whitePieceArray,blackPieceArray, pieces = self.undoAiMove(pieceOppTaken,pieces,currentOppPosition, prevOppMove, prevOppPiece,whitePieceArray,blackPieceArray,gameArray)
        
                    maxScoreArray.append(maxScore)
                    bestMoveArray.append(bestMove)
                    bestMovePieceArray.append(bestMovePiece)
                    
                #AI undoes the move
                currentPosition = (pieceToMove.row,pieceToMove.collumn)
                gameArray,whitePieceArray,blackPieceArray, pieces = self.undoAiMove(pieceTaken,pieces,currentPosition, prevMove, prevPiece,whitePieceArray,blackPieceArray,gameArray)
        #gets the minimum of the maximium score array
        minimumMaximum = 10000
        indexOfMiniMax = 10000
        
        for index in range(len(maxScoreArray)-1):
            if minimumMaximum > maxScoreArray[index]:
                minimumMaximum = maxScoreArray[index]
                indexOfMiniMax = index
        bestMovePieces = []
        bestMoves = []
        for i in range(len(maxScoreArray)-1):
            if maxScoreArray[i] == maxScoreArray[indexOfMiniMax]:
                bestMovePieces.append(bestMovePieceArray[i])
                bestMoves.append(bestMoveArray[i])
        
        #stack stuff
        AIMoveStack = stack(len(bestMoves))
        AIMovePiecesStack = stack(len(bestMovePieces))

        for move in bestMoves:
            AIMoveStack.push(move)

        for piece in bestMovePieces:
            AIMovePiecesStack.push(piece)

        return AIMovePiecesStack, AIMoveStack


    


    def makeAiMove(self,pieceToMove, move, gameArray,pieces,blackPieceArray, whitePieceArray):
        
        y = move[0]
        x = move[1]
        prevMove = (pieceToMove.row, pieceToMove.collumn)
        null = nullObject(pieceToMove.row,pieceToMove.collumn,'n',0)

    
        #if piece takes piece:
        pieceTaken = None
        if gameArray[y][x].name != 'null':
            #remove it from piece array
            pieces.remove(gameArray[y][x])
            
            if gameArray[y][x].colour == 'w':   
                pieceTaken = gameArray[y][x]
                #remove it from white piece array if it is a white piece
                whitePieceArray.remove(gameArray[y][x])
                
            if gameArray[y][x].colour == 'b':
                pieceTaken = gameArray[y][x]
                #remove it from black piece array if it is a black piece
                blackPieceArray.remove(gameArray[y][x])
            

            gameArray[y][x] = nullObject(y,x,'n',0)
    #x refers to row, y refers to col
        
        gameArray[pieceToMove.row][pieceToMove.collumn] = null

        # piece = new square 
        pieceToMove.collumn = x
        pieceToMove.row = y
        gameArray[y][x] = pieceToMove
        return prevMove, pieceToMove, pieceTaken,pieces,blackPieceArray, whitePieceArray,

    def undoAiMove(self,takenPiece,pieces,currentPosition, originalPosition, pieceToMove,whitePieceArray,blackPieceArray,gameArray):
        
        if takenPiece is not None:
            objToAdd = takenPiece
            if takenPiece.colour == 'w':
                whitePieceArray.append(takenPiece)
            else:
                blackPieceArray.append(takenPiece)

            pieces.append(takenPiece)
        else: 
            objToAdd = nullObject(currentPosition[0], currentPosition[1],'n',-1)
        gameArray[currentPosition[0]][currentPosition[1]] = objToAdd
        gameArray[originalPosition[0]][originalPosition[1]] = pieceToMove
        pieceToMove.row = originalPosition[0]
        pieceToMove.collumn = originalPosition[1]

        return gameArray,whitePieceArray,blackPieceArray, pieces

    def addPieceTakenBack(self,pieceTaken,whitePieceArray,blackPieceArray,gameArray):
        if pieceTaken.colour == 'w':
            whitePieceArray.append(pieceTaken)
            
            gameArray[pieceTaken.row][pieceTaken.collumn] = pieceTaken
        if pieceTaken.colour == 'b':
            blackPieceArray.append(pieceTaken)
            gameArray[pieceTaken.row][pieceTaken.collumn] = pieceTaken
        return whitePieceArray,blackPieceArray, gameArray




    def getRandomMove(self,blackPieceArray,gameArray):
        allMovesArray = []
        for piece in blackPieceArray:
            movesForCurrentPiece = piece.possibleMoves()
            movesForCurrentPiece.append(piece.id)
            allMovesArray.append(movesForCurrentPiece)

        tempArray = []
        for moves in allMovesArray:
            if len(moves) != 1:
                tempArray.append(moves)

        allMovesArray = tempArray
        randomInt = random.randint(0, len(allMovesArray)-1)
        moveArray = allMovesArray[randomInt]
        
        pieceToMoveId = moveArray[len(moveArray)-1]
        randomMoveNum = random.randint(0, len(moveArray)-2)
        randomMove = moveArray[randomMoveNum]
        
        for i in range(8):
            for j in range(8):
                if gameArray[i][j].id == pieceToMoveId:
                    randomPieceToMove = gameArray[i][j]

        return randomPieceToMove, randomMove

class stack:
    def __init__(self, size):
        self.end = 0
        self.dataStack = []
        self.size = size

    def pop(self): 
        if bool(self.end): #override bool command
            self.end -=1
            return self.dataStack[self.end]
        else:
            raise IndexError('stack underflow error')

    def push(self, data):
        if self.end < self.size:
            self.end +=1
            self.dataStack.append(data)
        else:
            raise IndexError('stack overflow error')