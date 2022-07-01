import sys
import math
from controller import Robot, Camera, CameraRecognitionObject, InertialUnit, DistanceSensor, PositionSensor
from MazeCellWall import *

########################
# TA's Use
########################
starting_cell = 16

# 0 = East, 90 = North, 180 = West, 270 = South 
starting_heading = 90

#Mapping of the cell numbers
map = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

#Map of the discovered cells
discovered = [["?","?","?","?"],["?","?","?","?"],["?","?","?","?"],["?","?","?","?"]]


#Takes in an average IMU readings and forces it to be a 
# cardinal direction
def angleMM(theta):
    belief_theta = 0
    sd = 25
    if (90 - sd) <= theta <= (90+sd):
        belief_theta = 90
    elif (180-sd) <= theta <= (180 +sd):
        belief_theta = 180
    elif (270-sd) <= theta <= (270+sd):
        belief_theta = 270
    elif theta >= (360-sd) or theta <= (0+sd):
        belief_theta = 0
        
    return belief_theta
         

#######################################################
# General driving forward a distance of D function.
# will update the pose of the robot based on D, and the
# current heading of the robot.
#######################################################  
            
def driveD(robot,D):
    t_start=robot.getTime()
    
    start_position = abs(leftposition_sensor.getValue())
    leftMotor.setVelocity(5)
    rightMotor.setVelocity(5)
    headings = []
    
    while robot.step(timestep) != -1:
        headings.append(imu_cleaner(imu.getRollPitchYaw()[2]))
        if (robot.getTime() - t_start) >= 2.5:
            leftMotor.setVelocity(0)
            rightMotor.setVelocity(0)
            break
    
    D = .8*(abs(leftposition_sensor.getValue())-start_position)
    if predicted_pose[3] == 0 :
        theta = 0
    else:
        theta = math.radians(angleMM(sum(headings)/len(headings)))
    
    predicted_pose[0] = predicted_pose[0] + (D*math.cos(theta))
    predicted_pose[1] = predicted_pose[1] + (D*math.sin(theta))
    predicted_pose[2] = cellPredict(predicted_pose[0],predicted_pose[1])
    predicted_pose[3] = math.degrees(theta)
   
#######################################################
# General function to rotate the robot by degree,
# will also update the pose of the robot after the
# roation
#######################################################    
    
def rotate(robot,degree):
    
    if degree < 0 :
        sign = -1
    else:
        sign = 1
    X_rad = math.radians(degree)
    phi = sign*1
    
    omega = 2*.8 /2.28
    T = abs(X_rad / omega)
    end_heading = (predicted_pose[3] - degree)%360

    t_start = robot.getTime()
    leftMotor.setVelocity(phi)
    rightMotor.setVelocity(-phi)
      
    while robot.step(timestep) != -1:
         current_heading = imu_cleaner(imu.getRollPitchYaw()[2])
         if (robot.getTime() - t_start) >= T:
            leftMotor.setVelocity(0)
            rightMotor.setVelocity(0)
            break
    
    t_start = robot.getTime()
    headings=[]       
    while robot.step(timestep) != -1:
         headings.append(imu_cleaner(imu.getRollPitchYaw()[2]))
         if (robot.getTime() - t_start) >= 1.5:
            leftMotor.setVelocity(0)
            rightMotor.setVelocity(0)
            break
    
    theta = angleMM(sum(headings)/len(headings))

    if end_heading == 0:
        predicted_pose[3] = 0
    else:
        predicted_pose[3] = theta 
        

#######################################################
# Converts meters to Inches
#######################################################
def meterToinch(value):
    return value*39.37
    
#Cleans the IMU readings so that the are in degrees and in the
# range of [0,359]
def imu_cleaner(imu_reading):
    rad_out = imu_reading
    if rad_out < 0:
        rad_out = rad_out + 2*math.pi
    return math.degrees(rad_out)

#Given the global fram cordinates x and y this will
# return the cell number
def cellPredict(x,y):
    if -20 <= x < -10:
        i = 0
    elif -10 <= x < 0:
        i = 1
    elif 0 <= x < 10:
        i = 2
    elif 10 <= x < 20:
        i = 3
    if 10 <= y < 20:
        j = 0
    elif 0 <= y < 10:
        j = 1
    elif -10 <= y < 0:
        j = 2
    elif -20 <= y < -10:
        j = 3
        
    return map[j][i]
    
#This is called to update the discovered map and print it as well
def mapping(cell):
    i,j = mapIndex(cell)
       
    discovered[i][j] = "V"
    for r in range(4):
        print("|", discovered[r][0], " ", discovered[r][1], " ", discovered[r][2], " ", discovered[r][3], "|")


# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#enable distance sensors
frontDistanceSensor = robot.getDevice('front distance sensor')
leftDistanceSensor = robot.getDevice('left distance sensor')
rightDistanceSensor = robot.getDevice('right distance sensor')
# rearDistanceSensor = robot.getDevice('rear_ds')
frontDistanceSensor.enable(timestep)
leftDistanceSensor.enable(timestep)
rightDistanceSensor.enable(timestep)
# rearDistanceSensor.enable(timestep)

# enable camera and recognition
camera = robot.getDevice('camera1')
camera.enable(timestep)
camera.recognitionEnable(timestep)

#######################################################
# Gets Robots Motors
#######################################################

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)


#######################################################
# Gets Robot's the position sensors
#######################################################

leftposition_sensor = robot.getDevice('left wheel sensor')
rightposition_sensor = robot.getDevice('right wheel sensor')
leftposition_sensor.enable(timestep)
rightposition_sensor.enable(timestep)

imu = robot.getDevice('inertial unit')
imu.enable(timestep)

#Based on the starting cell this gets the global fram cordinates
# and sets the robot pose
# cord = cell_to_cord(starting_cell)
# predicted_pose =[cord[0],cord[1],starting_cell,starting_heading]
      
# Main loop:
while robot.step(timestep) != -1:
    #Gets Distance Sensor readings
    ld = leftDistanceSensor.getValue()
    fd = frontDistanceSensor.getValue()
    rd = rightDistanceSensor.getValue()
    # bd = meterToinch(rearDistanceSensor.getValue()) 
    print("Left Distance Sensor  : ",ld)
    print("Front Distance Sensor : ",fd)
    print("Right Distance Sensor : ",rd)
    
    # print("########################################################################")
    # print("Predicted Pose:",predicted_pose)         
    # print("########################################################################")
    # mapping(predicted_pose[2])
    
    # Sets the heading based of predicted pose after motion
    # current_heading = predicted_pose[3]
    # if 89 <= current_heading <= 91:
        # heading = "North"
        
    # elif 179 <= current_heading <= 181:
        # heading = "West"
        
    # elif 269 <= current_heading <= 271:
        # heading = "South"
        
    # elif current_heading >= 359 or current_heading <= 1:
        # heading = "East"
         
    # else :
        # heading = "NA"
        
    # #Gets Distance Sensor readings
    # ld = meterToinch(leftDistanceSensor.getValue())
    # fd = meterToinch(frontDistanceSensor.getValue())
    # rd = meterToinch(rightDistanceSensor.getValue())
    # bd = meterToinch(rearDistanceSensor.getValue()) 
    # print("Left Distance Sensor  : ",ld)
    # print("Front Distance Sensor : ",fd)
    # print("Right Distance Sensor : ",rd)
    # print("Rear Distance Sensor  : ",bd)
    
    # #Gets the index of the the cell in regards to the wall_mapping array  
    # i,j,k = mazeIndex(heading, predicted_pose[2])
    # #Gets the current wall_mapping
    # wall_mapping = get_wall_maze()
    # #Checks to see if the walls have been mapped for the cell the robot is in
    # for wall_index in range(4):
        # if wall_mapping[i][j][wall_index] == "?":
            # map_cell_walls(predicted_pose[2],heading,[ld,fd,rd,bd])
            # break
    # #Updates wall_mapping
    # wall_mapping = get_wall_maze()
    # print("Current cell wall readings (1 = wall, 0 = no wall):")
    # print("    North : ",wall_mapping[i][j][0])
    # print("    East  : ",wall_mapping[i][j][1])
    # print("    South : ",wall_mapping[i][j][2])
    # print("    West  : ",wall_mapping[i][j][3])
    # print("Complete Wall Configuration (N,E,S,W):")
    # for row in range(4):
            
        # printf("\t Cell %i \t %s \t Cell %i \t %s \t Cell %i \t %s \t Cell %i \t %s \n",(row*4)+1, wall_mapping[row][0],(row*4)+2, wall_mapping[row][1],(row*4)+3,wall_mapping[row][2],(row*4)+4,wall_mapping[row][3])
  
    
    # Gets the next cell index
    # if heading == "North":
        # ni = i -1
        # nj = j 
        # if ni < 0:
            # ni = i
    # elif heading == "East":
        # ni = i 
        # nj = j + 1
        # if nj > 3:
            # nj = j
    # elif heading == "South":
        # ni = i +1
        # nj = j 
        # if ni > 3:
            # ni = i
    # elif heading == "West":
        # ni = i
        # nj = j - 1 
        # if nj < 0:
            # nj = j
    
    # #If the next cell is undiscoved and not blocked by a wall, moves robot
    # into then next cell
    # if fd > 5 and discovered[ni][nj] == "?":
        # driveD(robot, 10)
        
    # #Else check all the adjasent cell to see which ones are undiscovered and
    # and not blocked by a wall
    # else:
        # prev_cell_index = [i,j]
        # possible = []
        # possible_headings = []
        # possible_cells = []
        
        
        # for wall_index in range(len(wall_mapping[i][j])):
            # if wall_mapping[i][j][wall_index] == 0 :
                # possible.append(wall_index)
        
        # for possible_index in possible :
            # if possible_index == 0:
                # possible_headings.append("North")
                # possible_cells.append(predicted_pose[2] - 4)
            # elif possible_index == 1:
                # possible_headings.append("East")
                # possible_cells.append(predicted_pose[2] + 1)
            # elif possible_index == 2:
                # possible_headings.append("South")
                # possible_cells.append(predicted_pose[2] + 4)
            # elif possible_index == 3:
                # possible_headings.append("West")
                # possible_cells.append(predicted_pose[2] - 1)

        # next_cell = 0
        # next_cell_index = 0
        # for possible_cell_index in range(len(possible_cells)):
            # pi,pj = mapIndex(possible_cells[possible_cell_index])
            # if discovered[pi][pj] == "?":
                # next_cell = possible_cells[possible_cell_index]
                # next_cell_index = possible_cell_index

        # if next_cell != 0:
            # #print("here")
            # degree = turnNeeded(heading, possible_headings[next_cell_index])     
            # rotate(robot,degree)
            # pi,pj = mapIndex(possible_cells[next_cell_index])
        
        # #This is if there are no adjacent undiscoved cells that are unblocked
        # #just navigate untill the robot finds an undiscoved cell, WONT GET STUCK
        # else:
            # if fd < 5 :
                # if ld > 5 :
                    # rotate(robot,-90)
                # elif rd > 5 :
                    # rotate(robot,90)
                # else :
                    # rotate(robot,180)
            # else :
                # driveD(robot,10)
    
    # #Checks to see if all the cells have been discoved and mapped     
    # done = True
    # for index_i in range(len(discovered)) :
        # for index_j in range(len(discovered[0])):
            # if discovered[index_i][index_j] == "?" :
                # done = False
    # #Stopes if all the cells have been discovered and mapped
    # if done :
        # leftMotor.setVelocity(0)
        # rightMotor.setVelocity(0)
        # break
        
sys.exit()
    
