import numpy as np
import math
from queue import PriorityQueue

"""
Maze shape and index referance Top -> North & Right -> East
Each Cell is 180mm x 180mm

(0mm, 2880mm)                                     (2880mm, 2880m) 
ˇ                                                               ˇ
[  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15]
[ 16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31]
[ 32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47]
[ 48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63]
[ 64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79]        N
[ 80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95]        ˆ
[ 96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111]        |
[112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127]   W ‹--•--› E
[128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143]        |
[144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159]        ˇ
[160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175]        S
[176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191]
[192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207]
[208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223]
[224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239]
[240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255]
^                                                               ^
(0mm, 0mm)                                           (2880mm, 0m)

"""

# Dictionary of wall codes and wall configurations (DO NOT CHANGE)
wall_dict = {
            "Legend": ['N','E','S','W'],
            "Unknown": ['?','?','?','?'],
            0 : [0,0,0,0],
            1 : [1,0,0,0],
            2 : [0,1,0,0],
            4 : [0,0,1,0],
            8 : [0,0,0,1],
            3 : [1,1,0,0],
            5 : [1,0,1,0],
            9 : [1,0,0,1],
            6 : [0,1,1,0],
            10 : [0,1,0,1],
            12 : [0,0,1,1],
            7 : [1,1,1,0],
            11 : [1,1,0,1],
            13 : [1,0,1,1],
            14 : [0,1,1,1],
            15 : [1,1,1,1],
        }

#########################################################################################
# Function: Angle To Heading
#   INPUT:  theta   (in degrees)
#   OUTPUT: heading [North, East, South, West]            
#########################################################################################
def angle_to_heading(theta):
    heading = 0
    sd = 25
    if (90 - sd) <= theta <= (90+sd):
        heading = 'North'
    elif (180-sd) <= theta <= (180 +sd):
        heading = 'West'
    elif (270-sd) <= theta <= (270+sd):
        heading = 'South'
    elif theta >= (360-sd) or theta <= (0+sd):
        heading = 'East'
        
    return heading

#########################################################################################
# Function: Turn Needed
#   INPUT:  heading         [North, East, South, West] 
#           next_heading    [North, East, South, West] 
#   OUTPUT: theta           (degrees need to go from heading to next_heading)            
#########################################################################################
def turnNeeded(heading, next_heading):
    
    if heading == "North":
        if next_heading == "North":
            theta = 0 
        elif next_heading == "East":
            theta = 90
        elif next_heading == "South":
            theta = 180
        elif next_heading == "West":
            theta = -90
    
    elif heading == "East":
        if next_heading == "North":
            theta = -90 
        elif next_heading == "East":
            theta = 0
        elif next_heading == "South":
            theta = 90
        elif next_heading == "West":
            theta = 180
            
    elif heading == "South":
        if next_heading == "North":
            theta = 180 
        elif next_heading == "East":
            theta = -90
        elif next_heading == "South":
            theta = 0
        elif next_heading == "West":
            theta = 90
    
    elif heading == "West":
        if next_heading == "North":
            theta = 90 
        elif next_heading == "East":
            theta = 180
        elif next_heading == "South":
            theta = -90
        elif next_heading == "West":
            theta = 0
    
    return theta

#########################################################################################
# Function: Get Index From Row & Column
#   INPUT:  cell_r   (current cell's row index) 
#           cell_c   (current cell's col index) 
#           size     (deminisions of maze default 16)
#   OUTPUT: index    (index of cell in the world map maze)            
#########################################################################################
def get_index_from_rc(cell_r,cell_c,size=16):
    return (size*cell_r) + cell_c

#########################################################################################
# Function: Get Index From x & y
#   INPUT:  x       (robot's current x cordinate mm) 
#           y       (robot's current y cordinate mm) 
#           size    (deminisions of maze default 16)
#   OUTPUT: index   (index of cell in the world map maze)            
#########################################################################################
def get_index_from_xy(x,y):
    cell_c = math.floor(x/180)
    cell_r = math.floor((2880-y)/180)
    return get_index_from_rc(cell_r,cell_c)

#########################################################################################
# Function: Get Row & Column From Index 
#   INPUT:  index   (index of cell in the world map maze)  
#           size    (deminisions of maze default 16)
#   OUTPUT: cell_r  (current cell's row index) 
#           cell_c  (current cell's col index)             
#########################################################################################
def get_rc_from_index(index,size=16):
    return divmod(index,size)

#########################################################################################
# Function: Get x & y From Index
#   INPUT:  index   (index of cell in the world map maze)            
#           size    (deminisions of maze default 16)
#   OUTPUT: x       (robot's current x cordinate mm) 
#           y       (robot's current y cordinate mm) 
#########################################################################################
def get_xy_from_index(index,size=16):
    cell_r,cell_c = get_rc_from_index(index,size)
    return get_xy_from_rc(cell_r,cell_c,size)

#########################################################################################
# Function: Get x & y From Row & Column
#   INPUT:  cell_r (current cell's row index) 
#           cell_c (current cell's col index)            
#           size    (deminisions of maze default 16)
#   OUTPUT: x       (robot's current x cordinate mm) 
#           y       (robot's current y cordinate mm) 
#########################################################################################
# Takes a cell's row and column index and returns x & y cordinate in mm 
def get_xy_from_rc(cell_r,cell_c,size=16):
    center_x = ((90) + (cell_c*180))
    center_y = (((180*size) - 90) - (cell_r*180))
    return center_x,center_y

#########################################################################################
# Function: Sensor Readings to Wall Configuration
#   INPUT:  sr          [front_ds, right_ds, rear_ds, left_ds] 
#           heading     [North, East, South, West] 
#   OUTPUT: wall_config [North_s, East_s, South_s, West_s] where *_s is 1 if wall  0 if no
#                        wall in direction *         
#########################################################################################
def sensor_readings_to_wall_config(sr,heading='North'):
    wall_config = wall_dict['Legend']
    for i in range(len(sr)):
        if heading == 'North':
            if sr[i] <= .09:
                wall_config[i] = 1
            else:
                wall_config[i] = 0
        elif heading == 'East':
            if sr[i] <= .09:
                wall_config[(i+1)%4] = 1
            else:
                wall_config[(i+1)%4] = 0
        elif heading == 'South':
            if sr[i] <= .09:
                wall_config[(i+2)%4] = 1
            else:
                wall_config[(i+2)%4] = 0
        elif heading == 'West':
            if sr[i] <= .09:
                wall_config[(i+3)%4] = 1
            else:
                wall_config[(i+3)%4] = 0
    return wall_config

#########################################################################################
# Class:    Wall
#   ATRB:   translation_x (x cordinate of wall mm)
#           translation_y (y cordinate of wall mm)
#           translation_z (z cordinate of wall mm)
#           valid         [True, False] if there is a wall
#           direction     [North, East, South, West] relative to cell            
#########################################################################################
class wall:
    # TODO: create a non-exsistant wall
    def __init__(self, cell_index, cell_center_x, cell_center_y, wall_index, wall_valid):
        self.translation_x = cell_center_x
        self.translation_y = cell_center_y
        self.translation_z = 25
        if wall_valid == 1:
            self.valid = True
        else:
            self.valid = False
        if wall_index == 0:
            self.direction = 'North'
            self.translation_y += 90
        elif wall_index == 1:
            self.direction = 'East'
            self.translation_x += 90
        elif wall_index == 2:
            self.direction = 'South'
            self.translation_y -= 90
        elif wall_index == 3:
            self.direction = 'West'
            self.translation_x -= 90

        
#########################################################################################
# Class:    Cell
#   ATRB:   index               world map maze index
#           wall_code           integer code used to get wall config from dictionary
#           wall_config         [North_s, East_s, South_s, West_s] where *_s is 1 if wall  
#                               0 if no wall in direction *
#           discovered          [True, False] is cell has been discovered
#           cell_row            world map row index 
#           cell_col            world map col index
#           cell_to_north_row   world map row index for cell to the north
#           cell_to_north_col   world map col index for cell to the north
#           cell_to_north_index world map index for cell to the north
#           cell_to_east_row    world map row index for cell to the east
#           cell_to_east_col    world map col index for cell to the east
#           cell_to_east_index  world map index for cell to the east
#           cell_to_south_row   world map row index for cell to the south
#           cell_to_south_col   world map col index for cell to the south
#           cell_to_south_index world map index for cell to the south
#           cell_to_west_row    world map row index for cell to the west
#           cell_to_west_col    world map col index for cell to the west
#           cell_to_west_index  world map index for cell to the west
#           walls               List of wall objects one for each direction          
#########################################################################################
class cell:
    def __init__(self, cell_index = 0, wall_code = 'Unknown', discovered = False, size = 16, distance_to_goal = -1):
        
        self.cell_index = cell_index
        self.wall_code = wall_code
        self.wall_config = wall_dict[wall_code]
        self.discovered = discovered
        self.distance_to_goal = distance_to_goal
        
        # Sets the row and column index relative to a size x size maze (default 16x16)
        self.cell_row, self.cell_col = divmod(cell_index,size)
        
        # Sets the row and column index relative of adjacent cells
        
        # Cell to the North
        self.cell_to_north_row   = self.cell_row - 1 if self.cell_row - 1 >= 0 else 0
        self.cell_to_north_col   = self.cell_col
        self.cell_index_to_north = get_index_from_rc(self.cell_to_north_row,self.cell_to_north_col)
        
        # Cell to the South
        self.cell_to_south_row = self.cell_row + 1 if self.cell_row + 1 <= 15 else 15
        self.cell_to_south_col = self.cell_col
        self.cell_index_to_south = get_index_from_rc(self.cell_to_south_row,self.cell_to_south_col)

        # Cell to the East
        self.cell_to_east_row = self.cell_row
        self.cell_to_east_col = self.cell_col + 1 if self.cell_col + 1 <= 15 else 15
        self.cell_index_to_east = get_index_from_rc(self.cell_to_east_row,self.cell_to_east_col)

        # Cell to the West
        self.cell_to_west_row = self.cell_row
        self.cell_to_west_col = self.cell_col - 1 if self.cell_col - 1 >= 0 else 0
        self.cell_index_to_west = get_index_from_rc(self.cell_to_west_row,self.cell_to_west_col)
        
        # Sets the (x,y) center of the cell relative the the maze (in mm)
        self.center_x = ((90) + (self.cell_col*180))
        self.center_y = (((180*size) - 90) - (self.cell_row*180))
        
        # Creates a list of wall object ordered North, East, South, West
        self.walls = []
        for wall_indexer in range(4):
            w = wall(self.cell_index, self.center_x, self.center_y, wall_indexer, self.wall_config[wall_indexer])
            self.walls.append(w)
  
    ##############################################################################################
    # Class Function: Get Adjacent Cell
    #   INPUT:  direction [North, East, South, West] 
    #  
    #   OUTPUT: cell_to_*_row  world map row index for cell to the * in [North, East, South, West]
    #           cell_to_*_col  world map col index for cell to the * in [North, East, South, West]          
    ##############################################################################################
    def get_adjacent_cell(self,direction):
        if direction == "North":
            return self.cell_to_north_row, self.cell_to_north_col
    
        elif direction == "East":
            return self.cell_to_east_row, self.cell_to_east_col
                
        elif direction == "South":
            return self.cell_to_south_row, self.cell_to_south_col
        
        elif direction == "West":
            return self.cell_to_west_row, self.cell_to_west_col

    ##############################################################################################
    # Class Function: Get Direction to Next Cell
    #   INPUT:  direction [North, East, South, West] 
    #  
    #   OUTPUT: cell_to_*_row  world map row index for cell to the * in [North, East, South, West]
    #           cell_to_*_col  world map col index for cell to the * in [North, East, South, West]          
    ##############################################################################################
    def get_direction_next_cell(self,next_cell):
        if self.cell_index_to_north == next_cell.cell_index:
            return 'North'
        elif self.cell_index_to_east == next_cell.cell_index:
            return 'East'
        elif self.cell_index_to_south == next_cell.cell_index:
            return 'South'
        elif self.cell_index_to_west == next_cell.cell_index:
            return 'West'

    ##############################################################################################
    # Class Function: Is Cell Adjacent and Unblocked
    #   INPUT:  next_cell 
    #  
    #   OUTPUT: [True, False] if two cells are adjacent and there is no wall between them          
    ##############################################################################################
    def is_adjacent_cell_and_unblocked(self,next_cell):
        
        # Check to see if the next cell is adjacent to the current cell
        adjacent = False
        direction_index = None
        if self.cell_index_to_north == next_cell.cell_index:
            adjacent = True
            direction_index = 0
        elif self.cell_index_to_east == next_cell.cell_index:
            adjacent = True
            direction_index = 1
        elif self.cell_index_to_south == next_cell.cell_index:
            adjacent = True
            direction_index = 2
        elif self.cell_index_to_west == next_cell.cell_index:
            adjacent = True
            direction_index = 3

        # Checks to see if there is a wall between the two adjacent cells
        if adjacent:
            unblocked = self.walls[direction_index].valid
        return adjacent and unblocked
        

#########################################################################################
# Class:    Maze
#   ATRB:   maze                Size x Size np.array of cell objects (Size default is 16)
#           fully_discovered    [True, False] is the all cell in the maze discovered
#########################################################################################
class maze:
    # Construction of a Maze Object. Wall configuration can be known or unknown 
    def __init__(self, cell_codes=np.full(256, 'Unknown'), size = 16, goal_index = 119, start_index = 240):
        self.maze = np.full((size, size), cell())
        self.fully_discovered = False
        self.goal_index = goal_index
        self.goal_row, self.goal_col = get_rc_from_index(self.goal_index)
        indexer = 0
        for cell_code in cell_codes:
            r,c = divmod(indexer,size)
            
            cell_and_walls = cell(cell_index=indexer,wall_code=cell_code,distance_to_goal=self.distance_to_goal(r,c))
            self.maze[r][c] = cell_and_walls
            indexer+=1
    
    ##############################################################################################
    # Class Function: Get Adjacent Cell
    #   INPUT:  cell_r          world map row index 
    #           cell_col        world map col index          
    #           sensor_readings [front_ds, right_ds, rear_ds, left_ds]
    #           heading         [North, East, South, West] 
    #  
    #   OUTPUT: None
    #   ACTION: updates the cell stored at cell_r, cell_c with a discovered cell with walls         
    ##############################################################################################
    def set_cell_walls(self,cell_r,cell_c,sensor_readings,heading='North'):
        # Gets original indexer
        indexer = get_index_from_rc(cell_r,cell_c)
        # Gets wall config
        wall_config = sensor_readings_to_wall_config(sr=sensor_readings,heading=heading)
        print(wall_config)
        wall_code = list(wall_dict.keys())[list(wall_dict.values()).index(wall_config)]
        # Creates new cell object and updates the maze
        cell_and_walls = cell(cell_index=indexer,wall_code=wall_code,discovered=True)
        self.maze[cell_r][cell_c] = cell_and_walls
    
    ##############################################################################################
    # Class Function: Is Adjacent Cell Discovered
    #   INPUT:  cell_r        world map row index 
    #           cell_c        world map col index  
    #           direction     [North, East, South, West]
    #   OUTPUT: [True, False] if the next cell is discovered         
    ##############################################################################################
    def is_adjacent_cell_discovered(self, cell_r, cell_c,direction):
        next_r, next_c = self.maze[cell_r][cell_c].get_adjacent_cell(direction)
        return self.maze[next_r][next_c].discovered

    ##############################################################################################
    # Class Function: Gets Perfered Order of Next Cell
    #   INPUT:  cell_r        world map row index 
    #           cell_c        world map col index  
    #           direction     [North, East, South, West]
    #   OUTPUT: [cell 1-4 ]   sorted list of cells based on distance to goal         
    ##############################################################################################
    def get_prefered_next_cells(self, cell_r, cell_c):
        next_cells = []
        has_next = False

        for w in self.maze[cell_r][cell_c].walls:
            if not w.valid and not self.is_adjacent_cell_discovered(cell_r,cell_c,w.direction):
                next_r, next_c = self.maze[cell_r][cell_c].get_adjacent_cell(w.direction)
                next_cells.append(self.maze[next_r][next_c])
                has_next = True
        if has_next:
            return sorted(next_cells, key=lambda x: x.distance_to_goal)
        else:

            return None

    ##############################################################################################
    # Class Function: Gets Neighbor Cell
    #   INPUT:  cell_r        world map row index 
    #           cell_c        world map col index  
    #           direction     [North, East, South, West]
    #   OUTPUT: [cell 1-4 ]   list of cells neighboring current cell with out a blocking wall        
    ##############################################################################################
    def get_neighbor_cells(self, cell_r, cell_c):
        next_cells = []
        has_next = False

        for w in self.maze[cell_r][cell_c].walls:
            if not w.valid :
                next_r, next_c = self.maze[cell_r][cell_c].get_adjacent_cell(w.direction)
                next_cells.append(self.maze[next_r][next_c])
                has_next = True
        if has_next:
            return sorted(next_cells, key=lambda x: x.distance_to_goal)
        else:

            return None

    ##############################################################################################
    # Class Function: Is Maze Fully Discovered
    #   INPUT:  self (maze object) 
    #  
    #   OUTPUT: [True, False] if the world map is fully discovered         
    ##############################################################################################
    # Updates fully discovered flag
    def is_fully_discovered(self):
        self.fully_discovered = True
        for maze_row in self.maze:
            for maze_cell in maze_row:
                if not maze_cell.discovered:
                    self.fully_discovered = False
        return self.fully_discovered
        

    ##############################################################################################
    # Class Function: Is Goal Cell Discovered
    #   INPUT:  self (maze object)
    #           goal_index (index of the cell we want to see if is discovered) 
    #  
    #   OUTPUT: [True, False] if the goal cell is fully discovered         
    ##############################################################################################
    # Updates fully discovered flag
    def is_goal_discovered(self, goal_cell= -1):
        if goal_cell ==-1:
            return self.maze[self.goal_row][self.goal_col].discovered
        else:
            r,c = get_rc_from_index(goal_cell)
            return self.maze[r][c].discovered

    ##############################################################################################
    # Class Function: Distance to Cell
    #   INPUT:  self        (maze object)
    #           current_r   world map row index of current cell
    #           current_c   world map col index of current cell
    #           goal_r      world map row index of goal cell
    #           goal_c      world map col index of goal cell
    #  
    #   OUTPUT: int of distance to goal cell in number of cells assume 4-way conntection     
    ##############################################################################################
    # Updates fully discovered flag
    def distance_to_goal(self, current_r,current_c, goal_r = -1, goal_c =- 1):
        if goal_r ==-1 and goal_c == -1:
            return  abs(current_r - self.goal_row) + abs(current_c-self.goal_col)
        else:
            return abs(current_r - goal_r) + abs(current_c-goal_c)   

    ##############################################################################################
    # Class Function: Get Undiscovered Cells Sorted
    #   INPUT:  self        (maze object)
    #           current_r   world map row index of current cell
    #           current_c   world map col index of current cell
    #  
    #   OUTPUT: a sorted list of undiscovered cells based on distance to current cell and goal    
    ##############################################################################################
    # Updates fully discovered flag
    def get_sorted_undiscovered(self, current_r,current_c):
        undiscovered_cells = []
        has_undiscovered =False
        for maze_row in self.maze:
            for maze_cell in maze_row:
                if not maze_cell.discovered:
                    undiscovered_cells.append(maze_cell)
                    has_undiscovered = True

        return sorted(undiscovered_cells, key=lambda x: (self.distance_to_goal(x.cell_row,x.cell_col,current_r,current_c),x.distance_to_goal))

#########################################################################################
# Class:    robotPose
#   ATRB:   index   world map maze index
#           cell_r  world map row index 
#           cell_c  world map col index
#           x       (robot's current x cordinate mm) 
#           y       (robot's current y cordinate mm)
#           theta   robots's current IMU reading [0,359] degrees
#           heading [North, East, South, West]         
#########################################################################################  
class robotPose:
    def __init__(self,cell_index, theta):
        self.cell_index             = cell_index
        self.cell_r, self.cell_c    = get_rc_from_index(self.cell_index)
        self.x, self.y              = get_xy_from_rc(self.cell_r, self.cell_c)
        self.theta                  = theta
        self.heading                = angle_to_heading(theta)
        self.visited                = []
    
    ##############################################################################################
    # Class Function: Set  X Y
    #   INPUT:  self        (robot_pose object)
    #           x       (robot's current x cordinate mm) 
    #           y       (robot's current y cordinate mm)
    #   OUTPUT: None
    #   ACTION: updates the robot's beliefe of x, y, cell_r, cell_c, and cell_index        
    ##############################################################################################
    def set_xy(self,x,y):
        self.x = x
        self.y = y
        self.cell_index = get_index_from_xy(self.x,self.y)
        self.cell_r, self.cell_c    = get_rc_from_index(self.cell_index)
    
    ##############################################################################################
    # Class Function: Set  Cell Index
    #   INPUT:  self        (robot_pose object)
    #           cell_index   world map maze index
    #   OUTPUT: None
    #   ACTION: updates the robot's beliefe of x, y, cell_r, cell_c, and cell_index        
    ##############################################################################################
    def set_cell_index(self, cell_index):
        self.cell_index = cell_index
        self.cell_r, self.cell_c    = get_rc_from_index(self.cell_index)
        self.x, self.y              = get_xy_from_rc(self.cell_r, self.cell_y)
    ##############################################################################################
    # Class Function: Set Theta
    #   INPUT:  self        (robot_pose object)
    #           theta   robots's current IMU reading [0,359] degrees
    #   OUTPUT: None
    #   ACTION: updates the robot's beliefe of theta and heading      
    ##############################################################################################
    def set_theta(self, theta):
        self.theta = theta
        self.heading                = angle_to_heading(theta)
    
    ##############################################################################################
    # Class Function: Print Pose
    #   INPUT:  self        (robot_pose object)
    #          
    #   OUTPUT: None
    #   ACTION: prints the robot pose based off of beliefs       
    ##############################################################################################
    def printPose(self):
        print("Robots Pose ")
        print(" \t Current Cell:   \t" + str(self.cell_r) +", " + str(self.cell_c))
        print(" \t Current x, y:   \t" + str(self.x) +", " + str(self.y))
        print(" \t Current theta:  \t" + str(self.theta))
        # print(" \t Current Heading:\t" + self.heading)
    
    ##############################################################################################
    # Class Function: Add Visitied 
    #   INPUT:  self        (robot_pose object)
    #           current_cell  cell object that the robot is currently occupying
    #   OUTPUT: None
    #   ACTION: updates the list of cells the robot has visited     
    ##############################################################################################
    def add_visited(self, current_cell):
        if len(self.visited) > 0:
            if current_cell.cell_index != self.visited[-1].cell_index:
                self.visited.append(current_cell)
        else:
            self.visited.append(current_cell)
    
    ##############################################################################################
    # Class Function: Rotation Needed To Go to Last Cell
    #   INPUT:  self        (robot_pose object)
    #           current_heading [North, East, South, West] 
    #  OUTPUT: the angle needed to rotate the robot to the last cell   
    ##############################################################################################
    def rotation_needed_to_last_cell(self,current_heading):
        current_cell = self.visited[-1]
        previous_cell = self.visited[-2]
        dx = previous_cell.cell_col - current_cell.cell_col
        dy = previous_cell.cell_row - current_cell.cell_row
        if dx != 0:
            if dx > 0:
                needed_heading = 'East'
            else:
                needed_heading = 'West'
        if dy != 0:
            if dy > 0:
                needed_heading = 'South'
            else:
                needed_heading = 'North'
        return turnNeeded(current_heading, needed_heading)

    ##############################################################################################
    # Class Function: Add Visitied 
    #   INPUT:  self        (robot_pose object)
    #           
    #   OUTPUT: None
    #   ACTION: updates the list of cells the robot has visited     
    ##############################################################################################
    def moved_to_last_cell(self):
        self.visited.pop()
        self.visited.pop()

    ##############################################################################################
    # Class Function: Print Visited
    #   INPUT:  self        (robot_pose object)
    #          
    #   OUTPUT: None
    #   ACTION: prints the cell index of all the cells visited by the robot      
    ##############################################################################################
    def print_visted(self):
        out_list = []
        for visted_cells in self.visited:
            out_list.append(visted_cells.cell_index)
        print(out_list)
    
    ##############################################################################################
    # Class Function: Cell List to Action List
    #   INPUT:  self        (robot_pose object)
    #           current_heading [North, East, South, West]
    #           path    a list of cells that need to be traversed
    #   OUTPUT: a list of rotations needed to travers the path      
    ##############################################################################################
    def cell_list_to_action_list(self,current_heading,path):
        action_list = []
        for i in range(len(path)-1):
            current_cell = path[i]
            previous_cell = path[i+1]
            dx = previous_cell.cell_col - current_cell.cell_col
            dy = previous_cell.cell_row - current_cell.cell_row
            if dx != 0:
                if dx > 0:
                    needed_heading = 'East'
                else:
                    needed_heading = 'West'
            if dy != 0:
                if dy > 0:
                    needed_heading = 'South'
                else:
                    needed_heading = 'North'
            action_list.append(turnNeeded(current_heading, needed_heading))
            current_heading = needed_heading
            
        return action_list

    ##############################################################################################
    # Class Function: A*
    #   INPUT:  self        (robot_pose object)
    #           world_map   Maze object
    #   OUTPUT: a list cells to be traversed     
    ##############################################################################################
    def astar(self,world_map):
        start_cell = world_map.maze[self.cell_r][self.cell_c]
        g_score = {}
        f_score = {} 
        for rows in world_map.maze:
            for cells in rows:
                g_score[cells]=float('inf')
                f_score[cells]=float('inf') 
        
        g_score[start_cell]=0
        f_score[start_cell]=start_cell.distance_to_goal

        open_cells=PriorityQueue()
        open_cells.put((start_cell.distance_to_goal,start_cell.distance_to_goal,(start_cell.cell_row,start_cell.cell_col)))
        aPath = {}
        while not open_cells.empty():
            r,c = open_cells.get()[2]
            current_cell = world_map.maze[r][c]
            if not current_cell.discovered:
                fwdPath=[current_cell]
                while current_cell.cell_index != start_cell.cell_index:
                    fwdPath.append(aPath[current_cell])
                    current_cell=aPath[current_cell]
                fwdPath.reverse()   
                return fwdPath

            
            neighbor_cell = world_map.get_neighbor_cells(current_cell.cell_row,current_cell.cell_col)

            for neighbor in neighbor_cell:

                temp_g_score = g_score[current_cell]+1
                temp_f_score = temp_g_score + neighbor.distance_to_goal

                if temp_f_score < f_score[neighbor]:
                    g_score[neighbor]= temp_g_score
                    f_score[neighbor]= temp_f_score
                    open_cells.put((temp_f_score,neighbor.distance_to_goal,(neighbor.cell_row,neighbor.cell_col)))
                    aPath[neighbor]=current_cell

        