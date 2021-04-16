import pygame
import time
import math
import numpy as np
from matplotlib import pyplot as plt

def obstacleOrNot(point, clearance = 5):
    """
        Check whether the point is inside or outside the
        defined obstacles and clearance.
        Note: The obstacles have been defined using half 
        plane method
        Input: point/testCase(tuple)
        Return: Boolean(True or False)
    """
    x = point[0]
    y = point[1]
    
    if (x<0) or (x>1000) or (y<0) or (y>1000):
        return False
    
    # circle1
    elif((x-200)**2 + (y-200)**2 - (100 + clearance)**2 < 0): #circle
        return False
    
    # circle2
    elif((x-200)**2 + (y-800)**2 - (100 + clearance)**2 < 0): #circle
        return False
    
    # Square
    elif(((x-25+clearance>0) and (x-175-clearance<0)) and ((y-425+clearance>0) and (y-575-clearance<0))):
        return False
    
    # Horizontal Rectangle
    elif(((x-375+clearance>0) and (x-625-clearance<0)) and ((y-425+clearance>0) and (y-575-clearance<0))):
        return False
    
    # Vertical Rectangle
    elif(((x-725+clearance>0) and (x-875-clearance<0)) and ((y-200+clearance>0) and (y-400-clearance<0))):
        return False
    
    else:
        return True


class A_Star:
    """
    Class created to implement queue for A star
    Maintains a list of nodes with another list
    maintaining the cost of each node.
    """

    def __init__(self, node, goalPoint):
        """
        Initialize a A_Star object corresponding to a
        start point.
        Input: node(tuple)
        Return:
        """

        self.goalPoint = goalPoint
        self.step_size = 0

        self.queue = [node]

        self.cost_to_come = {node:0}
        self.cost= {node:0+self.euclideanDistance(node)}

        self.child_parent_rel = {node:(0,0)}
        
       


    def euclideanDistance(self, node):
        """
        Generate a priority number for each node by the extent of
        arrangement i.e., checking the distance from current node
        to the goal node.

        Input: self,testCase/node

        Returns: Priority of the input node

        """
        
        d = math.sqrt((node[0]-self.goalPoint[0])**2 + (node[1]-self.goalPoint[1])**2)
        return d

    def insert(self, node, new_node):
        """
        Insert an element in the queue and also store its
        cost to come and cost incase the current cost is greater than new 
        cost
        Input: self, node(tuple), new_node(tuple), cost(float)
        Returns: None
        """
        self.queue.append(new_node)

        if (new_node not in self.child_parent_rel) or (self.child_parent_rel[new_node][1] > self.cost[new_node]):
            cost_to_come = self.cost_to_come[node] +  self.step_size

            self.cost_to_come[new_node] = cost_to_come
            cost = cost_to_come + self.euclideanDistance(new_node)

            self.child_parent_rel[new_node] = [node, cost]
            self.cost[new_node] = cost
        
    def extract(self):
        """
        Pop a point which has the minimum cost
        from the queue.
        Input: None
        Returns: The node with the minimum
        cost(tuple)
        """
        key_of_minimum_cost = min(self.cost, key=self.cost.get)
        #print(self.queue)
        #print(self.cost[key_of_minimum_cost],key_of_minimum_cost,self.cost_to_come[key_of_minimum_cost])
        self.cost.pop(key_of_minimum_cost)
        self.queue.remove(key_of_minimum_cost)

        
        return key_of_minimum_cost


class MovePoint:
    """
    Class that is used to do decide point moving opeartion
    and processing which includes generating possible moves for the
    point.
    """

    def __init__(self, startPoint, goalPoint, size, theta):
        """
        Initialize the MovePoint object corresponding to a
        start point, goal point, step size, size of arena and the algorithm 
        to use.
        
        Input: startPoint(tuple), endPoint(tuple),
        size(tuple), algo(str)
        Return: None
        """
        self.goalPoint = goalPoint

        self.queue = A_Star(startPoint,goalPoint)

        self.size = size
        self.visited = {startPoint:0}

        self.theta = {startPoint:np.radians(theta)}


    def cost(self, node, Thetai, action):

        t = 0
        # r = 0.038
        # L = 0.354
        r = 3.8
        L = 35.4
        dt = 0.1
        Xn= node[0]
        Yn= node[1]
        
        Thetan = Thetai

        D=0
        while t<1:
            t = t + dt
            Delta_Xn = 0.5*r * (action[0] + action[1]) * math.cos(Thetan) * dt
            Delta_Yn = 0.5*r * (action[0] + action[1]) * math.sin(Thetan) * dt
            Xn += Delta_Xn
            Yn += Delta_Yn
            Thetan += (r / L) * (action[1] - action[0]) * dt
            #D += math.sqrt(math.pow((0.5*r * (action[0] + action[1]) * math.cos(Thetan) * dt),2)+math.pow((0.5*r * (action[0] + action[1]) * math.sin(Thetan) * dt),2))
        D = math.sqrt(math.pow((Xn - node[0]),2)+math.pow((Yn - node[1]),2))
        
        return (int(Xn), int(Yn)), Thetan, D

    def nodeOperation(self, node, theta, action):
        """
        Generate the next node based on the operation and
        the node
        Input: node/point(tuple), moveCost(float),
        *args(list), **kwargs(dict)
        Return: True/False(Bool)
        """
        
        newNode = False

        if(obstacleOrNot(node)):
            newNode, new_theta, new_step_size= self.cost(node, theta, action)
            self.queue.step_size = new_step_size
        
        if(newNode and obstacleOrNot(newNode) and newNode not in self.visited):
            self.visited[newNode] = 0
            self.theta[newNode] = new_theta
            self.queue.insert(node, newNode)
            
        return False

    def pointProcessor(self):
        """
        Process the point moving operation and check if the
        goal node is achived or not.
        Input: self
        Return: True/False(Bool)
        """
        queue = self.queue

        size = self.size
        goalPoint = self.goalPoint
        visited = self.visited
        
        node= queue.extract()

        if(queue.euclideanDistance(node)<15):
            if (goalPoint != node):
                self.queue.child_parent_rel[goalPoint] = [node,0]
            return True


        operationParams = [[15,15], [20,20],[15,0],[0,15],[15,20],[20,15]]

        # print("#######"+str(node))
        for action in operationParams:
            self.nodeOperation(node, self.theta[node], action)
        # print("#######")
        return False 
        
    def backTrace(self,startPoint):
        """
        Back trace the path from goal point to start point
        Input: self,startPoint(tuple)
        Return: backTraceArr(list)
        """
        goalPoint = self.goalPoint

        child_parent_relation = self.queue.child_parent_rel
        backTraceArr = []

        
        
        node =  child_parent_relation[goalPoint][0]
        while(node != startPoint):
            # print(child_parent_relation)
            # print(node)
            node = child_parent_relation[node][0]
            backTraceArr.append(node)
        return backTraceArr, child_parent_relation, self.theta

def to_pygame(coords):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], 1000 - coords[1])

def triangle(gameDisplay,colour,start,end,angle):
    """
    Draw a triangle at the point given the start and end points and the angle.
    """
    rotation = angle
    t1 = to_pygame((end[0]+2*math.sin(math.radians(rotation)), end[1]+2*math.cos(math.radians(rotation))))
    t2 = to_pygame((end[0]+2*math.sin(math.radians(rotation-120)), end[1]+2*math.cos(math.radians(rotation-120))))
    t3 = to_pygame((end[0]+2*math.sin(math.radians(rotation+120)),end[1]+2*math.cos(math.radians(rotation+120))))
    pygame.draw.polygon(gameDisplay, colour, (t1, t2, t3))


def main():
    print("\n")
    print(r"""    ____        __  __       ____  __                           
   / __ \____ _/ /_/ /_     / __ \/ /___ _____  ____  ___  _____
  / /_/ / __ `/ __/ __ \   / /_/ / / __ `/ __ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /_/ / / /  / ____/ / /_/ / / / / / / /  __/ /    
/_/    \__,_/\__/_/ /_/  /_/   /_/\__,_/_/ /_/_/ /_/\___/_/     
                                                                
""")
    
    x1 = int(input("\nEnter the x coordinate of the start point: "))
    y1 = int(input("Enter the y coordinate of the start point: "))

    x2 = int(input("Enter the x coordinate of the goal point: "))
    y2 = int(input("Enter the y coordinate of the goal point: "))

    

    theta = int(input("Enter the theta of the start point: "))
    print("\n")
    
    start = time.time()
    startPoint = (x1,y1)
    endPoint = (x2,y2)
    arenaSize = (1000,1000)

    if((not obstacleOrNot(startPoint)) or (startPoint[0] > arenaSize[0]) or (startPoint[1] > arenaSize[1])):
        outStr = "Error: Start Point either on/inside obstacle or outside specified arena"
        print("#"*len(outStr))
        print("\n"+outStr+"\n")
        print("#"*len(outStr))
        print("\n")
        return False
    if((not obstacleOrNot(endPoint)) or (endPoint[0] > arenaSize[0]) or (endPoint[1] > arenaSize[1])):
        outStr = "Error: Goal either on/inside obstacle or outside specified arena"
        print("#"*len(outStr))
        print("\n"+outStr+"\n")
        print("#"*len(outStr))
        print("\n")
        return False

    

    

    move = MovePoint(startPoint,endPoint,arenaSize,theta)  
    flag = False
    while(not flag):
        flag = move.pointProcessor()
    
    backTraceArr, child_parent_rel, theta = move.backTrace(startPoint)
    end = time.time()
    finalOut = f"\nPath found in {round(end - start, 4)} seconds.\n"
    print(finalOut)
    
    pygame.init()

    pygame.display.set_caption("Path Planner")

    white = (255,255,255)
    black = (0,0,0)
    
    yellow = (255,255,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255,10)


    gameDisplay = pygame.display.set_mode((1000,1000))
    gameDisplay.fill(white)
    
    for i in range(1000):
        for j in range(1000):
            if not obstacleOrNot([i,j],0):
                pygame.draw.circle(gameDisplay, red, to_pygame((i,j)),1)
            elif not obstacleOrNot([i,j]):
                pygame.draw.circle(gameDisplay, green, to_pygame((i,j)),1)
    # rect_cl = [(46.77,101.02),(177.81,192.745),(160.615,217.33),(29.58,125.604)]
    # newCoords = [to_pygame(x) for x in rect_cl]
    # pygame.draw.polygon(gameDisplay, green, newCoords)
    
    # rect = [(48,108),(170.87,194.04),(159.40,210.42),(36.53,124.383)]
    # newCoords = [to_pygame(x) for x in rect]
    # pygame.draw.polygon(gameDisplay, red, newCoords)

    # pygame.draw.circle(gameDisplay, green, to_pygame((90,70)),40)
    # pygame.draw.circle(gameDisplay, red, to_pygame((90,70)),35)
    
    # ellipseCenter = to_pygame((181,180))
    # ellipse = (ellipseCenter[0],ellipseCenter[1],130,70)
    # pygame.draw.ellipse(gameDisplay, green, ellipse)
    
    # ellipseCenter = to_pygame((186,175))
    # ellipse_cl = (ellipseCenter[0],ellipseCenter[1],120,60)
    # pygame.draw.ellipse(gameDisplay, red, ellipse_cl)

    # polygon = [(195,225),(235,225),(235,245),(215,245),(215,265),(235,265),(235,285),(195,285)]
    # newPolygon = [to_pygame(x) for x in polygon]
    # pygame.draw.polygon(gameDisplay, green, newPolygon)
    
    # polygon = [(200,230),(230,230),(230,240),(210,240),(210,270),(230,270),(230,280),(200,280)]
    # newPolygon = [to_pygame(x) for x in polygon]
    # pygame.draw.polygon(gameDisplay, red, newPolygon)

    clock = pygame.time.Clock()
    
    while True:
        pygame.event.get()
        
        pygame.draw.circle(gameDisplay, black, to_pygame(endPoint),2)
        for key in move.visited.keys():
            if child_parent_rel[key][0]:
                pygame.draw.line(gameDisplay,blue,to_pygame(key),to_pygame(child_parent_rel[key][0]))
            clock.tick(10000000)
            pygame.display.update()
        backTraceArr = backTraceArr[::-1]
        for point in range(len(backTraceArr)-1):
            pygame.draw.line(gameDisplay, black, to_pygame(backTraceArr[point]),to_pygame(backTraceArr[point+1]),width=2)
            triangle(gameDisplay,black,backTraceArr[point],backTraceArr[point+1],theta[backTraceArr[point]])
            clock.tick(1000000)
            pygame.display.update()
        
        time.sleep(10)
        pygame.quit()
        quit()

if __name__ == '__main__':
    main()