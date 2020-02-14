import sys
import copy
from timeit import default_timer as timer

class GameState:

  def __init__(self, inputGrid, inputPool):
    self.gameGrid = inputGrid   #the 2d array representing the game board
    self.x = len(inputGrid[0])  #the height of the board
    self.y = len(inputGrid)     #the width of the board 
    self.spawnPool = inputPool  #The array of the spawn pattern
    self.processString = ""     #A string keeping track of the path

  #Generate a new tile in the grid
  def generateTile(self):
    #Determine where to generate a new tile
    #check top left
    if self.gameGrid[0][0] == 0:
      self.gameGrid[0][0] = self.spawnPool[0]

    #check top right
    elif self.gameGrid[0][self.x-1] == 0:
      self.gameGrid[0][self.x-1] = self.spawnPool[0]

    #check bottom right
    elif self.gameGrid[self.x-1][self.y-1] == 0:
      self.gameGrid[self.x-1][self.y-1] = self.spawnPool[0]

    #check bottom left
    elif self.gameGrid[0][self.y-1] == 0:
      self.gameGrid[0][self.y-1] = self.spawnPool[0]

    #spawning fails
    else:
      return
    
    # Cycle the spawnPool
    self.spawnPool.append(self.spawnPool.pop(0))
  
  #Perform a left shift on the game grid
  def leftShift(self):
    for r in self.gameGrid:
      counter = 0
      #Determine the number of shifts to perform
      for i in range(len(r)):
          if r[i] == 0:
            counter += 1
      #Remove zeros from row
      r[:] = [x for x in r if x != 0]
      #Loop over & Combine numbers
      if(len(r) > 1):
        counter2 = 0
        for i in range(0, len(r)-1):
          if(r[i-counter2] == r[i+1-counter2]):
            r[i]=r[i]*2
            counter2 += (1)
            r.pop(i-2)
            counter += 1
      #Append zeros
      for i in range(counter):
        r.append(0)
    #Spawn new tile
    self.generateTile()
    #Add to the process string
    self.processString += "L"

  #Perform a right shift on the grid
  def rightShift(self):
    for r in self.gameGrid:
      counter = 0
      #Find number of shifts to perform
      for i in range(len(r)):
          if r[i] == 0:
            counter += 1
      #remove shifts
      r[:] = [x for x in r if x != 0]
      #combine same numbers
      if(len(r) > 1):
        for i in range(len(r)-1, 0, -1):
          if(r[i] == r[i-1]):
            r[i]=r[i]*2
            r.pop(i-1)
            counter += 1
      #Append zeroes to fill row
      for i in range(counter):
        r.insert(0,0)
    #Spawn new tile
    self.generateTile()
    #Add process to the path string
    self.processString += "R"

  #perform an up shift on the entire grid
  def upShift(self):
    for i in range(0, self.x):
      colCount = i
      zeroCount = 0
      colTemp = []
      for r in self.gameGrid:
        #Count the number of zeros and save the order of the non-zeros
        if r[colCount] == 0:
          zeroCount += 1
        else:
          colTemp.append(r[colCount])
      #Combine same numbers
      if(len(colTemp) > 1):
        counter2 = 0
        for i in range(0, len(colTemp)-1):
          if(colTemp[i-counter2] == colTemp[i+1-counter2]):
            colTemp[i-counter2]=colTemp[i-counter2]*2
            colTemp.pop(i+1-counter2)
            counter2 += 1
            zeroCount += 1
      #Append zeros to the end of array
      for i in range(zeroCount):
        colTemp.append(0)
      #edit each column for the shifted values
      for r in self.gameGrid:
        r[colCount] = colTemp.pop(0)
    #Spawn new tile
    self.generateTile()
    #Append the process to the processString
    self.processString += "U"
  
  #perform a down shift on the grid
  def downShift(self):
    for i in range(0, self.x):
      colCount = i
      zeroCount = 0
      colTemp = []
      for r in self.gameGrid:
        #Count the number of zeros and save the order of the non-zeros
        if r[colCount] == 0:
          zeroCount += 1
        else:
          colTemp.append(r[colCount])
      #Combine same numbers
      if(len(colTemp) > 1):
        for i in range(len(colTemp)-1, 0, -1):
          if(colTemp[i] == colTemp[i-1]):
            colTemp[i]=colTemp[i]*2
            colTemp.pop(i-1)
            zeroCount += 1
      #append zeros to beginning
      for i in range(zeroCount):
        colTemp.insert(0, 0)
      #edit each column to the shifted values
      for r in self.gameGrid:
        r[colCount] = colTemp.pop(0)
    #Spawn new tile
    self.generateTile()
    #Append the process to the processString
    self.processString += "D"
  
  #check the win condiditon of the game
  def isWin(self):
    #check the entire grid for the target value
    for x in range(0, self.x):
      for y in range(0, self.y):
        if(self.gameGrid[x][y] == targetNum):
          return True;
    #else, you have not won (yet!)
    return False
  #simple function to output the grid in it's current state
  def printState(self):
    print(len(self.processString))
    print("Process: " + self.processString)
    for r in self.gameGrid:
      for i in r:
        print(i, end=' ')
      print()

#open the input file
f = open(sys.argv[1])

#read the target integer
targetNum = int(f.readline().rstrip())

#read the width and height, and split into respective variables
wh = f.readline().rstrip().split(" ")
width = int(wh[0])
height = int(wh[1])

#read in and format the spawning pattern into a list
pattern = f.readline().rstrip().split(" ")
for i in range(0, len(pattern)):
  pattern[i] = int(pattern[i])

#create a 2d array representation of the input grid
tempgrid = []
for i in range(0, height):
  templst = f.readline().rstrip().split(" ")
  for j in range(0, len(templst)):
    templst[j] = int(templst[j])
  tempgrid.append(templst)

#Create a game object with the input
game = GameState(tempgrid, pattern)


#BFTS Algorithm implementation
start = timer()
fullstart = start
isSolved = False
queue = []
while(not isSolved):
  isSolved = game.isWin()
  if(isSolved):
    break

  leftGame = copy.deepcopy(game)
  leftGame.leftShift()
  queue.append(leftGame)

  rightGame = copy.deepcopy(game)
  rightGame.rightShift()
  queue.append(rightGame)

  downGame = copy.deepcopy(game)
  downGame.downShift()
  queue.append(downGame)

  upGame = copy.deepcopy(game)
  upGame.upShift()
  queue.append(upGame)

  game = queue[0]
  queue.pop(0)


if(isSolved):
  end = timer()
  print(int(1000 * (end - fullstart)))
  game.printState()