from tkinter import *
from random import randint
import os

GAME_SIZE=4
BACKGROUND_COLOR = "#94877a"
EMPTY_COLOR = "#afa79a"
# Background colors
GRID_COLOR = {2:"#efe5dd", 4:"#eee2c9", 8:"#f4b37a", 16:"#f79466", 32:"#f87d60", 64:"#f85f3d", 128:"#efcf73", 256:"#eecd63", 512:"#eecA52", 1024:"#efc740", 2048:"#efc42f" }
# Font colors
FONT_COLOR = { 2:"#7a6f67", 4:"#7a6f69", 8:"#faf9f4", 16:"#faf6f2", 32:"#faf8f6", 64:"#fbfaf5", 128:"#fbfaf8", 256:"#faf8f8", 512:"#faf8f8", 1024:"#faf8f8", 2048:"#faf8f8" }


#Main

class Game2048(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('2048')
        self.bind("<Key>", self.getKey)# Key handler
        self.operations = { "'w'": MoveUp, "'s'": MoveDown, "'a'": MoveLeft, "'d'": MoveRight }
        self.initWindow()
        self.initMatrix()
        self.mainloop()
    # Starting screen
    def initWindow(self):
        bar=Frame(self)
        bar.grid()
        # Score
        self.t = Label(bar, justify=LEFT, font=("Verdana", 25, "bold"))
        self.t.pack(side='left')
        Button(bar, text="New Game", command=self.initMatrix,width=10,font=("Verdana", 20, "bold"),bg="#ffe4c7").pack(side='right')
        background = Frame(self, bg=BACKGROUND_COLOR)
        background.grid()
        self.gameGrid = []
        # Starting box
        for i in range(GAME_SIZE):
            x = []
            for j in range(GAME_SIZE):
                t = Label(background, justify=CENTER, font=("Verdana", 40, "bold"), width=4, height=2)
                t.grid(row=i, column=j, padx=5, pady=5)
                x.append(t)
            self.gameGrid.append(x)

    # Starting numbers
    def initMatrix(self):
        self.matrix = getEmptyMatrix()
        self.grade=0
        self.record=0
        self.getNewNumber()
        self.getNewNumber()
        # Score history
        if os.path.exists('record.txt'):
            with open('record.txt', 'r') as f:     
                self.record=f.read()  
                self.record=int(self.record)
        self.updateShow()
    # Refresh page
    def updateShow(self):
        # Update score
        self.t.configure(text="\nScore: %-15d\nBest: %-15d\n"%(self.grade,self.record))
        # Update placement
        for i in range(GAME_SIZE):
            for j in range(GAME_SIZE):
                x = self.matrix[i][j]
                if x == 0:
                    self.gameGrid[i][j].configure(text="", bg=EMPTY_COLOR)
                else:
                    self.gameGrid[i][j].configure(text=str(int(x)), bg=GRID_COLOR[x], fg=FONT_COLOR[x])
        self.update_idletasks()
    # Check game state
    def getState(self):
        # Win if contains 2048
        for x in self.matrix:
            if 2048 in x:
                return 1
        # Continue game
        for x in self.matrix:
            if 0 in x:
                return 0
        # Check for combination possibility whebn all containers filled
        for i in range(GAME_SIZE): 
            for j in range(GAME_SIZE-1): 
                if self.matrix[i][j]==self.matrix[i][j+1] or self.matrix[j][i]==self.matrix[j+1][i]:
                    return 0
        # Lost
        return -1
    # Allowed keys
    def getKey(self, event):
        key = repr(event.char)
        # Check if key is valid
        if key in self.operations:
            # Move action
            self.matrix,done,self.grade = self.operations[key](self.matrix,self.grade)
            # Check valid
            if done:
                if self.grade>self.record:
                    with open('record.txt', 'w') as f:
                        f.write(str(int(self.grade))) 
                        self.record=self.grade
                self.getNewNumber()
                self.updateShow()
                nowState=self.getState()
                if nowState==1:
                    # Display Win
                    self.gameGrid[int(GAME_SIZE/2-1)][int(GAME_SIZE/2-1)].configure(text="Game",bg=EMPTY_COLOR,fg=FONT_COLOR[16])
                    self.gameGrid[int(GAME_SIZE/2-1)][int(GAME_SIZE/2)].configure(text="Won!",bg=EMPTY_COLOR,fg=FONT_COLOR[16])
                if nowState==-1:
                    # Display lost
                    self.gameGrid[int(GAME_SIZE/2-1)][int(GAME_SIZE/2-1)].configure(text="Game",bg=EMPTY_COLOR,fg=FONT_COLOR[16])
                    self.gameGrid[int(GAME_SIZE/2-1)][int(GAME_SIZE/2)].configure(text="Lost",bg=EMPTY_COLOR,fg=FONT_COLOR[16])
    # Create 2 or 4
    def getNewNumber(self):
        index_x=randint(0, GAME_SIZE - 1)
        index_y=randint(0, GAME_SIZE - 1)
        # Find random empty spot
        while self.matrix[index_x][index_y] != 0:
            index_x=randint(0, GAME_SIZE - 1)
            index_y=randint(0, GAME_SIZE - 1)
        if self.grade>2048:
            self.matrix[index_x][index_y] = randint(1, 2)*2
        else:
            self.matrix[index_x][index_y] = 2

# Create containers
def getEmptyMatrix():
    mat=[]
    for i in range(GAME_SIZE):
        mat.append([])
        for j in range(GAME_SIZE):
            mat[i].append(0)
    return mat

# Up

def MoveUp(mat,grade):
    newGrade=grade
    newMatrix=getEmptyMatrix()
    # Movement check
    done=False
    # Move bottom to top
    for i in range(GAME_SIZE):
        count=0
        for j in range(GAME_SIZE):
            if mat[j][i]!=0:
                newMatrix[count][i]=mat[j][i]
                count+=1
    # Addition of neighbouring number
    for i in range(GAME_SIZE):
         for j in range(GAME_SIZE-1):
             if newMatrix[j][i]==newMatrix[j+1][i] and newMatrix[j][i]!=0:
                 newMatrix[j][i]*=2
                 newGrade+=newMatrix[j][i]
                 newMatrix[j+1][i]=0
    # Move all from bottom to top
    newMatrix2=getEmptyMatrix()
    for i in range(GAME_SIZE):
        count=0
        for j in range(GAME_SIZE):
            if newMatrix[j][i]!=0:
                newMatrix2[count][i]=newMatrix[j][i]
                count+=1
    # Check for successful combination
    if not (mat==newMatrix):
        done=True
    return (newMatrix2,done,newGrade)

#Down

def MoveDown(mat,grade):
    newGrade=grade
    newMatrix=getEmptyMatrix()
    # Movement check
    done=False
    # Move top to bottom
    for i in range(GAME_SIZE):
        count=GAME_SIZE-1
        for j in range(GAME_SIZE):
            j=GAME_SIZE-j-1
            if mat[j][i]!=0:
                newMatrix[count][i]=mat[j][i]
                count-=1
    # Addition of neighbouring number
    for i in range(GAME_SIZE):
         for j in range(GAME_SIZE-1):
             j=GAME_SIZE-j-1
             if newMatrix[j][i]==newMatrix[j-1][i] and newMatrix[j][i]!=0:
                 newMatrix[j][i]*=2
                 newGrade+=newMatrix[j][i]
                 newMatrix[j-1][i]=0
     # Move all to bottom
    newMatrix2=getEmptyMatrix()
    for i in range(GAME_SIZE):
        count=GAME_SIZE-1
        for j in range(GAME_SIZE):
            j=GAME_SIZE-j-1
            if newMatrix[j][i]!=0:
                newMatrix2[count][i]=newMatrix[j][i]
                count-=1
    # Check for successful combination
    if not (mat==newMatrix):
        done=True    
    return (newMatrix2,done,newGrade)

# Left

def MoveLeft(mat,grade):
    newGrade=grade
    newMatrix=getEmptyMatrix()
    # Movement check
    done=False
    # Move left from right
    for i in range(GAME_SIZE):
        count=0
        for j in range(GAME_SIZE):
            if mat[i][j]!=0:
                newMatrix[i][count]=mat[i][j]
                count+=1
    # Addition of neighbouring number
    for i in range(GAME_SIZE):
         for j in range(GAME_SIZE-1):
             if newMatrix[i][j]==newMatrix[i][j+1] and newMatrix[i][j]!=0:
                 newMatrix[i][j]*=2
                 newGrade+=newMatrix[i][j]
                 newMatrix[i][j+1]=0
    # Move all on right to left
    newMatrix2=getEmptyMatrix()
    for i in range(GAME_SIZE):
        count=0
        for j in range(GAME_SIZE):
            if newMatrix[i][j]!=0:
                newMatrix2[i][count]=newMatrix[i][j]
                count+=1
    # Check for successful combination
    if not (mat==newMatrix):
        done=True
    return (newMatrix2,done,newGrade)

# Right

def MoveRight(mat,grade):
    newGrade=grade
    newMatrix=getEmptyMatrix()
    # Movement check
    done=False
    # Move right to left
    for i in range(GAME_SIZE):
        count=GAME_SIZE-1
        for j in range(GAME_SIZE):
            j=GAME_SIZE-j-1
            if mat[i][j]!=0:
                newMatrix[i][count]=mat[i][j]
                count-=1
    # Addition of neighbouring number
    for i in range(GAME_SIZE):
         for j in range(GAME_SIZE-1):
             j=GAME_SIZE-j-1
             if newMatrix[i][j]==newMatrix[i][j-1] and newMatrix[i][j]!=0:
                 newMatrix[i][j]*=2
                 newGrade+=newMatrix[i][j]
                 newMatrix[i][j-1]=0
    # Move all from left to right
    newMatrix2=getEmptyMatrix()
    for i in range(GAME_SIZE):
        count=GAME_SIZE-1
        for j in range(GAME_SIZE):
            j=GAME_SIZE-j-1
            if newMatrix[i][j]!=0:
                newMatrix2[i][count]=newMatrix[i][j]
                count-=1
    # Check for successful combination
    if not (mat==newMatrix):
        done=True
    return (newMatrix2,done,newGrade)

# Start app        
def startGame():
    root.destroy()
    gamegrid = Game2048()

# Rules
if __name__=='__main__':
    root = Tk()             # initiate app
    root.title("Rules")    
    root.geometry('500x380')
    Label(root, text="Rules", bg="#ffe4c7", justify=CENTER, font=("Verdana", 40, "bold"), width=6, height=1).pack()
    rule="\n\n2048 has 18 boxes, at start, there will be 2 boxes \nfill with 2 or 4, you can choose to move left, right, \nup or down. Everytime you swipe, the numbers will \nall move to that certain direction. New numbers will \nappear at the empty boxes and only in the form of 2 \nor 4. When numbers collide with each other, the \nnumbers will be added together. The game will end \nwhen the number 2048 is formed.\n\n Controls: W (Up) A (Left) S (Down) D (Right)\n"
    Label(root, text=rule, justify=CENTER, font=("Verdana", 12)).pack()
    Button(root, text="Start", command=startGame,bg="#ffe4c7",width=20).pack()
    root.mainloop() 