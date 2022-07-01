import numpy as np
import math

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

        
class cell:
    def __init__(self, index=0, wall_code='Unknown', size = 16):
        
        self.index = index
        self.wall_code = wall_code
        self.wall_config = wall_dict[wall_code]
        
        # Sets the row and column index relative to a size x size maze (default 16x16)
        self.cell_row, self.cell_col = divmod(index,size)
        
        # Sets the row and column index relative of adjacent cells
        # used to check next cell status
        self.cell_to_north_row = self.cell_row - 1
        self.cell_to_north_col = self.cell_col
        self.cell_to_south_row = self.cell_row + 1
        self.cell_to_south_col = self.cell_col
        self.cell_to_east_row = self.cell_row
        self.cell_to_east_col = self.cell_col + 1
        self.cell_to_west_row = self.cell_row
        self.cell_to_west_col = self.cell_col - 1
        
        # Sets the (x,y) center of the cell relative the the maze (in mm)
        self.center_x = ((90) + (self.cell_col*180))
        self.center_y = (((180*size) - 90) - (self.cell_row*180))
        
        # Creates a list of wall object
        # TODO : fix so that no walls are dealt with
        self.walls = []
        for wall_indexer in range(4):
            self.walls.append(wall(self.index, self.center_x, self.center_y, wall_indexer, self.wall_config[wall_indexer]))

class maze:
    # Construction of a Maze Object. Wall configuration can be known or unknown 
    def __init__(self, cell_codes=np.full(256, 'Unknown'), size = 16):
        self.maze = np.full((size, size), cell())
        indexer = 0
        for cell_code in cell_codes:
            r,c = divmod(indexer,size)
            cell_and_walls = cell(index=indexer,wall_code=cell_code)
            self.maze[r][c] = cell_and_walls
            indexer+=1
    
    # Updates cell and wall configuration in the Maze (default assumes robot is facing North if not provided)
    def set_cell_walls(cell_r,cell_c,sensor_readings,heading='North'):
        # Gets original indexer
        indexer = get_index_from_rc(cell_r,cell_c)
        # Gets wall config
        wall_config = sensor_readings_to_wall_config(sr=sensor_readings,heading=heading)
        wall_code = list(wall_dict.keys())[list(wall_dict.values()).index(wall_config)]
        # Creates new cell object and updates the maze
        cell_and_walls = cell(index=indexer,wall_code=cell_code)
        self.maze[r][c] = cell_and_walls
        return 0
    
    # Takes a cell's row and column index and returns original indexer
    def get_index_from_rc(cell_r,cell_c,size=16):
        return (size*cell_r) + cell_c
    
    # Takes a cell's index and returns row and column index
    def get_rc_from_index(index,size=16):
        return divmod(index,size)
    
    # Takes a cell's index and returns x & y cordinate in mm 
    def get_xy_from_index(index,size=16):
        cell_r,cell_c = get_rc_from_index(index,size)
        return cget_xy_from_rc(cell_r,cell_c,size)
    
    # Takes a cell's row and column index and returns x & y cordinate in mm 
    def get_xy_from_rc(cell_r,cell_c,size=16):
        center_x = ((90) + (c*180))
        center_y = (((180*size) - 90) - (r*180))
        return center_x,center_y
    
    # Takes the robot sensor readings and heading and converts it to a wall configuration (default assumes robot heading is North)
    def sensor_readings_to_wall_config(sr,heading='North'):
        wall_config = wall_dict['Legend']
        for i in range(len(sr)):
            if heading == 'North':
                if sr[i] <= .05:
                    wall_config[i] = 1
                else:
                    wall_config[i] = 0
            elif heading == 'East':
                if sr[i] <= .05:
                    wall_config[(i+1)%4] = 1
                else:
                    wall_config[(i+1)%4] = 0
            elif heading == 'South':
                if sr[i] <= .05:
                    wall_config[(i+2)%4] = 1
                else:
                    wall_config[(i+2)%4] = 0
            elif heading == 'West':
                if sr[i] <= .05:
                    wall_config[(i+3)%4] = 1
                else:
                    wall_config[(i+3)%4] = 0
        