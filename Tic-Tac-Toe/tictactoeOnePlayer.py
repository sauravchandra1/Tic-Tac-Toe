# tic tac toe

import random, pygame, sys
from pygame.locals import *


FPS = 30 # frames per second , the general speed of the program
WINDOWWIDTH = 640 # window's width in pixel
WINDOWHEIGHT = 480 # window's height in pixel
BOARDSIZE = 3 # number of rows and columns in playing board
GAPSIZE = 10 # gap size between boxes in pixel
BOXSIZE = 90 # width and height of box in pixel

XMARGIN = int(( WINDOWWIDTH - ( BOARDSIZE*( BOXSIZE + GAPSIZE ))) / 2 )
YMARGIN = int(( WINDOWHEIGHT - ( BOARDSIZE*( BOXSIZE + GAPSIZE ))) / 2 )

# Bot evaluation constants
WIN = 10
TIE = 0
LOSS = -10

PLAYER1 = 'X'
BOT = 'O'
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('TIC-TAC-TOE => 2 Players GAME')

    mainBoard = getInitialStateBoard()
    revealedBoxes = generateRevealedBoxesData(False)


    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(mainBoard,revealedBoxes)
    turn = PLAYER1
    winner = None
    tie = False
    # play again button
    playagain = True
    fontPlayAgain = pygame.font.Font('freesansbold.ttf',32)
    playAgainText = fontPlayAgain.render('PLAY AGAIN !!!', True, YELLOW, RED)
    playAgainTextRect = playAgainText.get_rect()
    playAgainTextRect.bottomright = (WINDOWWIDTH-5, WINDOWHEIGHT-5)

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard,revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if turn == PLAYER1 and boxx !=None and boxy != None :
            # The mouse is currently over a box and its player1's turn.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                mainBoard[boxx][boxy] = PLAYER1 # set box with the player sign
                turn = BOT
                if hasWon(mainBoard , PLAYER1) :
                    turn = None
                    winner = PLAYER1
                    playagain = False
                if gameOver(revealedBoxes):
                    tie = True
                    turn = None
                    playagain = False
        elif turn == BOT  :
            # The bot will play as its its turn now.
            botx, boty = playbot(mainBoard, revealedBoxes)
            
            if not revealedBoxes[botx][boty]:
                
                #drawHighlightBox(botx, boty)
                revealedBoxes[botx][boty] = True # set the box as "revealed"
                mainBoard[botx][boty] = BOT # set box with the player sign
                turn = PLAYER1
                if hasWon(mainBoard , BOT):
                    turn = None
                    playagain = False
                    winner = BOT
                if gameOver(revealedBoxes):
                    tie = True
                    turn = None
                    playagain = False

        elif turn == None and mouseClicked and playAgainTextRect.collidepoint(mousex, mousey):
            playagain = True
            mainBoard = getInitialStateBoard()
            revealedBoxes = generateRevealedBoxesData(False)
            turn = PLAYER1
            winner = None
            tie = False
                
        # Display game state
        fontObj = pygame.font.Font('freesansbold.ttf',32)
        if turn == PLAYER1 or turn == BOT :
            textSurfaceObj = fontObj.render('        PLAYER : ' + str(PLAYER1) + '                        BOT : ' + str(BOT) , True , WHITE)  
        elif winner == PLAYER1:
            textSurfaceObj = fontObj.render('PLAYER (' + str(PLAYER1) + ')  has Won the game' , True , GREEN)
        elif winner == BOT :
            textSurfaceObj = fontObj.render('BOT  (' + str(BOT) + ') has Won the game' , True , ORANGE)
        elif tie:
            textSurfaceObj = fontObj.render('                              DRAW !!!' , True , WHITE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (2,4)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        if not playagain:
            DISPLAYSURF.blit(playAgainText, playAgainTextRect)
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getInitialStateBoard():
    # Create the board data structure, with every box initialised to 0.
    board = []
    for x in range(BOARDSIZE):
        column = []
        for y in range(BOARDSIZE):
            column.append(0)
        board.append(column)
    return board

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDSIZE):
        revealedBoxes.append([val] * BOARDSIZE)
    return revealedBoxes


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):
            left, top = leftTopCoordsOfBox(boxx, boxy)
               # Draw a covered box.
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            if revealed[boxx][boxy]:
                # Draw the (revealed) icon.
                drawIcon(board[boxx][boxy], boxx, boxy)


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def drawIcon(icon, boxx, boxy):
    half = int(BOXSIZE * 0.50)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    fontObj = pygame.font.Font('freesansbold.ttf',48)
    if icon == PLAYER1:
        textSurfaceObj = fontObj.render(str(PLAYER1) , True , GREEN)
    if icon == BOT:
        textSurfaceObj = fontObj.render(str(BOT) , True , ORANGE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (left+half,top+half)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)



def hasWon(board, player):

    if board[0][0]==player and board[0][1]==player and board[0][2]==player:
        return True
    if board[1][0]==player and board[1][1]==player and board[1][2]==player:
        return True
    if board[2][0]==player and board[2][1]==player and board[2][2]==player:
        return True
    if board[0][0]==player and board[1][0]==player and board[2][0]==player:
        return True
    if board[0][1]==player and board[1][1]==player and board[2][1]==player:
        return True
    if board[0][2]==player and board[1][2]==player and board[2][2]==player:
        return True
    if board[0][0]==player and board[1][1]==player and board[2][2]==player:
        return True
    if board[0][2]==player and board[1][1]==player and board[2][0]==player:
        return True
    return False




def gameOver(revealedBoxes):
    for x in range(BOARDSIZE):
        for y in range(BOARDSIZE):
            if not revealedBoxes[x][y]:
                return False
    return True



def playbot(board, revealed):
    maxScore = -100
    botx = 0
    boty = 0
    for x in range(BOARDSIZE):
        for y in range(BOARDSIZE):
            if not revealed[x][y] :
                revealed[x][y] = True
                board[x][y] = BOT
                if hasWon(board, BOT):
                    revealed[x][y] = False
                    board[x][y] = 0
                    return (x, y)
                elif gameOver(revealed):
                    revealed[x][y] = False
                    board[x][y] = 0
                    return (x, y)
                else:
                    score = minimiser(board, revealed )
                    if score > maxScore:
                        maxScore = score
                        botx = x
                        boty = y
                    revealed[x][y] = False
                    board[x][y] = 0
    return (botx, boty)

def minimiser(board, revealed):
    minScore = 100
    for x in range(BOARDSIZE):
        for y in range(BOARDSIZE):
            if not revealed[x][y] :
                revealed[x][y] = True
                board[x][y] = PLAYER1
                if hasWon(board, PLAYER1):
                    revealed[x][y] = False
                    board[x][y] = 0
                    return LOSS
                elif gameOver(revealed):
                    revealed[x][y] = False
                    board[x][y] = 0
                    return TIE
                else :
                    score = maximiser(board, revealed)
                    if score < minScore :
                        minScore = score
                    revealed[x][y] = False
                    board[x][y] = 0
    return minScore





def  maximiser(board, revealed):
    maxScore = -100
    for x in range(BOARDSIZE):
        for y in range(BOARDSIZE):
            if not revealed[x][y] :
                revealed[x][y] = True
                board[x][y] = BOT
                if hasWon(board, BOT):
                    revealed[x][y] = False
                    board[x][y] = 0
                    return WIN
                elif gameOver(revealed):
                    revealed[x][y] = False
                    board[x][y] = 0
                    return TIE
                else:
                    score = minimiser(board, revealed)
                    if score >= maxScore:
                        maxScore = score
                    revealed[x][y] = False
                    board[x][y] = 0
    return ( maxScore )
    



if __name__ == '__main__':
    main()
