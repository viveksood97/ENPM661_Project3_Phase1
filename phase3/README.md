# ENPM661 - Project3 Phase-3

#### Project3 Phase-3 for ENPM661: Planning for Autonomous Robots by:
#### Vivek Sood(UID:117504279) 
#### Rigved Rajesh Kulkarni(UID:117358124)

### Part 1: A* algorithm: Simulation in Matplotlib

##### 1. This python script is used to find path between start point and goal point while avoiding defined obstacles.
##### 2. The algorithm that we have implemented for phase 1 is A* algorithm.
### Packages Used
```python
import time
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.animation as animation
```
##### Note: Apart from pygame everything else is an inbuilt package
### Usage
##### To run the program
```bash
python3 version1.py
```
##### This will generate a prompt.

```bash
 
   ____        __  __       ____  __                           
   / __ \____ _/ /_/ /_     / __ \/ /___ _____  ____  ___  _____
  / /_/ / __ `/ __/ __ \   / /_/ / / __ `/ __ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /_/ / / /  / ____/ / /_/ / / / / / / /  __/ /    
/_/    \__,_/\__/_/ /_/  /_/   /_/\__,_/_/ /_/_/ /_/\___/_/     
                                                                


Enter the x coordinate of the start point: 100
Enter the y coordinate of the start point: 100
Enter the x coordinate of the goal point: 900
Enter the y coordinate of the goal point: 900
Enter the theta of the start point: 0
Enter RPM1: 15 # recommended value
Enter RPM2: 20 # recommended value

```
##### Enter start and goal positions and the code will find a path and start the animation depicting the path.

To save the video uncomment line 387: ani.save('animation.mp4') 


### Part 2: A* algorithm: Simulation in Gazebo using ros