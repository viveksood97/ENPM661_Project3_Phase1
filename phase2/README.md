# ENPM661 - Project3 Phase-2

#### Project3 Phase-2 for ENPM661: Planning for Autonomous Robots by:
#### Vivek Sood(UID:117504279) 
#### Rigved Rajesh Kulkarni(UID:117358124)
### Description

##### 1. This python script is used to find path between start point and goal point while avoiding defined obstacles.
##### 2. The algorithm that we have implemented for phase 1 is A* algorithm.
### Packages Used
```python
import pygame
import time
import math
from matplotlib import pyplot as plt
```
##### Note: Apart from pygame everything else is an inbuilt package
### Usage
##### To run the program
```bash
python3 version1.py
```
##### This will generate a prompt.

```bash
pygame 2.0.1 (SDL 2.0.14, Python 3.6.10)
Hello from the pygame community. https://www.pygame.org/contribute.html
 
   ____        __  __       ____  __                           
   / __ \____ _/ /_/ /_     / __ \/ /___ _____  ____  ___  _____
  / /_/ / __ `/ __/ __ \   / /_/ / / __ `/ __ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /_/ / / /  / ____/ / /_/ / / / / / / /  __/ /    
/_/    \__,_/\__/_/ /_/  /_/   /_/\__,_/_/ /_/_/ /_/\___/_/     
                                                                


Enter the x coordinate of the start point: 0
Enter the y coordinate of the start point: 0
Enter the x coordinate of the goal point: 400
Enter the y coordinate of the goal point: 300
Enter the step size for movement between 1 and 10: 10

```
##### Enter start and goal positions and the code will find a path and start the animation depicting the path.
