from tkinter import *
import random, tkinter.messagebox

class MindSweeper(object):
    def __init__(self, width=10, height = 10, minenum = 20):
        self.window = Tk()
        self.window.title("MindSweeper")
        self.window.resizable(0,0)  # 크기고정_여기서 0은 false

        self.button=[]  # 지뢰판
        self.markflag=[]    # 지뢰표시
        self.btnflag=[] # 해당 버튼이 눌렸는지 판단
        self.markcnt = 0  # 몇 개의 mark를 남겼는지
        self.minenum = minenum  # 총 지뢰 개수
        self.mapwidth = width   # 지뢰판의 너비
        self.mapheight = height # 지뢰판의 높이
        self.mine = []  # 지뢰의 좌표를 담은 list
        self.minecnt = []   # 각 좌표별 감지되는 지뢰 개수
        self.cnt=0

        for i in range(self.mapwidth): # btnflag와 minecnt를 초기화시킴
            tmprow = []
            tmpflag = []
            tmpmark = []
            for j in range(self.mapheight):
                tmprow.append(0)
                tmpflag.append(False)
                tmpmark.append(False)

            self.minecnt.append(tmprow)
            self.btnflag.append(tmpflag)
            self.markflag.append(tmpmark)

        for i in range(self.minenum):   # 지뢰 위치 정하기
            x = random.randint(0, self.mapwidth - 1)
            y = random.randint(0, self.mapheight - 1)

            tmp=0
            while True: # 겹치는 지뢰가 없도록 함
                if tmp==len(self.mine):
                    self.mine.append((x,y))
                    break
                if(x==self.mine[tmp][0]) and (y==self.mine[tmp][1]):
                    x = random.randint(0, self.mapwidth - 1)
                    y = random.randint(0, self.mapheight - 1)
                    tmp=0
                else:
                    tmp+=1

        for i in range(len(self.mine)): # 각 좌표별 지뢰개수 세기
            x = self.mine[i][0]
            y = self.mine[i][1]
            self.minecnt[x][y] = 0

            if x > 0:   # x==0인 상황을 피함
                if y > 0:
                    self.minecnt[x-1][y-1]+=1
                self.minecnt[x-1][y]+=1
                if y<self.mapheight-1:
                    self.minecnt[x-1][y+1]+=1

            if x < self.mapwidth-1:
                if y>0:
                    self.minecnt[x+1][y-1] +=1
                self.minecnt[x+1][y] += 1
                if y<self.mapheight-1:
                    self.minecnt[x+1][y+1]+=1

            if y>0:
                self.minecnt[x][y-1]+=1

            if y<self.mapheight-1:
                self.minecnt[x][y+1]+=1

        self.markText = StringVar()  # string변수 선언
        self.markText.set("000")

        mainMenu = Menu(self.window)  # 메뉴바 만들기
        self.window.config(menu=mainMenu)  # 위젯의 설정을 변경하는 메서드

        gameMenu = Menu(mainMenu, tearoff=0)  # tearoff는 하위메뉴를 의미 (false)
        helfMenu = Menu(mainMenu, tearoff=0)
        mainMenu.add_cascade(label="게임", menu=gameMenu)
        mainMenu.add_cascade(label="도움말", menu=helfMenu)
        gameMenu.add_command(label="초급", command=self.setlowlevel)
        gameMenu.add_command(label="중급", command=self.setmiddlelevel)
        gameMenu.add_command(label="고급", command=self.sethighlevel)
        gameMenu.add_separator()
        gameMenu.add_command(label="종료", command=self.window.destroy)

        frame1 = Frame(self.window, borderwidth=10, relief="ridge")
        self.label = Label(frame1, text="0" + str(self.minenum), relief="ridge")
        self.label.pack(side="left", anchor="n", fill="both")
        self.homebtn = Button(frame1, command=self.home, text="♥")
        self.homebtn.pack(side="left", anchor="n", fill="both")
        marklabel = Label(frame1, textvariable=self.markText, relief="ridge")
        marklabel.pack(side="left", anchor="n", fill="both")

        frame2 = Frame(self.window, borderwidth=10, relief="ridge")

        for i in range(self.mapheight): # 지뢰판 세팅
            row = []
            flag = []
            for j in range(self.mapwidth):
                row.append(Button(frame2, text="", width=2, height=1))
                row[j].grid(row=i + 3, column=j + 3)
                row[j].bind("<Button-3>", self.mark)  # 마우스 우클릭
                row[j].bind("<Button-1>", self.click)  # 마우스 좌클릭
            self.button.append(row)
            self.markflag.append(flag)

        frame1.pack(fill="both", expand=True)
        frame2.pack(fill="both")

        self.window.mainloop()

    def click(self, event):
        col = int((event.x_root - self.window.winfo_x() - 18)/24)
        row = int((event.y_root - self.window.winfo_y() - 108) / 26)
        print(row, col)
        self.btnopen(row,col)

        mine_flag = False
        for i in range(len(self.mine)):
            if (row == self.mine[i][0]) and (col == self.mine[i][1]):
                mine_flag = True  # 지뢰인지 확인->맞으면 true

        if mine_flag:
            for j in range(len(self.mine)):
                x, y = self.mine[j][0], self.mine[j][1]
                self.button[x][y].config(relief="flat", text="*")
            self.game_over()
        else:
            self.gameWin(row,col)

    def spread(self, row, col):
        # 0인 칸을 누르면
        # 주위 8개의 칸이 open
        if(self.minecnt[row][col]==0):
            if row > 0:   # x==0인 상황을 피함
                if col > 0:
                    if (self.btnflag[row-1][col-1]==False):
                        self.btnopen(row-1,col-1)
                        self.gameWin(row-1,col-1)
                if (self.btnflag[row-1][col])==False:
                    self.btnopen(row-1,col)
                    self.gameWin(row-1, col)
                if col<self.mapheight-1:
                    if (self.btnflag[row-1][col+1]==False):
                        self.btnopen(row-1,col+1)
                        self.gameWin(row-1, col+1)

            if row < self.mapwidth-1:
                if col>0:
                    if (self.btnflag[row+1][col-1]==False):
                        self.btnopen(row+1,col-1)
                        self.gameWin(row+1, col-1)
                if (self.btnflag[row+1][col]==False):
                    self.btnopen(row+1,col)
                    self.gameWin(row+1, col)
                if col<self.mapheight-1:
                    if (self.btnflag[row+1][col+1]==False):
                        self.btnopen(row+1,col+1)
                        self.gameWin(row+1, col+1)

            if col>0:
                if (self.btnflag[row][col-1]==False):
                    self.btnopen(row,col-1)
                    self.gameWin(row, col-1)

            if col<self.mapheight-1:
                if (self.btnflag[row][col+1]==False):
                    self.btnopen(row,col+1)
                    self.gameWin(row, col+1)

    def btnopen(self,row,col):
        if (self.btnflag[row][col]):
            return
        self.button[row][col].config(relief="flat", state="disabled")
        self.button[row][col].unbind("<Button-3>")
        self.btnflag[row][col] = True

    def gameWin(self,row,col):
        self.button[row][col].config(text=self.minecnt[row][col])
        self.cnt += 1
        self.spread(row,col)
        if (self.cnt + self.minenum == self.mapwidth * self.mapheight):
            self.game_win()

    def setlowlevel(self):
        self.window.destroy()
        MindSweeper(10, 10, 20)

    def setmiddlelevel(self):
        self.window.destroy()
        MindSweeper(20, 20, 100)

    def sethighlevel(self):
        self.window.destroy()
        MindSweeper(25, 25, 150)

    def home(self):
        w = self.mapwidth
        h = self.mapheight
        n = self.minenum
        self.window.destroy()
        MindSweeper(w, h, n)

    def game_over(self):
        for i in self.button:
            for j in i:
                j.unbind("<Button-1>")
        tkinter.messagebox.showinfo("GameOver", "Lose..")

    def game_win(self):
        for i in self.button:
            for j in i:
                j.unbind("<Button-1>")
                j.unbind("<button-3>")
        tkinter.messagebox.showinfo("GameWin","Win!")

    def mark(self, event):
        col = int((event.x_root - self.window.winfo_x() - 18) / 24)
        row = int((event.y_root - self.window.winfo_y() - 108) / 26)
        print(row, col)
        if(self.markflag[row][col]):
            self.button[row][col].bind("<Button-1>",self.click)
            self.markflag[row][col]=False
            self.markcnt-=1
            self.button[row][col].config(text="")
        else:
            self.markflag[row][col]=True
            self.button[row][col].unbind("<Button-1>")
            self.markcnt+=1
            self.button[row][col].config(text="※")
        self.markText.set(str(self.markcnt))


if __name__ == "__main__":
    MindSweeper()
