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
  
  def combineValues(self, arr):
    counter = 0
    #for each value
    for i in range(0, len(arr)-1):
      if i > len(arr)-1 or i+1 > len(arr)-1:
        break
      #if the shifted values are the same, combine them
      if arr[i] == arr[i+1]:
        arr[i] *= 2
        arr.pop(i+1)
        counter+= 1
    return counter

  #Perform a left shift on the game grid
  def leftShift(self):
    tempState = copy.deepcopy(self.gameGrid)
    for i in range(0, self.y):
      #remove zeros form array
      self.gameGrid[i] = list(filter(lambda num: num != 0, self.gameGrid[i]))
      #combine values 
      k = self.combineValues(self.gameGrid[i])
      #reapply values
      for j in range(0, (self.y)-(len(self.gameGrid[i]))):
        self.gameGrid[i].append(0)
    if self.gameGrid == tempState:
      return
    #Spawn new tile
    self.generateTile()
    #Add to the process string
    self.processString += "L"

  #Perform a right shift on the grid
  def rightShift(self):
    tempState = copy.deepcopy(self.gameGrid)
    for i in range(0, self.y):
      #remove zeros from list
      self.gameGrid[i] = list(filter(lambda num: num != 0, self.gameGrid[i]))
      #reverse so the same combine function can be used
      self.gameGrid[i].reverse()
      k = self.combineValues(self.gameGrid[i])
      #re-reverse
      self.gameGrid[i].reverse()
      #replace values
      for j in range(0, (self.y)-(len(self.gameGrid[i]))):
        self.gameGrid[i].insert(0, 0)
    if self.gameGrid == tempState:
      return
    #Spawn new tile
    self.generateTile()
    #Add process to the path string
    self.processString += "R"

  #perform an up shift on the entire grid
  def upShift(self):
    tempState = copy.deepcopy(self.gameGrid)
    for i in range(0, self.x):
      downarr = []
      #formulate an array from the columns
      for j in range(0, self.y):
        downarr.append(self.gameGrid[j][i])
        #remove zeros
      downarr = list(filter(lambda num: num != 0, downarr))
      #reverse so the function can be used
      downarr.reverse()
      k = self.combineValues(downarr)
      #reinsert the zeros
      for j in range(0, (self.y)-(len(downarr))):
        downarr.insert(0, 0)
      #re-reverse
      downarr.reverse()
      #reinsert values to grid
      for j in range(0, self.y):
        self.gameGrid[j][i] = downarr[j]
    if self.gameGrid == tempState:
      return
    #Spawn new tile
    self.generateTile()
    #Append the process to the processString
    self.processString += "U"
  
  #perform a down shift on the grid
  def downShift(self):
    tempState = copy.deepcopy(self.gameGrid)
    for i in range(0, self.x):
      downarr = []
      #formulate an array with the correct column values
      for j in range(0, self.y):
        downarr.append(self.gameGrid[j][i])
      #remove zeros
      downarr = list(filter(lambda num: num != 0, downarr))
      #combine values
      k = self.combineValues(downarr)
      #readd zeros
      for j in range(0, (self.y)-(len(downarr))):
        downarr.insert(0, 0)
      #reapply values to grid
      for j in range(0, self.y):
        self.gameGrid[j][i] = downarr[j]
    if self.gameGrid == tempState:
      return
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
    print(self.processString)
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