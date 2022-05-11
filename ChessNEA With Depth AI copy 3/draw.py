from piece import *

class Draw:
    def __init__(self):
        self.win = pygame.display.set_mode((900, 900))
        self.border = pygame.Rect(900//2 -5,0,10,900)
        self.gameXYXY = (60,60,780,780)
        self.board = pygame.transform.scale(pygame.image.load(os.path.join('img', 'board.png')), (780,780))
        

    def drawBoard(self):
        
        #basic drawing the board
        self.win.fill((123,158,168))
        self.win.blit(self.board, (60 ,60))
        pygame.draw.rect(self.win, (0,0,0), (60,60,780,780), 5)
        return self.win

    #updates the board
        #pygame.display.update()

   
        #pygame.display.update()
                    
    def drawPieces(self,array):
        for i in range(8):
            for j in range(8):
                if array[i][j].colour != 'n':
                    array[i][j].draw(self.win)
        return array

    def drawPositions(self,posArray):
        for i in range(8):
            for j in range(8):
                if posArray[i][j].colour != 'n':
                    posArray[i][j].draw(self.win)

    def drawRedBox(self,toggleRedBox,redX,redY):
        try:
            if toggleRedBox == True:
                pygame.draw.rect(self.win, (240,128,128), (redX*(780/8) + 60 ,redY*(780/8) + 60, 97.5,97.5), 5) 
                pygame.display.update()
        except Exception as e:
            print(e)


