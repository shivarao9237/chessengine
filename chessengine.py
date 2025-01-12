"""it is for making valid moves"""
class GameState():
    def __init__(self):
        self.board=[["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bp","bp","bp","bp","bp","bp","bp","bp"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["wp","wp","wp","wp","wp","wp","wp","wp"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.movefunctions={'p':self.getallpawnmoves,'R':self.getallrookmoves,'B':self.getallbishopmoves,
                            'N':self.getallknightmoves,'Q':self.getallqueenmoves,'K':self.getallkingmoves}

        self.whitetomove=True
        self.movelog=[]
        self.whitekinglocation=(7,4)
        self.blackkinglocation=(0,4)
        self.checkmate=False
        self.stalemate=False
        self.enpassantpossible=()
        self.currentcastlingright=castlerights(True,True,True,True)
        self.castlerightlog=[castlerights(self.currentcastlingright.wks,self.currentcastlingright.bks,self.currentcastlingright.wqs,self.currentcastlingright.bqs)]
    def makemove(self,move):
        self.board[move.startrow][move.startcol]="--"
        self.board[move.endrow][move.endcol]=move.piecemoved
        self.movelog.append(move)
        self.whitetomove= not self.whitetomove
        if move.piecemoved=="wK":
            self.whitekinglocation=(move.endrow,move.endcol)
        elif move.piecemoved=="bK":
            self.blackkinglocation=(move.endrow,move.endcol)
        if move.ispawnpromotion:
            self.board[move.endrow][move.endcol]=move.piecemoved[0]+'Q'
        if move.isenpassantmove:
            self.board[move.startrow][move.endcol]='--'
        if move.piecemoved[1]=='p' and abs(move.startrow-move.endrow)==2:
            self.enpassantpossible=((move.startrow+move.endrow)//2,move.startcol)
        else:
            self.enpassantpossible=()
        if move.iscastlemove:
            if move.endcol-move.startcol==2:
                self.board[move.endrow][move.endcol-1]=self.board[move.endrow][move.endcol+1]
                self.board[move.endrow][move.endcol+1]='--'
            else:
                self.board[move.endrow][move.endcol+1]=self.board[move.endrow][move.endcol-2]
                self.board[move.endrow][move.endcol-2]='--'
        self.updatecastlerights(move)
        self.castlerightlog.append(castlerights(self.currentcastlingright.wks,self.currentcastlingright.bks,self.currentcastlingright.wqs,self.currentcastlingright.bqs))
    def undomove(self):
        move=self.movelog.pop()
        self.board[move.startrow][move.startcol]=move.piecemoved
        self.board[move.endrow][move.endcol]=move.piececaptured
        self.whitetomove=not self.whitetomove
        if move.piecemoved=="wK":
            self.whitekinglocation=(move.startrow,move.startcol)
        elif move.piecemoved=="bK":
            self.blackkinglocation=(move.startrow,move.startcol)
        if move.isenpassantmove:
            self.board[move.endrow][move.endcol]='--'
            self.board[move.startrow][move.endcol]=move.piececaptured
            self.enpassantpossible=(move.endrow,move.endcol)
        if move.piecemoved[1]=='p' and abs(move.startrow-move.endrow)==2:
            self.enpassantpossible=()
        self.castlerightlog.pop()
        self.currentcastlingright=self.castlerightlog[-1]
        if move.iscastlemove:
            if move.endcol-move.startcol==2:
                self.board[move.endrow][move.endcol+1]=self.board[move.endrow][move.endcol-1]
                self.board[move.endrow][move.endcol-1]='--'
            else:
                self.board[move.endrow][move.endcol-2]=self.board[move.endrow][move.endcol+1]
                self.board[move.endrow][move.endcol+1]='--'

    def updatecastlerights(self,move):
        if move.piecemoved=='wK':
            self.currentcastlingright.wks=False
            self.currentcastlingright.wqs=False
        elif move.piecemoved=='bK':
            self.currentcastlingright.bks=False
            self.currentcastlingright.bqs=False
        elif move.piecemoved=='wR':
            if move.startrow==7:
                if move.startcol==0:
                    self.currentcastlingright.wqs=False
                if move.startcol==7:
                    self.currentcastlingright.wks=False
        elif move.piecemoved=='bR':
            if move.startrow==0:
                if move.startcol==0:
                    self.currentcastlingright.bqs=False
                if move.startcol==7:
                    self.currentcastlingright.bks=False
    def getvalidmoves(self):
        tempenpassentpossible=self.enpassantpossible
        tempcastlerights=castlerights(self.currentcastlingright.wks,self.currentcastlingright.bks,self.currentcastlingright.wqs,self.currentcastlingright.bqs)
        moves=self.getallpossiblemoves()
        if self.whitetomove:
            self.getcastlemoves(self.whitekinglocation[0],self.whitekinglocation[1],moves)

        else:
            self.getcastlemoves(self.blackkinglocation[0],self.blackkinglocation[1],moves)
        for i in range(len(moves)-1,-1,-1):
            self.makemove(moves[i])
            self.whitetomove=not self.whitetomove
            if self.incheck():
                moves.remove(moves[i])
            self.whitetomove=not self.whitetomove
            self.undomove()
        if len(moves)==0:
            if self.incheck():
                self.checkmate=True
            else:
                self.stalemate=True
        else:
            self.checkmate=False
            self.stalemate=False
        self.enpassantpossible=tempenpassentpossible
        self.currentcastlingright=tempcastlerights
        return moves
    def incheck(self):
        if self.whitetomove:
            return self.squareunderattack(self.whitekinglocation[0],self.whitekinglocation[1])
        else:
            return self.squareunderattack(self.blackkinglocation[0],self.blackkinglocation[1])
        

    def squareunderattack(self,r,c):
        self.whitetomove=not self.whitetomove
        oppmoves=self.getallpossiblemoves()
        self.whitetomove=not self.whitetomove
        for move in oppmoves:
            if move.endrow==r and move.endcol==c:
                return True
        return False
    
    def getallpossiblemoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if(turn=='w' and self.whitetomove) or (turn=='b' and not self.whitetomove):
                    piece=self.board[r][c][1]
                    self.movefunctions[piece](r,c,moves)
        return moves
    def getallpawnmoves(self,r,c,moves):
        if self.whitetomove:
            if self.board[r-1][c]=="--":
                moves.append(move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(move((r,c),(r-2,c),self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0]=='b':
                    moves.append(move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1)==self.enpassantpossible:
                    moves.append(move((r,c),(r-1,c-1),self.board,isenpassantmove=True))
            if c+1<=7:
                if self.board[r-1][c+1][0]=='b':
                    moves.append(move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1)==self.enpassantpossible:
                    moves.append(move((r,c),(r-1,c+1),self.board,isenpassantmove=True))
        else:
            if self.board[r+1][c]=="--":
                moves.append(move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(move((r,c),(r+2,c),self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0]=='w':
                    moves.append(move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1)==self.enpassantpossible:
                    moves.append(move((r,c),(r+1,c-1),self.board,isenpassantmove=True))
            if c+1<=7:
                if self.board[r+1][c+1][0]=='w':
                    moves.append(move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1)==self.enpassantpossible:
                    moves.append(move((r,c),(r+1,c+1),self.board,isenpassantmove=True))

    def getallrookmoves(self, r, c, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemycolor = "b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":
                        moves.append(move((r, c), (endrow, endcol), self.board))
                    elif endpiece[0] == enemycolor:
                        moves.append(move((r, c), (endrow, endcol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getallbishopmoves(self,r,c,moves):
        directions=((-1,-1),(-1,1),(1,-1),(1,1))
        enemycolor="b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1,8):
                endrow=r+d[0]*i
                endcol=c+d[1]*i
                if 0<=endrow<8 and 0<=endcol<8:
                    endpiece=self.board[endrow][endcol]
                    if endpiece=="--":
                        moves.append(move((r,c),(endrow,endcol),self.board))
                    elif endpiece[0]==enemycolor:
                        moves.append(move((r,c),(endrow,endcol),self.board))
                        break
                    else:
                        break
                else:
                    break
    def getallknightmoves(self,r,c,moves):
        directions=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        enemycolor="w" if self.whitetomove else "b"
        for d in directions:
            endrow=r+d[0]
            endcol=c+d[1]
            if 0<=endrow<8 and 0<=endcol<8:
                endpiece=self.board[endrow][endcol]
                if endpiece[0]!=enemycolor:
                   moves.append(move((r,c),(endrow,endcol),self.board))
    def getallqueenmoves(self,r,c,moves):
         directions=((-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(0,-1),(1,0),(0,1))
         enemycolor="b" if self.whitetomove else "w"
         for d in directions:
            for i in range(1,8):
                endrow=r+d[0]*i
                endcol=c+d[1]*i
                if 0<=endrow<8 and 0<=endcol<8:
                    endpiece=self.board[endrow][endcol]
                    if endpiece=="--":
                        moves.append(move((r,c),(endrow,endcol),self.board))
                    elif endpiece[0]==enemycolor:
                        moves.append(move((r,c),(endrow,endcol),self.board))
                        break
                    else:
                        break
                else:
                    break
    def getallkingmoves(self,r,c,moves):
        directions=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        enemycolor="w" if self.whitetomove else "b"
        for d in range(8):
            endrow=r+directions[d][0]
            endcol=c+directions[d][1]
            if 0<=endrow<8 and 0<=endcol<8:
                endpiece=self.board[endrow][endcol]
                if endpiece[0]!=enemycolor:
                   moves.append(move((r,c),(endrow,endcol),self.board))
    def getcastlemoves(self,r,c,moves):
        if self.squareunderattack(r,c):
            return
        if (self.whitetomove and self.currentcastlingright.wks )or(not self.whitetomove and self.currentcastlingright.bks):
            self.getkingsidecastlemoves(r,c,moves)
        if(self.whitetomove and self.currentcastlingright.wqs )or(not self.whitetomove and self.currentcastlingright.bqs):
            self.getqueensidecastlemoves(r,c,moves)
    def getkingsidecastlemoves(self,r,c,moves):
        if self.board[r][c+1]=='--' and self.board[r][c+2]=='--':
            if not self.squareunderattack(r,c+1) and not self.squareunderattack(r,c+2):
                moves.append(move((r,c),(r,c+2),self.board,iscastlemove=True))
    def getqueensidecastlemoves(self,r,c,moves):
        if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]:
            if not self.squareunderattack(r,c-1) and not self.squareunderattack(r,c-2):
                moves.append(move((r,c),(r,c-2),self.board,iscastlemove=True))
    
class castlerights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs
class move():
    rankstorows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowstoranks={v:k for k,v in rankstorows.items()}
    filestocols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colstofiles={v:k for k,v in filestocols.items()}
    def __init__(self,startsq,endsq,board,isenpassantmove=False,iscastlemove=False):
        self.startrow=startsq[0]
        self.startcol=startsq[1]
        self.endrow=endsq[0]
        self.endcol=endsq[1]
        self.piecemoved=board[self.startrow][self.startcol]
        self.piececaptured=board[self.endrow][self.endcol]
        self.ispawnpromotion=False
        self.isenpassantmove=False
        if (self.piecemoved=='wp' and self.endrow==0) or (self.piecemoved=='bp' and self.endrow==7):
            self.ispawnpromotion=True
        self.isenpassantmove=isenpassantmove
        if self.isenpassantmove:
            self.piececaptured='wp' if self.piecemoved=='bp' else 'bp'
        self.iscastlemove=iscastlemove
        self.moveid=self.startrow*1000+self.startcol*100+self.endrow*10+self.endcol

    def __eq__(self, other):
        if isinstance(other,move):
            return self.moveid==other.moveid
        return False


    def getchessnotation(self):
        return self.getrankfile(self.startrow,self.startcol)+self.getrankfile(self.endrow,self.endcol)
    
    def getrankfile(self,r,c):
        return self.colstofiles[c]+self.rowstoranks[r]
          
