#Module: GameState.py
from random import randint

class GameState:

  def __init__(self, inputGrid, inputPool, targetNum):
    self.gameGrid = inputGrid   #the 2d array representing the game board
    self.x = len(inputGrid[0])-1  #the height of the board
    self.y = len(inputGrid)-1     #the width of the board 
    self.spawnPool = inputPool  #The array of the spawn pattern
    self.processString = ""     #A string keeping track of the path
    self.weight = 0
    self.targetNum = targetNum

  def __lt__(self, other):
    return self.weight < other.weight
  
  def __eq__(self, other):
    return self.processString == other.processString

  def fast_copy(self):
    copy_object = GameState([list(x) for x in self.gameGrid], [x for x in self.spawnPool], self.targetNum)
    copy_object.processString = self.processString
    return copy_object

  #Generate a new tile in the grid
  def generateTile(self):
    #Determine where to generate a new tile
    #check top left
    if self.gameGrid[0][0] == 0:
      self.gameGrid[0][0] = self.spawnPool[0]

    #check top right
    elif self.gameGrid[0][self.x] == 0:
      self.gameGrid[0][self.x] = self.spawnPool[0]

    #check bottom right
    elif self.gameGrid[self.y][self.x] == 0:
      self.gameGrid[self.y][self.x] = self.spawnPool[0]

    #check bottom left
    elif self.gameGrid[self.y][0] == 0:
      self.gameGrid[self.y][0] = self.spawnPool[0]

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
    tempState = self.fast_copy()
    for i in range(0, self.y+1):
      #remove zeros form array
      self.gameGrid[i] = list(filter(lambda num: num != 0, self.gameGrid[i]))
      #combine values 
      k = self.combineValues(self.gameGrid[i])
      #reapply values
      for j in range(0, (self.x)-(len(self.gameGrid[i])-1)):
        self.gameGrid[i].append(0)
    if self.gameGrid == tempState.gameGrid:
      return False
    #Spawn new tile
    self.generateTile()
    self.getWeight()
    #Add to the process string
    self.processString += "L"
    return True

  #Perform a right shift on the grid
  def rightShift(self):
    tempState = self.fast_copy()
    for i in range(0, self.y+1):
      #remove zeros from list
      self.gameGrid[i] = list(filter(lambda num: num != 0, self.gameGrid[i]))
      #reverse so the same combine function can be used
      self.gameGrid[i].reverse()
      k = self.combineValues(self.gameGrid[i])
      #re-reverse
      self.gameGrid[i].reverse()
      #replace values
      for j in range(0, (self.x)-(len(self.gameGrid[i])-1)):
        self.gameGrid[i].insert(0, 0)
    if self.gameGrid == tempState.gameGrid:
      return False
    #Spawn new tile
    self.generateTile()
    self.getWeight()
    #Add process to the path string
    self.processString += "R"
    return True 

  #perform an up shift on the entire grid
  def upShift(self):
    tempState = self.fast_copy()
    for i in range(0, self.x+1):
      downarr = []
      #formulate an array from the columns
      for j in range(0, self.y+1):
        downarr.append(self.gameGrid[j][i])
        #remove zeros
      downarr = list(filter(lambda num: num != 0, downarr))
      #reverse so the function can be used
      downarr.reverse()
      k = self.combineValues(downarr)
      #reinsert the zeros
      for j in range(0, (self.y)-(len(downarr)-1)):
        downarr.insert(0, 0)
      #re-reverse
      downarr.reverse()
      #reinsert values to grid
      for j in range(0, self.y+1):
        self.gameGrid[j][i] = downarr[j]
    
    if self.gameGrid == tempState.gameGrid:
      return False
    #Spawn new tile
    self.generateTile()
    self.getWeight()
    #Append the process to the processString
    self.processString += "U"
    return True
  
  #perform a down shift on the grid
  def downShift(self):
    tempState = self.fast_copy()
    for i in range(0, self.x+1):
      downarr = []
      #formulate an array with the correct column values
      for j in range(0, self.y+1):
        downarr.append(self.gameGrid[j][i])
      #remove zeros
      downarr = list(filter(lambda num: num != 0, downarr))
      #combine values
      k = self.combineValues(downarr)
      #readd zeros
      for j in range(0, (self.y)-(len(downarr)-1)):
        downarr.insert(0, 0)
      #reapply values to grid
      for j in range(0, self.y+1):
        self.gameGrid[j][i] = downarr[j]
    if self.gameGrid == tempState.gameGrid:
      return False
    #Spawn new tile
    self.generateTile()
    self.getWeight()
    #Append the process to the processString
    self.processString += "D"
    return True
  
  #check the win condiditon of the game
  def isWin(self):
    #check the entire grid for the target value
    for r in self.gameGrid:
      for i in r:
        if(i == self.targetNum):
          return True;
    #else, you have not won (yet!)
    return False
  #simple function to output the grid in it's current state
  def printState(self):
    print(len(self.processString))
    print("Weight:", self.weight)
    print(self.processString)
    for r in self.gameGrid:
      for i in r:
        print(i, end=' ')
      print()
  
  # '''
  # Old heuristic
  # def getWeight(self):
  #   score = 0
  #   for r in self.gameGrid:
  #     for i in range(0, len(r)):
  #       score += r[i]
  #   # Heuristic:
  #   # Sum of every tile on the board, divided by the number
  #   #   of available tile spaces. This is similar to the 2048 
  #   #   scoring system, which gives points based on combined 
  #   #   tile values. I multiply this by a psudorandom number
  #   #   (seeded value) to prevent very similar boards from
  #   #   creating a loop (such as [UDUDUDUDU]) and when 0,
  #   #   trims the nodes to be tried for a solution.
  #   self.weight = (score/(self.x+1 * self.y+1)) * randint(0,5)
  #   '''
    
  
  #This heuristic struggles to solve 4096 without hitting max recusion depth
  # '''
  def getWeight(self):
    values = []
    for i in self.gameGrid:
      for j in i:
        values.append(j)
    self.combineValues(values)
    values.sort()
    values.reverse()
    if(values[0] >= self.targetNum):
      return 1
    else:
      return (1+self.distancePredictor(values, list(self.spawnPool)))

  def distancePredictor(self, values, spawns):
    #print(values)
    values.append(spawns[0])
    spawns.append(spawns.pop(0))
    self.combineValues(values)
    values.sort()
    values.reverse()
    if(values[0] >= self.targetNum):
      return 1
    else:
      return (1+self.distancePredictor(values, spawns))