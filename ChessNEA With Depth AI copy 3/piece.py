import pygame
import os
import time
from pygame.sprite import collide_circle



whitePieceArray = []
whitePieceWordArray = ['w_bishop', 'w_king','w_knight', 'w_pawn', 'w_queen', 'w_rook']

for i in range(len(whitePieceWordArray)):
    whitePieceArray.append(pygame.transform.scale(pygame.image.load(os.path.join("img", whitePieceWordArray[i] + ".png")), ((780//8)-20,(780//8)-20)))

blackPieceArray = []
blackPieceWordArray = ['b_bishop', 'b_king','b_knight', 'b_pawn', 'b_queen', 'b_rook']
for i in range(len(blackPieceWordArray)):
    blackPieceArray.append(pygame.transform.scale(pygame.image.load(os.path.join("img", blackPieceWordArray[i] + ".png")), ((780//8)-20,(780//8)-20)))
posPieceArray = []
posPieceWordArray = ['ball']
for i in range(len(posPieceWordArray)):
    posPieceArray.append(pygame.transform.scale(pygame.image.load(os.path.join("img", posPieceWordArray[i] + ".png")), ((780//8)-20,(780//8)-20)))


class Piece:

    def __init__(self, collumn, row, colour, imageIndex, name,id):
        self.collumn = collumn
        self.row = row
        self.colour = colour
        self.imageIndex = imageIndex
        self.name = name
        self.id = id

    def draw(self, win):
        if self.colour == 'w':
            drawPiece = whitePieceArray[self.imageIndex]
        elif self.colour == 'b':
            drawPiece = blackPieceArray[self.imageIndex]
        elif self.colour == 'p':
            drawPiece = posPieceArray[self.imageIndex]
        x = (self.row * (780/8)) + 70
        y = (self.collumn * (780/8)) + 70

        win.blit(drawPiece, (y,x))
        
    def remove(self):
        self.collumn = -1
        self.row = -1

    def possibleMoves(self,gameArray):
        return None

class nullObject(Piece):
    def __init__(self,collumn,row,colour,imageIndex):
        super().__init__(collumn,row,colour,imageIndex,"null",'n')

class positionObject(Piece):
    def __init__(self,collumn,row):
        super().__init__(collumn,row,"p",0,"posi",'p')

class castleObject(Piece):
    def __init__(self,collumn,row,colour,imageIndex):
        super().__init__(collumn,row,colour,imageIndex,"cast")   

class indicatorObject(Piece):
    def __init__(self,collumn,row,colour,imageIndex,id):
        super().__init__(collumn,row,colour,imageIndex,"indd")

class Bishop(Piece):  
    def __init__(self,collumn,row,colour,id):
        super().__init__(collumn,row,colour,0,"Bish",id)

    def possibleMoves(self,gameArray):
        y = self.row
        x = self.collumn
        moves = []
         
        
        for yvar in range(2):
            if yvar == 0:
                ky = 1
            if yvar == 1:
                ky = -1
            
            for xvar in range(2):
                if xvar == 0:
                    kx = 1
                if xvar == 1:
                    kx = -1
                try: 
                    i=1
                    while gameArray[y+(i*ky)][x+(i*kx)].colour == 'n' and y+(i*ky)>=0  and x+(i*kx) >=0 and y+(i*ky)<=7  and x+(i*kx) <=7:
                            if gameArray[y+(i*ky)][x+(i*kx)].colour != self.colour:
                                moves.append((y + (i*ky), x + (i*kx)))
                            else:
                                break
                            i+=1        
                except Exception as e:
                    pass
                try:
                    if gameArray[y+(i*ky)][x+(i*kx)].colour != self.colour and y+(i*ky)>=0  and x+(i*kx) >=0 and y+(i*ky)<=7  and x+(i*kx) <=7:
                        moves.append((y+(i*ky), x+(i*kx)))
                    i+=1
                except Exception as e:
                    pass
        return moves

class King(Piece):  
    def __init__(self,collumn,row,colour,id):
        super().__init__(collumn,row,colour,1,"King",id)

    def possibleMoves(self,gameArray):
        y = self.row
        x = self.collumn
        moves = []
        cast = []
         
        
        for yvar in range(2):
            if yvar == 0:
                ky = 1
            if yvar == 1:
                ky = -1
            
            for xvar in range(2):
                if xvar == 0:
                    kx = 1
                if xvar == 1:
                    kx = -1
                i=1
                try: 
                    if gameArray[y+(i*ky)][x+(i*kx)].colour != self.colour and y+(i*ky)>=0  and x+(i*kx) >=0 and y+(i*ky)<=7  and x+(i*kx) <=7:
                        moves.append((y+(i*ky), x+(i*kx)))
                except Exception as e:
                    pass
        for yvar in range(2):
            if yvar == 0:
                ky = 1
            if yvar == 1:
                ky = -1  

            try: 
                if gameArray[y+(i*ky)][x].colour != self.colour and y+(i*ky)>=0  and x >=0 and y+(i*ky)<=7  and x <=7:
                    moves.append((y+(i*ky), x))
            except Exception as e:
                pass

        for xvar in range(2):
                if xvar == 0:
                    kx = 1
                if xvar == 1:
                    kx = -1
                try: 
                    if gameArray[y][x+(i*kx)].colour != self.colour and y+(i*kx)>=0  and x >=0 and y+(i*kx)<=7  and x <=7:
                        moves.append((y, x+(i*kx)))
                except Exception as e:
                    pass
        
        return moves
    
class Knight(Piece):  
    def __init__(self,collumn,row,colour,id):
        super().__init__(collumn,row,colour,2,"Knig",id)
    def possibleMoves(self,gameArray):
        y = self.row
        x = self.collumn
        moves = []
         
        #2 different situations,
        #y = -2, 2 and x = 1 or -1
        #x = -2, 2 and y = 1 or -1
        for yvar in range(2):
            if yvar == 0:
                ky = 2
            if yvar == 1:
                ky = -2
            
            for xvar in range(2):
                if xvar == 0:
                    kx = 1
                if xvar == 1:
                    kx = -1
                try: 
                    i=1
                    if gameArray[y+(i*ky)][x+(i*kx)].colour != self.colour and y+(i*ky)>=0  and x+(i*kx) >=0 and y+(i*ky)<=7  and x+(i*kx) <=7:
                        moves.append((y+(i*ky), x+(i*kx)))
                    i+=1
      
                except Exception as e:
                    pass
        for yvar in range(2):
            if yvar == 0:
                ky = 1
            if yvar == 1:
                ky = -1
            
            for xvar in range(2):
                if xvar == 0:
                    kx = 2
                if xvar == 1:
                    kx = -2
                try: 
                    i=1
                    if gameArray[y+(i*ky)][x+(i*kx)].colour != self.colour and y+(i*ky)>=0  and x+(i*kx) >=0 and y+(i*ky)<=7  and x+(i*kx) <=7:
                        moves.append((y+(i*ky), x+(i*kx)))
                    i+=1
      
                except Exception as e:
                    pass
        return moves


class Pawn(Piece):  
    def __init__(self,collumn,row,colour,id):
        super().__init__(collumn,row,colour,3,"Pawn",id)
    def possibleMoves(self, gameArray):
        
        y = self.row
        x = self.collumn
        moves = []
           
        if self.colour == 'b':
            #black (move down)
            try:
                if gameArray[y+1][x].colour == 'n':
                    moves.append((y + 1, x ))
            except Exception as e:
                pass
            #black first move(move down)
            try:
                if y == 1 and gameArray[y+2][x].colour == 'n' and gameArray[y+1][x].colour == 'n':
                    moves.append((y + 2, x ))
            except Exception as e:
                pass
            
        
        if self.colour == 'w':
            #white (move up)
            try:
                if gameArray[y-1][x].colour == 'n':
                    moves.append((y - 1, x ))
            except Exception as e:
                pass
            #white first move(move up)
            try:
                if y == 6 and gameArray[y-2][x].colour == 'n' and gameArray[y-1][x].colour == 'n':
                    moves.append((y - 2, x ))
            except Exception as e:
                pass

        if self.colour == 'w':
            #white pawn take top right
            try:
                if gameArray[y - 1][x + 1].colour != self.colour:
                    if gameArray[y-1][x+1].colour != 'n' and y-1 >=0 and x+1 <= 7:
                        moves.append((y-1, x+1))
            except Exception as e:
                pass
            #white pawn take top left
            try:
                if gameArray[y - 1][x - 1].colour != self.colour:
                    if gameArray[y-1][x-1].colour != 'n' and y-1 >=0 and x-1 >= 0:
                        moves.append((y-1, x-1))
            except Exception as e:
                pass
        if self.colour == 'b':
            #black pawn take bottom right
            try:
                if gameArray[y + 1][x + 1].colour != self.colour:
                    if gameArray[y+1][x+1].colour != 'n' and y+1 <=7 and x+1 <= 7:
                        moves.append((y+1, x+1))
            except Exception as e:
                pass
            #black pawn take bottom left
            try:
                if gameArray[y + 1][x - 1].colour != self.colour:
                    if gameArray[y+1][x-1].colour != 'n' and y+1 <=7 and x-1 >= 0:
                        moves.append((y+1, x-1))
            except Exception as e:
                pass
            
        return moves

class Queen(Piece):  
    def __init__(self,collumn,row,colour,id):
        super().__init__(collumn,row,colour,4,"Quee",id)
    def possibleMoves(self,gameArray):
        y = self.row
        x = self.collumn
        moves = []
         
        
        for yvar in range(2):
            if yvar == 0:
                ky = 1
            if yvar == 1:
                ky = -1
            
            for xvar in range(2):
                if xvar == 0:
                    kx = 1
                if xvar == 1:
                    kx = -1
                i=1
                try:  
                    
                    while gameArray[y+(i*ky)][x+(i*kx)].colour == 'n' and y+(i*ky)>=0  and x+(i*kx) >=0 and y+(i*ky)<=7  and x+(i*kx) <=7:
                            if gameArray[y+(i*ky)][x+(i*kx)].colour != self.colour:
                                moves.append((y + (i*ky), x + (i*kx)))
                            else:
                                break
                            i+=1        
                except Exception as e:
                    pass
                try:
                    if gameArray[y+(i*ky)][x+(i*kx)].colour != self.colour and y+(i*ky)>=0  and x+(i*kx) >=0 and y+(i*ky)<=7  and x+(i*kx) <=7:
                            moves.append((y+(i*ky), x+(i*kx)))
                    i+=1
                except Exception as e:
                    pass

        for yvar in range(2):
            if yvar == 0:
                ky = 1
            if yvar == 1:
                ky = -1  
            i=1

            try:    
                while gameArray[y+(i*ky)][x].colour == 'n' and y+(i*ky)>=0  and x >=0 and y+(i*ky)<=7  and x <=7:
                        if gameArray[y+(i*ky)][x].colour != self.colour:
                            moves.append((y + (i*ky), x))
                        else: 
                            break
                        i+=1        
            except Exception as e:
                pass
            try:    
                if gameArray[y+(i*ky)][x].colour != self.colour and y+(i*ky)>=0  and x >=0 and y+(i*ky)<=7  and x <=7:
                        moves.append((y+(i*ky), x))
                i+=1
            except Exception as e:
                pass

        for xvar in range(2):
                if xvar == 0:
                    kx = 1
                if xvar == 1:
                    kx = -1
                i=1
                
                try: 
                    while gameArray[y][x+(i*kx)].colour == 'n' and y>=0  and x+(i*kx) >=0 and y<=7  and x+(i*kx) <=7:
                            if gameArray[y][x+(i*kx)].colour != self.colour:
                                moves.append((y, x + (i*kx)))
                            else:
                                break
                            i+=1        
                except Exception as e:
                    pass
                try: 
                    if gameArray[y][x+(i*kx)].colour != self.colour and y>=0  and x+(i*kx) >=0 and y<=7  and x+(i*kx) <=7:
                        moves.append((y, x+(i*kx)))  
                    i+=1
                except Exception as e:
                    pass
                    
        return moves

class Rook(Piece):  
    def __init__(self,collumn,row,colour,id):
        super().__init__(collumn,row,colour,5,"Rook",id)
    def possibleMoves(self,gameArray):
        y = self.row
        x = self.collumn
        moves = []
    
        for yvar in range(2):
            if yvar == 0:
                ky = 1
            if yvar == 1:
                ky = -1  
            i=1

            try: 
                while gameArray[y+(i*ky)][x].colour == 'n' and y+(i*ky)>=0  and x >=0 and y+(i*ky)<=7  and x <=7:
                        if gameArray[y+(i*ky)][x].colour != self.colour:
                            moves.append((y + (i*ky), x))
                        else:
                            break
                        i+=1        
            except Exception as e:
                pass
            try: 
                if gameArray[y+(i*ky)][x].colour != self.colour and y+(i*ky)>=0  and x >=0 and y+(i*ky)<=7  and x <=7:
                    moves.append((y+(i*ky), x))
                i+=1
            except Exception as e:
                pass

        for xvar in range(2):
                if xvar == 0:
                    kx = 1
                if xvar == 1:
                    kx = -1
                i=1
                
                try: 
                    while gameArray[y][x+(i*kx)].colour == 'n' and y>=0  and x+(i*kx) >=0 and y<=7  and x+(i*kx) <=7:
                            if gameArray[y][x+(i*kx)].colour != self.colour:
                                moves.append((y, x + (i*kx)))
                            else:
                                break
                            i+=1        
                except Exception as e:
                    pass
                try: 
                    if gameArray[y][x+(i*kx)].colour != self.colour and x+(i*kx)>=0  and y >=0 and x+(i*kx)<=7  and y <=7:
                            moves.append((y, x+(i*kx)))
                        
                    i+=1
                except Exception as e:
                    pass
        return moves


    
