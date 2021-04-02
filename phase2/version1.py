import pygame
import time
import math
from matplotlib import pyplot as plt
import numpy as np



def obstacleOrNot(point):
    """
        Check whether the point is inside or outside the
        defined obstacles.
        Note: The obstacles have been defined using half 
        plane method
        Input: point/testCase(tuple)
        Return: Boolean(True or False)
    """
    x = point[0]
    y = point[1]
    #circle
    if((x-90)**2 + (y-70)**2 - 50**2 < 0): #circle
        return False
    
    # tilted Rectangle
    # elif((8604*x - 12287*y + 914004 < 0) and (81900*x +59350*y-25510527 < 0) and (86036*x - 122870*y + 12140167 > 0) and (8192*x + 5735*y - 1012596 > 0)):
    #     return False
    
    # l1 = y - 0.7*x - 74.4
    l1 = y - 0.7*x - 56.09
    # l2 = y + 1.43*x - 176.64
    l2 = y + 1.43*x - 140.19
    # l3 = y - 0.7*x - 98.8
    l3 = y - 0.7*x - 117.11
    # l4 = y + 1.43*x - 438.37
    l4 = y + 1.43*x - 474.82
    
    if l1>0 and l2>0 and l3<0 and l4<0:
        return False
    
    # C shaped Polygon
    elif((x >= 185 and x <= 225 and y <= 295 and y >=215 ) or (x>= 225 and x <= 245 and y >=255 and y <= 295) or (y >= 215 and y <= 255 and x >= 225 and x <= 245)):
        return False
    
    # ellipse
    elif((((x-246)/75))**2 + (((y-145)/45))**2 - 1 < 0):
        return False
    
    else:
        return True

class A_Star:
    """
    Class created to implement queue for Djikstra
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
        self.queue = [node]
        self.cost = {node:0}
        self.child_parent_rel = {node:(0,0)}
        self.goalPoint = goalPoint


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

    def insert(self, node, new_node, cost):
        """
        Insert an element in the queue and also store its
        cost incase the current cost is greater than new 
        cost
        Input: self, node(tuple), new_node(tuple), cost(float)
        Returns: None
        """
        self.queue.append(new_node)

        if (new_node not in self.child_parent_rel) or self.child_parent_rel[new_node][1] > cost:
            cost += self.euclideanDistance(new_node)
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
        self.cost.pop(key_of_minimum_cost)
        self.queue.remove(key_of_minimum_cost)
        return key_of_minimum_cost


class MovePoint:
    """
    Class that is used to do decide point moving opeartion
    and processing which includes generating possible moves for the
    point.
    """

    def __init__(self, startPoint, goalPoint, theta, size):
        """
        Initialize the MovePoint object corresponding to a
        start point, goal point, size of arena and the algorithm 
        to use.
        
        Input: startPoint(tuple), endPoint(tuple),
        size(tuple), algo(str)
        Return: None
        """
        self.goalPoint = goalPoint
        self.theta = theta

        self.queue = A_Star(startPoint,goalPoint)

        self.size = size
        self.visited = {startPoint:0}
        self.cost = {startPoint:0}
        
    
    def nodeOperation(self, node, moveCost, *args):
        """
        Generate the next node based on the operation and
        the node
        Input: node/point(tuple), moveCost(float),
        *args(list), **kwargs(dict)
        Return: True/False(Bool)
        """
        
        newNode = False

        # if(y == "None"):
        #     if(obstacleOrNot(node) and node[0] != x):
        #         newNode = (node[0]+args[0],node[1]+args[1])
        # elif(x == "None"):
        #     if(obstacleOrNot(node) and node[1] != y):
        #         newNode = (node[0]+args[0],node[1]+args[1])
        # else:
        if(obstacleOrNot(node)):
            newNode = (node[0]+int(moveCost*math.cos(node[2] + args[0])),node[1]+int(moveCost*math.sin(node[2] + args[0])),(node[2] + args[0])%360)
        # if(newNode and self.goalPoint == newNode):
        if(newNode and self.queue.euclideanDistance(newNode) < 1.5):
                self.visited[newNode] = 0
                cost = self.cost[node] + moveCost
                self.cost[newNode] = cost
                # self.theta = self.theta + args[0]
                self.queue.insert(node, newNode, cost)
                
                self.visited[self.goalPoint] = 0
                cost = self.cost[newNode] + moveCost
                self.cost[self.goalPoint] = cost
                # self.theta = self.theta % 360
                self.queue.insert(newNode, self.goalPoint, cost)
                return True
        
        if(newNode and newNode not in self.visited):
            self.visited[newNode] = 0
            cost = self.cost[node] + moveCost
            self.cost[newNode] = cost
            # self.theta = self.theta + args[0]
            self.queue.insert(node, newNode, cost)
            
        return False


       

    def pointProcessor(self, step_size):
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
        #popping an element from the queue
        if(len(queue.queue) == 0):
            return True
        node= queue.extract()
        
        operationParams = [[step_size, 30], 
                            [step_size, 60], 
                            [step_size, 0], 
                            [step_size, -30], 
                            [step_size, -60]] 
        
        for param in operationParams:
            flag = self.nodeOperation(node, param[0],param[1])
            if flag == True:
                return True

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
        
        node = goalPoint
        while(node != startPoint):
            node = child_parent_relation[node][0]
            backTraceArr.append(node)
        return backTraceArr



def to_pygame(coords):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], 300 - coords[1])

def animate(*args):
    '''
    Animates the process of searching and finding
    
    input: Point coordinate
    output: Boolean, True if point is in circle
    '''
    
    return im

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
    
    step_size = int(input("Enter the step size for movement between 1 and 10: "))
    print("\n")
    
    start = time.time()
    theta = 30
    startPoint = (x1,y1,theta)
    endPoint = (x2,y2)
    arenaSize = (400,300)

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
    if( (step_size<1) or (step_size>10)):
        outStr = "Error: Step Size is incorrect. Please enter step size between 1 and 10"
        print("#"*len(outStr))
        print("\n"+outStr+"\n")
        print("#"*len(outStr))
        print("\n")
        return False

    

    move = MovePoint(startPoint,endPoint,theta,arenaSize)  
    flag = False
    while(not flag):
        flag = move.pointProcessor(step_size)
    
    end = time.time()
    finalOut = f"\nPath found in {round(end - start, 4)} seconds.\n"
    print(finalOut)
    
    backTraceArr = move.backTrace(startPoint)
    
    #-------------------------------------------------------------------------------#
    
    f_map = np.zeros(shape = (arenaSize[1],arenaSize[0],3))
    
    # Plot the map
    for i in range(arenaSize[0]):
        for j in range(arenaSize[1]):
            if not obstacleOrNot([i,j]):
                f_map[j][i] = [255,255,0]
                
    # Initialise the plotting figure            
    fig,px = plt.subplots(1,1)
    plt.xlim(0, 400)
    plt.ylim(0, 300)
    # Q = px.quiver(np.array(backTraceArr[0][0]),np.array(backTraceArr[0][1]),np.array(3),np.array(-1),units='xy' ,scale=1)
    px.imshow(f_map.astype('uint8'), animated=True)
    for i in backTraceArr:
        px.quiver(np.array(i[0]),np.array(i[1]),np.cos(i[2]),np.sin(i[2]),units='xy' , color='r')
    
    # im = plt.imshow(f_map.astype('uint8'), animated=True)
    # ani = animation.FuncAnimation(fig,animate, interval=0)
    plt.show()
    
    #-------------------------------------------------------------------------------#
    
    # pygame.init()

    # pygame.display.set_caption("Path Planner")

    # white = (255,255,255)
    # black = (0,0,0)
    
    # yellow = (255,255,0)
    # red = (255,0,0)
    # green = (0,255,0)
    # blue = (0,0,255,10)


    # gameDisplay = pygame.display.set_mode((400,300))
    # gameDisplay.fill(white)
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

    # clock = pygame.time.Clock()
    
    # while True:
    #     pygame.event.get()
        
    #     pygame.draw.circle(gameDisplay, black, to_pygame(endPoint),2)
    #     for key in move.visited.keys():
    #         pygame.draw.circle(gameDisplay, blue, to_pygame(key),1)
    #         clock.tick(10000000)
    #         pygame.display.update()

    #     for point in backTraceArr:
    #         pygame.draw.circle(gameDisplay, yellow, to_pygame(point),10,1)
    #         clock.tick(150)
    #         pygame.display.update()

        
        
        
    #     time.sleep(3)
    #     pygame.quit()
        
        
        # xpts = []
        # ypts = []
        # for x in range(arenaSize[0]):
        #         for y in range(arenaSize[1]):
        #             if not (obstacleOrNot((x,y))):
        #                 xpts.append(x)
        #                 ypts.append(y)
        # plt.scatter(xpts,ypts,s=0.1)
        # plt.show()
        # quit()
    
    

   
    
    

if __name__ == '__main__':
    main()

