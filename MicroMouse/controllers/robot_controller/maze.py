import sys
import math



#Cell wall configuration North, East, South, West
cell_1  = [1,0,1,1]
cell_2  = [1,0,1,0]
cell_3  = [1,1,0,0]
cell_4  = [1,1,0,1]
cell_5  = [1,0,0,1]
cell_6  = [1,1,0,0]
cell_7  = [0,0,0,1]
cell_8  = [0,1,0,0]
cell_9  = [0,1,0,1]
cell_10 = [0,0,1,1]
cell_11 = [0,1,1,0]
cell_12 = [0,1,0,1]
cell_13 = [0,0,1,1]
cell_14 = [1,0,1,0]
cell_15 = [1,0,1,0]
cell_16 = [0,1,1,0]

#Actual wall configuration, depending this can be used for verification
# or the actual navigation of the robot
maze = [[cell_1,cell_2,cell_3,cell_4],
        [cell_5,cell_6,cell_7,cell_8],
        [cell_9,cell_10,cell_11,cell_12],
        [cell_13,cell_14,cell_15,cell_16]]
     
#Wall Config initialized to unknown for each cell [North, East, South, West]
cellp_1  = ["?","?","?","?"]
cellp_2  = ["?","?","?","?"]
cellp_3  = ["?","?","?","?"]
cellp_4  = ["?","?","?","?"]
cellp_5  = ["?","?","?","?"]
cellp_6  = ["?","?","?","?"]
cellp_7  = ["?","?","?","?"]
cellp_8  = ["?","?","?","?"]
cellp_9  = ["?","?","?","?"]
cellp_10 = ["?","?","?","?"]
cellp_11 = ["?","?","?","?"]
cellp_12 = ["?","?","?","?"]
cellp_13 = ["?","?","?","?"]
cellp_14 = ["?","?","?","?"]
cellp_15 = ["?","?","?","?"]
cellp_16 = ["?","?","?","?"]

#Initilizes a wall configuration map to all unknown
wall_maze = [[cellp_1,cellp_2,cellp_3,cellp_4],
             [cellp_5,cellp_6,cellp_7,cellp_8],
             [cellp_9,cellp_10,cellp_11,cellp_12],
             [cellp_13,cellp_14,cellp_15,cellp_16]]
    
#Map of the wave front planner
wave_map = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

#Global array to hold the cell numbers checked by a recursive funtion                            
checked_cells = []

# Creates wall maze data structure
def set_wall_maze(size=16):


#Getters for Global Varables
def get_wall_maze():
    return wall_maze
    
def get_maze():
    return maze

def getMaze():
    return maze    

#This sets up a Wave front Planner map with a goal in cell goal_cell
def path_planner(goal_cell,time):
    if time == 1:
        i,j,k = mazeIndex("North",goal_cell)
        wave_map[i][j] = 1
        recursive_wave(goal_cell)
    else:
        global checked_cells
        checked_cells = []
        recursive_wave2(goal_cell)
    return wave_map
    
            
#Generates the Wave front Planner map when it is first called
# this will not return the optimal solution
def recursive_wave(cell):
    
    checked_cells.append(cell)
    possible_cells = get_possible_cells(cell)
    i,j,k = mazeIndex("North",cell)
    value = wave_map[i][j]
    for next_cell in possible_cells:
        #print("From :", cell, "T0 :", next_cell, "Value : ", value)
        i,j,k = mazeIndex("North",next_cell)
        if value + 1 < wave_map[i][j] or wave_map[i][j]==0:
            wave_map[i][j] = value + 1
        if next_cell not in checked_cells:
            
            recursive_wave(next_cell)

#Optimizes the solution produced by recursive_wave(cell), this will
# chage the values if the is a shorter path to a specific cell
def recursive_wave2(cell):
    checked_cells.append(cell)
    possible_cells = get_possible_cells(cell)
    i,j,k = mazeIndex("North",cell)
    value = wave_map[i][j]
    for next_cell in possible_cells:
        #print("From :", cell, "T0 :", next_cell, "Value : ", value)
        ni,nj,k = mazeIndex("North",next_cell)
        if value + 1 < wave_map[ni][nj]:
            wave_map[ni][nj] = value + 1
        if next_cell not in checked_cells:
            
            recursive_wave2(next_cell)           

#Given the converged wave_map, this will find the optimal
# path from the starting point to the goal
def path_finder(starting_cell, goal_cell):
    path = []
    path.append(starting_cell)
    possible_cells = get_possible_cells(starting_cell)
    found_goal = False
    while not found_goal:
        min = 100
        best_cell = 0
        for next_cell in possible_cells:
            i,j = mapIndex(next_cell)
            if wave_map[i][j] < min :
                min = wave_map[i][j]
                best_cell = next_cell
        path.append(best_cell)
        if best_cell == goal_cell:
            found_goal = True
        else:
            possible_cells = get_possible_cells(best_cell)
    return path
    

#Checks the wall configuration of the map and sees what cells can be
# traveled to from the input cell (i.e. no wall)
# TODO: Fix to match MicroMouse Mazes   
def get_possible_cells(cell):

    i,j,k = mazeIndex("North",cell)
    
    prev_cell_index = [i,j]
    possible = []
    possible_headings = []
    possible_cells = []
        
    for wall_index in range(len(maze[i][j])):
        if maze[i][j][wall_index] == 0 :
            possible.append(wall_index)
    
    for possible_index in possible :
        if possible_index == 0:
            possible_headings.append("North")
            possible_cells.append(cell - 4)
        elif possible_index == 1:
            possible_headings.append("East")
            possible_cells.append(cell + 1)
        elif possible_index == 2:
            possible_headings.append("South")
            possible_cells.append(cell + 4)
        elif possible_index == 3:
            possible_headings.append("West")
            possible_cells.append(cell - 1)
            
    return possible_cells

#printf function that mirrors C
def printf(format, *args):
    sys.stdout.write(format % args)

def print_map(map):
    for i in range(4):
        printf("|%i,%i,%i,%i|\n",map[i][0],map[i][1],map[i][2],map[i][3])
        
#Given the cell, heading, and sensor readings, predicts the wall configuration
# updates globale wall_maze 
def map_cell_walls(cell,heading,readings):
    i,j,k = mazeIndex(heading,cell)
    li,fi,ri,bi = wall_mapping(heading)
    #left wall
    if readings[0] < 9 :
        wall_maze[i][j][li] = 1
    else :
        wall_maze[i][j][li] = 0
        
    #front wall
    if readings[1] < 9 :
        wall_maze[i][j][fi] = 1
    else :
        wall_maze[i][j][fi] = 0
    
    #right wall
    if readings[2] < 9 :
        wall_maze[i][j][ri] = 1
    else :
        wall_maze[i][j][ri] = 0
        
    #rear wall
    if readings[3] < 9 :
        wall_maze[i][j][bi] = 1
    else :
        wall_maze[i][j][bi] = 0
    
#Given the robot heading this returns the mapping of relative direction (left, front,..)
# to their obsolute indexing (North, East, ...)
def wall_mapping(heading):
    if heading == "North":
        left_wall_index = 3
        front_wall_index = 0
        right_wall_index = 1
        rear_wall_index =2
    elif heading == "East":
        left_wall_index = 0
        front_wall_index = 1
        right_wall_index = 2
        rear_wall_index = 3
    elif heading == "South":
        left_wall_index = 1
        front_wall_index = 2
        right_wall_index = 3
        rear_wall_index = 0
    elif heading == "West":
        left_wall_index = 2
        front_wall_index = 3
        right_wall_index = 0
        rear_wall_index = 1
        
    return left_wall_index, front_wall_index, right_wall_index, rear_wall_index

#Given the heading and cell of the robot, returns the index of the cell and wall robot
# is facing

# TODO: Fix to match MicroMouse Mazes    
def mazeIndex(heading,cell):

    if heading == "North":
        k = 0
    elif heading == "East":
        k = 1
    elif heading == "South":
        k = 2
    elif heading == "West":
        k = 3
    
    if cell == 1:
        i = 0
        j = 0
    elif cell == 2:
        i = 0
        j = 1
    elif cell == 3:
        i = 0
        j = 2
    elif cell == 4:
        i = 0
        j = 3
    elif cell == 5:
        i = 1
        j = 0
    elif cell == 6:
        i = 1
        j = 1
    elif cell == 7:
        i = 1
        j = 2
    elif cell == 8:
        i = 1
        j = 3
    elif cell == 9:
        i = 2
        j = 0
    elif cell == 10:
        i = 2
        j = 1
    elif cell == 11:
        i = 2
        j = 2
    elif cell == 12:
        i = 2
        j = 3
    elif cell == 13:
        i = 3
        j = 0
    elif cell == 14:
        i = 3
        j = 1
    elif cell == 15:
        i = 3
        j = 2
    elif cell == 16:
        i = 3
        j = 3
        
    return i,j,k
    
#Given Cell returns map index   
# TODO: Fix to match MicroMouse Mazes     
def mapIndex(cell):
    if cell == 1:
        i = 0
        j = 0
    elif cell == 2:
        i = 0
        j = 1
    elif cell == 3:
        i = 0
        j = 2
    elif cell == 4:
        i = 0
        j = 3
    elif cell == 5:
        i = 1
        j = 0
    elif cell == 6:
        i = 1
        j = 1
    elif cell == 7:
        i = 1
        j = 2
    elif cell == 8:
        i = 1
        j = 3
    elif cell == 9:
        i = 2
        j = 0
    elif cell == 10:
        i = 2
        j = 1
    elif cell == 11:
        i = 2
        j = 2
    elif cell == 12:
        i = 2
        j = 3
    elif cell == 13:
        i = 3
        j = 0
    elif cell == 14:
        i = 3
        j = 1
    elif cell == 15:
        i = 3
        j = 2
    elif cell == 16:
        i = 3
        j = 3
    return i,j
    
#Given current robot heading and possible_heading, calculates the change in
# roation needed to face the new heading 
def turnNeeded(heading, possible_heading):
    
    if heading == "North":
        if possible_heading == "North":
            rotate = 0 
        elif possible_heading == "East":
            rotate = 90
        elif possible_heading == "South":
            rotate = 180
        elif possible_heading == "West":
            rotate = -90
    
    elif heading == "East":
        if possible_heading == "North":
            rotate = -90 
        elif possible_heading == "East":
            rotate = 0
        elif possible_heading == "South":
            rotate = 90
        elif possible_heading == "West":
            rotate = 180
            
    elif heading == "South":
        if possible_heading == "North":
            rotate = 180 
        elif possible_heading == "East":
            rotate = -90
        elif possible_heading == "South":
            rotate = 0
        elif possible_heading == "West":
            rotate = 90
    
    elif heading == "West":
        if possible_heading == "North":
            rotate = 90 
        elif possible_heading == "East":
            rotate = 180
        elif possible_heading == "South":
            rotate = -90
        elif possible_heading == "West":
            rotate = 0
    
    return rotate
    

#Given cell returns the golbal frame cordinates
# TODO: Fix to match MicroMouse Mazes       
def cell_to_cord(cell_number):
    if cell_number == 1:
        cord = [-15,15]
    elif cell_number == 2 :
        cord=[-5,15]
    elif cell_number == 3 :
        cord=[5,15]
    elif cell_number == 4 :
        cord=[15,15]
    elif cell_number == 5 :
        cord=[-15,5]
    elif cell_number == 6 :
        cord=[-5,5]
    elif cell_number == 7 :
        cord=[5,5]
    elif cell_number == 8 :
        cord=[15,5]
    elif cell_number == 9 :
        cord=[-15,-5]
    elif cell_number == 10 :
        cord=[-5,-5]
    elif cell_number == 11 :
        cord=[5,-5]
    elif cell_number == 12 :
        cord=[15,-5]
    elif cell_number == 13 :
        cord=[-15,-15]
    elif cell_number == 14 :
        cord=[-5,-15]
    elif cell_number == 15 :
        cord=[5,-15]
    elif cell_number == 16 :
        cord=[15,-15]
    return cord

       