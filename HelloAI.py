from GameState import GameState
import sys
import heapq
from random import seed
from random import randint
from timeit import default_timer as timer
from collections import defaultdict


def AStar(state):
  pq = []
  visited = {}
  heapq.heappush(pq, state)

  while(len(pq) != 0):
    node = heapq.heappop(pq)
    #Check if node is a win state
    if(node.isWin()):
      return node
    #Check if node has been visited
    #Find the hash value for this node
    hashValue = hash(node.processString)
    #If this value exists in the hashtable, we have already visited
    if visited.get(hashValue) is None:
      #add state to visited
      visited[hashValue] = node
      #the left shift child
      leftState = node.fast_copy()
      #If it is a valid move, add state to heapq
      if(leftState.leftShift()):
        #consider the weight of the state to the cost
        leftState.weight = leftState.weight + len(leftState.processString)
        heapq.heappush(pq, leftState)

      #the right shift child
      rightState = node.fast_copy()
      #If it is a valid move, add state to heapq
      if(rightState.rightShift()):
        #consider the weight of the state to the cost
        rightState.weight = rightState.weight + len(rightState.processString)
        heapq.heappush(pq, rightState)

      #the down shift child
      downState = node.fast_copy()
      #If it is a valid move, add state to heapq
      if(downState.downShift()):
        #consider the weight of the  state to the cost
        downState.weight = downState.weight + len(downState.processString)
        heapq.heappush(pq, downState)

      #the up shift child
      upState = node.fast_copy()
      #If it is a valid move, add state to heapq
      if(upState.upShift()):
        #consider the weight of the state to the cost
        upState.weight = upState.weight + len(upState.processString)
        heapq.heappush(pq, upState)

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
game = GameState(tempgrid, pattern, targetNum)

#Get Start time
start = timer()
fullstart = start

seed(1)
#Run algorithm
if(len(sys.argv) == 3):
  print("Bonus Not Implemented")
else:
  #Run algorithm
  finalNode = AStar(game)

  #Get finish time
  end = timer()

  #Output results
  print(int(1000 * (end - fullstart)))
  if(finalNode is not None):
    finalNode.printState()
  else:
    pass