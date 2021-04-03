import pygame
import time
import math
import numpy as np
from matplotlib import pyplot as plt

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
    
    # l1 = y - 0.7*x - 74.4
    l1 = y - 0.7*x - 56.09
    # l2 = y + 1.43*x - 176.64
    l2 = y + 1.43*x - 140.19
    # l3 = y - 0.7*x - 98.8
    l3 = y - 0.7*x - 117.11
    # l4 = y + 1.43*x - 438.37
    l4 = y + 1.43*x - 474.82
    
    if (x<0) or (x>400) or (y<0) or (y>300):
        return False
    
    #circle
    elif((x-90)**2 + (y-70)**2 - 50**2 < 0): #circle
        return False
    
    # tilted Rectangle
    # elif((8604*x - 12287*y + 914004 < 0) and (81900*x +59350*y-25510527 < 0) and (86036*x - 122870*y + 12140167 > 0) and (8192*x + 5735*y - 1012596 > 0)):
    #     return False
    
    
    elif l1>0 and l2>0 and l3<0 and l4<0:
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

    def __init__(self, node, goalPoint, step_size):
        """
        Initialize a A_Star object corresponding to a
        start point.
        Input: node(tuple)
        Return:
        """

        self.goalPoint = goalPoint
        self.step_size = step_size

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
        cost incase the current cost is greater than new 
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
        #print(self.cost[key_of_minimum_cost],key_of_minimum_cost)
        self.cost.pop(key_of_minimum_cost)
        self.queue.remove(key_of_minimum_cost)
        
        return key_of_minimum_cost


class MovePoint:
    """
    Class that is used to do decide point moving opeartion
    and processing which includes generating possible moves for the
    point.
    """

    def __init__(self, startPoint, goalPoint, step_size, size):
        """
        Initialize the MovePoint object corresponding to a
        start point, goal point, size of arena and the algorithm 
        to use.
        
        Input: startPoint(tuple), endPoint(tuple),
        size(tuple), algo(str)
        Return: None
        """
        self.goalPoint = goalPoint
        self.step_size = step_size

        self.queue = A_Star(startPoint,goalPoint,step_size)

        self.size = size
        self.visited = {startPoint:0}

        self.theta = {startPoint:0} 

    def nodeOperation(self, node, theta):
        """
        Generate the next node based on the operation and
        the node
        Input: node/point(tuple), moveCost(float),
        *args(list), **kwargs(dict)
        Return: True/False(Bool)
        """
        
        newNode = False
        step_size = self.step_size

        if(obstacleOrNot(node)):
            new_theta = self.theta[node] + theta
            newNode = (int(np.ceil(node[0]+(step_size*math.cos(new_theta)))), int(np.ceil(node[1]+(step_size*math.sin(new_theta)))))
            #print(newNode)

        
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

        #print(node)

        if(queue.euclideanDistance(node)<1.5):
            return True
        degrees = [-60,-30,0,30,60]
        #degrees = [-180,-90,0,90,180]

        operationParams = [math.radians(theta) for theta in degrees]

        # print("#######"+str(node))
        for theta in operationParams:
            self.nodeOperation(node, theta)
        # print("#######")
        return False 
        
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
    startPoint = (x1,y1)
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

    

    move = MovePoint(startPoint,endPoint,step_size,arenaSize)  
    flag = False
    while(not flag):
        flag = move.pointProcessor()
    
    end = time.time()
    finalOut = f"\nPath found in {round(end - start, 4)} seconds.\n"
    print(finalOut)
    

if __name__ == '__main__':
    # xpts = []
    # ypts = []
    # for x in range(500):
    #         for y in range(400):
    #             if not (obstacleOrNot((x,y))):
    #                 xpts.append(x)
    #                 ypts.append(y)
    # plt.scatter(xpts,ypts,s=0.1)
    # plt.show()
    main()