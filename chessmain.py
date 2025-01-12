""" it is for user side"""
import pygame as p
import chessengine,chessai

WIDTH=HEIGHT=512
DIMENSION=8
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS=15
IMAGES={}
def loadImages():
    pieces=["bB","bK","bN","bp","bQ","bR","wB","wK","wN","wp","wQ","wR"]
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=chessengine.GameState()
    validmoves=gs.getvalidmoves()
    movemade=False
    animate=False
    loadImages()
    running=True
    sqsel=()
    playerclick=[]
    gameover=False
    playerone=True
    playertwo=False
    while running:
        humanturn=(gs.whitetomove and playerone)or (not gs.whitetomove and playertwo)
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            elif e.type==p.MOUSEBUTTONDOWN:
             if not gameover and humanturn:
                location=p.mouse.get_pos()
                col=location[0]//SQ_SIZE
                row=location[1]//SQ_SIZE
                if sqsel==(row,col):
                    sqsel=()
                    playerclick=[]
                else:
                    sqsel=(row,col)
                    playerclick.append(sqsel)
                if len(playerclick)==2:
                    move=chessengine.move(playerclick[0],playerclick[1],gs.board)
                    print(move.getchessnotation())
                    for i in range(len(validmoves)):
                        if move == validmoves[i]:
                         gs.makemove(validmoves[i])
                         movemade=True
                         animate=True
                         sqsel=()
                         playerclick=[]
                    if not movemade:
                        playerclick=[sqsel]
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undomove()
                    movemade=True
                    animate=False
                if e.key==p.K_r:
                    gs=chessengine.GameState()
                    validmoves=gs.getvalidmoves
                    sqsel=()
                    playerclick=[]
                    movemade=False
                    animate=False

        if not gameover and not humanturn:
            aimove=chessai.findbestmove(gs,validmoves)
            if aimove is None:
              aimove=chessai.findmoves(validmoves)
            gs.makemove(aimove)
            movemade=True
            animate=True


        if movemade:
            if animate:
               animatemove(gs.movelog[-1],screen,gs.board,clock)
            validmoves=gs.getvalidmoves()
            movemade=False
            animate=False
        drawGameState(screen,gs,validmoves,sqsel)
        if gs.checkmate:
            gameover=True
            if gs.whitetomove:
                drawText(screen,'Black won by checkmate')
            else:
                drawText(screen,'White won by checkmate')
        elif gs.stalemate:
            drawText(screen,'stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()
def highlightsquares(screen,gs,validmoves,sqsel):
    if sqsel!=():
        r,c=sqsel
        if gs.board[r][c][0]==('w'if gs.whitetomove else 'b'):
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(p.Color('dark green'))
            for move in validmoves:
                if move.startrow==r and move.startcol==c:
                    screen.blit(s,(SQ_SIZE*move.endcol,SQ_SIZE*move.endrow))
def drawGameState(screen,gs,validmoves,sqsel):
    drawBoard(screen)
    highlightsquares(screen,gs,validmoves,sqsel)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    global colors
    colors=[p.Color("white"),p.Color("GREEN")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    
def animatemove(move,screen,board,clock):
    global colors
    dr=move.endrow-move.startrow
    dc=move.endcol-move.startcol
    framepersq=10
    framecount=(abs(dr)+abs(dc))*framepersq
    for frame in range(framecount+1):
        r,c=(move.startrow+dr*frame/framecount,move.startcol+dc*frame/framecount)
        drawBoard(screen)
        drawPieces(screen,board)
        color=colors[(move.endrow+move.endcol)%2]
        endsq=p.Rect(move.endcol*SQ_SIZE,move.endrow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endsq)
        if move.piececaptured!='--':
            screen.blit(IMAGES[move.piececaptured],endsq)
        screen.blit(IMAGES[move.piecemoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)
def drawText(screen,text):
    font=p.font.SysFont("Helvitca",32,True,False)
    textobject=font.render(text,0,p.Color('black'))
    textlocation = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textobject.get_width() / 2, 
        HEIGHT / 2 - textobject.get_height() / 2  
    )
    screen.blit(textobject,textlocation)
    textobject=font.render(text,0,p.Color("gray"))
    screen.blit(textobject,textlocation.move(2,2))


if __name__=="__main__":
    main()