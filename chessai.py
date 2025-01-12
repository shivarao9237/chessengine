import random
piecescore={'K':0,'Q':9,'R':5,'B':3,'N':3,'p':1}
checkmate=1000
stalemate=0
def findmoves(validmoves):
    return validmoves[random.randint(0,len(validmoves)-1)]

def findbestmove(gs,validmoves):
    turnmultiplier=1 if gs.whitetomove else -1
    opponentminmaxscore=checkmate
    bestplayermove=None
    random.shuffle(validmoves)
    for playermove in validmoves:
        gs.makemove(playermove)
        opponentmoves=gs.getvalidmoves()
        opponentmaxscore=-checkmate
        for opponentmove in opponentmoves:
            gs.makemove(opponentmove)
            if gs.checkmate:
                score=-turnmultiplier*checkmate
            elif gs.stalemate:
                score=stalemate
            else:
                score=-turnmultiplier*scorematerial(gs.board)
            if(score>opponentmaxscore):
                opponentmaxscore=score
            gs.undomove()
        if opponentminmaxscore>opponentmaxscore:
            opponentminmaxscore=opponentmaxscore
            bestplayermove=playermove
        gs.undomove()
    return bestplayermove


def scorematerial(board):
    score=0
    for row in board:
        for sq in row:
            if sq[0]=='w':
                score+=piecescore[sq[1]]
            elif sq[0]=='b':
                score+=piecescore[sq[1]]
    return score