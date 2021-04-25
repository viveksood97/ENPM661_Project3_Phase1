import time
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.animation as animation


def obstacleOrNot(point, radius = 22, clearance = 5):
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
    elif((x-200)**2 + (y-200)**2 - (100 + clearance + radius)**2 < 0): #circle
        return False
    
    # circle2
    elif((x-200)**2 + (y-800)**2 - (100 + clearance + radius)**2 < 0): #circle
        return False
    
    # Square
    elif(((x - 25 + clearance + radius > 0) and (x - 175 - clearance - radius < 0)) and ((y - 425 + clearance + radius > 0) and (y - 575 - clearance - radius < 0))):
        return False
    
    # Horizontal Rectangle
    elif(((x - 375 + clearance + radius > 0) and (x - 625 - clearance - radius < 0)) and ((y - 425 + clearance + radius > 0) and (y - 575 - clearance - radius < 0))):
        return False
    
    # Vertical Rectangle
    elif(((x - 725 + clearance + radius > 0) and (x - 875 - clearance - radius < 0)) and ((y - 200 + clearance + radius > 0) and (y - 400 - clearance - radius < 0))):
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

    def __init__(self, startPoint, goalPoint, size, theta, actions):
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
        self.actions = actions


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
            t += dt
            temp = 0.5*r * (action[0] + action[1]) * dt
            cos = math.cos(Thetan)
            sin = math.sin(Thetan)
            Delta_Xn = cos * temp
            Delta_Yn = sin * temp
            Xn += Delta_Xn
            Yn += Delta_Yn
            Thetan += (r / L) * (action[1] - action[0]) * dt
            if not obstacleOrNot((Xn,Yn)):
                return node, Thetai, 0
            D += math.sqrt(math.pow(Delta_Xn,2)+math.pow(Delta_Yn,2))
        
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
            newNode, new_theta, new_step_size = self.cost(node, theta, action)
                
        
        if(newNode and newNode not in self.visited and obstacleOrNot(newNode)):
            self.queue.step_size = new_step_size
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
                self.theta[goalPoint] = self.theta[node]
            return True


        operationParams = self.actions

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
        backTraceArr.append(goalPoint)
        while(node != startPoint):
            # print(child_parent_relation)
            # print(node)
            node = child_parent_relation[node][0]
            backTraceArr.append(node)
        return backTraceArr, child_parent_relation, self.theta

    
def plot_curve(node, Thetai, action, f_map, color):
    
        t = 0
        r = 3.8
        L = 35.4
        dt = 0.1
        Xn= node[0]
        Yn= node[1]
        
        Thetan = Thetai

        D=0
        while t<1:
            t = t + dt
            Delta_Xn = int(0.5*r * (action[0] + action[1]) * math.cos(Thetan) * dt)
            Delta_Yn = int(0.5*r * (action[0] + action[1]) * math.sin(Thetan) * dt)
            Xn += Delta_Xn
            Yn += Delta_Yn
            if obstacleOrNot((Xn,Yn)):
                f_map = cv2.line(f_map,(Xn,Yn),(Xn + Delta_Xn,Yn + Delta_Yn),color, thickness = 2)
            Thetan += (r / L) * (action[1] - action[0]) * dt
        
        return f_map


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
    
    rpm1 = int(input("Enter RPM1: "))
    rpm2 = int(input("Enter RPM2: "))
    
    actions = [[0, rpm1],[rpm1, 0],[rpm1, rpm1],[0, rpm2],[rpm2, 0],[rpm2, rpm2],[rpm1, rpm2],[rpm2, rpm1]]
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

    

    

    move = MovePoint(startPoint,endPoint,arenaSize,theta,actions)  
    flag = False
    while(not flag):
        flag = move.pointProcessor()
    
    backTraceArr, child_parent_rel, theta = move.backTrace(startPoint)
    end = time.time()
    finalOut = f"\nPath found in {round(end - start, 4)} seconds.\n"
    print(finalOut)
    
    f_map = np.zeros(shape = (1000,1000,3))
    for i in range(1000):
        for j in range(1000):
            if not obstacleOrNot([i,j],radius=0,clearance = 0):
                f_map[j][i] = [0,102,51]
            elif not obstacleOrNot([i,j],radius = 0):
                f_map[j][i] = [255,255,0]
            elif not obstacleOrNot([i,j]):
                f_map[j][i] = [0,0,255]
            else:
                f_map[j][i] = [255,255,255]
    
    fig = plt.figure()
    im = plt.imshow(f_map.astype('uint8'), origin='lower', animated=True)
    ims = []
    # actions = [[15,15],[15,0],[0,15],[15,20],[20,15],[20,20],[0,20],[20,0]]
    
    backTraceArr = backTraceArr[::-1]
    # print(backTraceArr)
    
    res = 0
    for key in move.visited.keys():
        if res%200 != 0 :
            res = res + 1
            for action in actions:
                f_map = plot_curve(key,theta[key],action,f_map,(128,128,128))
        else:
            res = res + 1
            im = plt.imshow(f_map.astype('uint8'),origin='lower')
            ims.append([im])
            
    
    for i in range(len(backTraceArr)):
        for action in actions:
            f_map = plot_curve(backTraceArr[i],theta[backTraceArr[i]],action,f_map,(255,0,00))

        im = plt.imshow(f_map.astype('uint8'),origin='lower')
        ims.append([im])
    
    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=False)
    # ani.save('animation.mp4')
    plt.show()

if __name__ == '__main__':
    main()