import numpy as np
import matplotlib.pyplot as plot
import copy
import math
import time

#Variables
Workspace = [300,200]
GoalNode = []
StartNode = []
Obstaclesx = []
Obstaclesy = []
ExploredNodes = []
node = []
CurrentNode = []
ParentNodeIndex = []
CurrentNodeIndex = 0
Path = []
NodePath = []
Cost = []
nodeString =[]
radius = int(input("Enter the radius of the robot: "))
clearance = int(input("Enter clearance: "))
#Blank Map Matrix
BlankMap = np.zeros((201,301))
#Fucntion to find equation of line between two points:
def FindLineEqn(x1,y1,x2,y2):
    slope = (y2-y1)/(x2-x1)
    c = y1-slope*x1
    return slope,c
# print(FindLineEqn(75,85,50,150))

def GenerateMap():
    Map = copy.deepcopy(BlankMap)
    for x in range(301):
        for y in range(201):

            if((x-225)**2 + (y-150)**2 <= (25 + clearance + radius)**2):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if(((x-150)**2/(40 + clearance + radius)**2 + (y-100)**2/(20 + clearance + radius)**2) <= 1):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if ((y-(0.6*x))>=(-125 - clearance - radius) and (y-(-0.6*x))<=(175 + clearance + radius) and (y-(0.6*x))<=(-95 + clearance + radius) and (y-(-0.6*x))>=(145 - clearance - radius)):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if((y-(13*x))<=(-140 + clearance + radius) and (y-(1*x))>=(100 - clearance - radius) and y <= (185 + clearance + radius) and (y-(1.4*x)>=(80 - clearance - radius))):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if ((y-(-1.2*x))>=(210 - clearance - radius) and (y-(1.2*x))>=(30 - clearance - radius) and (y-(-1.4*x))<=(290 + clearance + radius) and (y-(-2.6*x))>=(280 - clearance - radius) and y<=(185 + clearance + radius)):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if ((y - (1.73)*x + 135 >= 0 - clearance - radius) and (y + (0.58)*x - 96.35  <= 0 + clearance + radius) and (y - (1.73)*x - 15.54 <= 0 + clearance + radius) and (y + (0.58)*x - 84.81 >= 0 - clearance - radius)):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if ((y <=  clearance + radius)):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if ((x <= clearance + radius)):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if ((x >= 300  - (clearance + radius)  )):
                Map[200 - y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)
            if ((200 >= y >=  200 - (clearance + radius))):
                Map[200-y][x] = 1
                Obstaclesx.append(x)
                Obstaclesy.append(y)

    return Map

# Map = GenerateMap()
def GenerateWorkspace():
    plot.plot(Workspace[0],Workspace[1])
    plot.plot(StartNode[0], StartNode[1], "rx", markersize = '5')
    plot.plot(GoalNode[0], GoalNode[1], "go", markersize = '5')
    plot.scatter(Obstaclesx,Obstaclesy,color = 'b')
    # plot.show()


def GetUserInput():
    global StartNode
    global GoalNode
    global Radius
    global clearance

    while(True):
        print("Enter the co-ordinates of starting point separated by space  (x,y) --> x y:")
        StartNode = list(map(int, input().split()))
        if (len(StartNode)==2) and not(InObstacleSpace(StartNode)):
            break
        else:
            print("Please provide valid starting point")

    while(True):
        print("Enter the co-ordinates of goal point separated by space  (x,y) --> x y: ")
        GoalNode = list(map(int, input().split()))
        if len(GoalNode)==2 and not(InObstacleSpace(GoalNode)):
            break
        else:
             print("Please provide valid goal point")

#Function to check if the Node is in  Obstacle Space
def InObstacleSpace(Node):
    if(Map[200-Node[1]][Node[0]]) == 1:
        return True
    else:
        return False
# print(InObstacleSpace([25,185]))

#Functions for motion
def ActionMoveLeft(CurrentNode):
    if CurrentNode[0] > 0:
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[0] = CurrentNode[0] - 1
        return NewNode
# print("Move Left",ActionMoveLeft(CurrentNode))
# print("CurrentNode",CurrentNode)

def ActionMoveRight(CurrentNode):
    if CurrentNode[0] < Workspace[0] :
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[0]  = CurrentNode[0] + 1
        return NewNode
# print("Move Right",ActionMoveRight(CurrentNode))
# print("CurrentNode",CurrentNode)

def ActionMoveUp(CurrentNode):
    if CurrentNode[1] < Workspace[1] :
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[1]  = CurrentNode[1] + 1
        return NewNode
# print("Move Up",ActionMoveUp(CurrentNode))
# print("CurrentNode",CurrentNode)

def ActionMoveDown(CurrentNode):
    if CurrentNode[1] > 0 :
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[1]  = CurrentNode[1] - 1
        return NewNode
# print("Move Down",ActionMoveDown(CurrentNode))
# print("CurrentNode",CurrentNode)

def ActionMoveUpLeft(CurrentNode):
    if (CurrentNode[0] > 0) and (CurrentNode[1] < Workspace[1]):
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[0],NewNode[1]  = CurrentNode[0] - 1 , CurrentNode[1]+1
        return NewNode
# print("Move UpLeft",ActionMoveUpLeft(CurrentNode))
# print("CurrentNode",CurrentNode)

def ActionMoveUpRight(CurrentNode):
    if (CurrentNode[0] < Workspace[0]) and (CurrentNode[1] < Workspace[1]):
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[0],NewNode[1]= CurrentNode[0] + 1 , CurrentNode[1]+1
        return NewNode
# print("Move UpRight",ActionMoveUpRight(CurrentNode))
# print("CurrentNode",CurrentNode)

def ActionMoveDownLeft(CurrentNode):
    if (CurrentNode[0] > 0) and (CurrentNode[1] > 0):
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[0],NewNode[1] = CurrentNode[0] - 1 , CurrentNode[1]-1
        return NewNode
# print("Move DownLeft",ActionMoveDownLeft(CurrentNode))
# print("CurrentNode",CurrentNode)

def ActionMoveDownRight(CurrentNode):
    if (CurrentNode[0] < Workspace[0]) and (CurrentNode[1] > 0) :
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[0],NewNode[1] = CurrentNode[0] + 1 , CurrentNode[1]-1
        return NewNode
# print("Move DownRight",ActionMoveDownRight(CurrentNode))
# print("CurrentNode",CurrentNode)

#Function to check if a node is new and add it to the list
def AddNode(NewNode):
    global CurrentNodeIndex
    global CurrentNode
    global Map

    if (Map[200-NewNode[1]][NewNode[0]]) != 1 :
        node.append(NewNode)
        ParentNodeIndex.append(CurrentNodeIndex)
        Map[200-NewNode[1]][NewNode[0]] = 1
        # plot.scatter(NewNode[0],NewNode[1])
        # plot.pause(0.000001)

def GeneratePath(CurrentNode):
    global CurrentNodeIndex
    Path.append(CurrentNodeIndex)
    while(Path[0] != 0):
        Path.insert(0,ParentNodeIndex[node.index(CurrentNode)])
        CurrentNode = node[Path[0]]

    for i in range(len(Path)):
        NodePath.append(node[Path[i]])

def Dijkstra(InitialNode):
    global StartNode
    global GoalNode
    global CurrentNode
    global CurrentNodeIndex
    global Map
    CurrentNode = copy.deepcopy(InitialNode)
    node.append(CurrentNode)
    ParentNodeIndex.append(CurrentNodeIndex)
    plotX = []
    plotY = []
    while(((CurrentNode[0] != GoalNode[0]) or (CurrentNode[1] != GoalNode[1]))):

        if(ActionMoveLeft(CurrentNode) is not None):
            AddNode(ActionMoveLeft(CurrentNode))
        # print("CurrentNode",CurrentNode,"Right",ActionMoveRight(CurrentNode))
        if(ActionMoveRight(CurrentNode) is not None):
            AddNode(ActionMoveRight(CurrentNode))
        if(ActionMoveUp(CurrentNode) is not None):
            AddNode(ActionMoveUp(CurrentNode))
        if(ActionMoveDown(CurrentNode) is not None):
            AddNode(ActionMoveDown(CurrentNode))
        if(ActionMoveUpLeft(CurrentNode) is not None):
            AddNode(ActionMoveUpLeft(CurrentNode))
        if(ActionMoveUpRight(CurrentNode) is not None):
            AddNode(ActionMoveUpRight(CurrentNode))
        if(ActionMoveDownLeft(CurrentNode) is not None):
            AddNode(ActionMoveDownLeft(CurrentNode))
        if(ActionMoveDownRight(CurrentNode) is not None):
            AddNode(ActionMoveDownRight(CurrentNode))
        plotX.append(CurrentNode[0])
        plotY.append(CurrentNode[1])

        CurrentNodeIndex += 1
        if(CurrentNodeIndex >= len(node)):
            return False
        # print("CurrentNodeIndex",CurrentNodeIndex)
        CurrentNode = node[CurrentNodeIndex]
        if(len(plotX)%5000 == 0):
            plot.plot(plotX,plotY,'.k')
            plot.pause(0.001)
            plotX = []
            plotY = []
    plot.plot(plotX, plotY, '.k')
    plot.pause(0.001)
    plotX = []
    plotY = []

    return CurrentNode

Map = GenerateMap()
GetUserInput()
StartTime = time.time()
GenerateWorkspace()
print("Solving")
GoalNode = Dijkstra(StartNode)
if (GoalNode != False):
    GeneratePath(GoalNode)
    NodePathX = [x[0] for x in NodePath]
    NodePathY = [x[1] for x in NodePath]
    EndTime = time.time()
    print("Solved" , EndTime - StartTime)
    plot.plot(StartNode[0], StartNode[1], "rx", markersize='15')
    plot.plot(GoalNode[0], GoalNode[1], "bo", markersize='15')
    plot.plot(NodePathX,NodePathY,'r',linewidth = 1)
    plot.show()
else:
    EndTime = time.time()
    print("No Solution" , EndTime - StartTime)
    # print("No Solution")