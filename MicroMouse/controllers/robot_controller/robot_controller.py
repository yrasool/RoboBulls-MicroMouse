import sys
import math
from controller import Robot, Camera, CameraRecognitionObject, InertialUnit, DistanceSensor, PositionSensor
from MazeCellWall import *

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
#######################################################
# Assumptions
#######################################################
starting_cell = 240

# 0 = East, 90 = North, 180 = West, 270 = South 
starting_theta = 90

# Robot Deminsions in mm
wheel_radius = 20.32
axel_length = 57.912

#######################################################
# Creates World Map of the current Maze Default size 16
#######################################################
world_map = maze()

robot_pose = robotPose(starting_cell, starting_theta)         

#######################################################
# General driving forward a distance of D function.
# will update the pose of the robot based on D, and the
# current heading of the robot.
#######################################################  
# TODO: add PID to avoid side walls           
def driveD(robot,D):
    
    start_position = abs(leftposition_sensor.getValue())
    
    # Calculates velocity of each motor and the robot
    phi = 5                 # rad/sec
    vl  = 5 * wheel_radius  # mm/sec left motor
    vr  = 5 * wheel_radius  # mm/sec right motor
    v   = (vl+vr)/2         # mm/sec robot

    # Calculates Time need to move a distance D
    T   = D/v               # sec

    # Sets motor speeds and sets start time
    t_start=robot.getTime()
    leftMotor.setVelocity(phi)
    rightMotor.setVelocity(phi)

    headings = []
    while robot.step(timestep) != -1:
        # print(imu_cleaner(imu.getRollPitchYaw()[2]))
        headings.append(imu_cleaner(imu.getRollPitchYaw()[2]))
        if (robot.getTime() - t_start) >= T:
            leftMotor.setVelocity(0)
            rightMotor.setVelocity(0)
            break

    D = wheel_radius*(abs(leftposition_sensor.getValue())-start_position)
    
    if robot_pose.theta == 0 :
        theta = 0
    else:
        theta = sum(headings)/len(headings)
    new_x = robot_pose.x + (D*math.cos(math.radians(theta)))
    new_y = robot_pose.y + (D*math.sin(math.radians(theta)))
    robot_pose.set_xy(new_x,new_y)
    print(theta)
    robot_pose.set_theta(theta)
   
#######################################################
# General function to rotate the robot by degree,
# will also update the pose of the robot after the
# roation
#######################################################    
# TODO: empliment PID control to center on needed heading    
def rotate(robot,degree):
    
    # Determines Rotation and sets proper speeds
    if degree < 0 :
        sign = -1
    else:
        sign = 1
    X_rad = math.radians(degree)
    phi = sign*2
    
    # Calculates time need for rotation
    omega = 2*abs(phi)*wheel_radius / axel_length
    T = abs(X_rad / omega)
    # end_heading = (predicted_pose[3] - degree)%360

    t_start = robot.getTime()
    leftMotor.setVelocity(phi)
    rightMotor.setVelocity(-phi)
    
    starting_theta = round(imu_cleaner(imu.getRollPitchYaw()[2]))
    end_heading = round((starting_theta - degree)%360,2)

    while robot.step(timestep) != -1:
        current_heading = imu_cleaner(imu.getRollPitchYaw()[2])
        if (robot.getTime() - t_start) >= T:
            
            if end_heading <= 1 or end_heading >= 359:

                if current_heading > (end_heading+.05) and current_heading < (359-.05):
                    leftMotor.setVelocity(.01)
                    rightMotor.setVelocity(-.01)
                elif current_heading > (359+.05):
                    leftMotor.setVelocity(-.01)
                    rightMotor.setVelocity(.01)
                else:
                    leftMotor.setVelocity(0)
                    rightMotor.setVelocity(0)
                    break
            else:
                if current_heading > (end_heading+.05):
                    leftMotor.setVelocity(.01)
                    rightMotor.setVelocity(-.01)
                elif current_heading < (end_heading-.05):
                    leftMotor.setVelocity(-.01)
                    rightMotor.setVelocity(.01)
                else:
                    leftMotor.setVelocity(0)
                    rightMotor.setVelocity(0)
                    break
        else: 
            pass


    t_start = robot.getTime()
    headings=[]       
    while robot.step(timestep) != -1:
        headings.append(imu_cleaner(imu.getRollPitchYaw()[2]))
        if (robot.getTime() - t_start) >= 1.5:
            leftMotor.setVelocity(0)
            rightMotor.setVelocity(0)
            break
    
    # theta = angle_to_heading(sum(headings)/len(headings))
    if robot_pose.theta == 0 :
        theta = 0
    else:
        theta = sum(headings)/len(headings)
    # print(theta)
    robot_pose.set_theta(theta) 
    robot_pose.set_xy(robot_pose.x,robot_pose.y)

# Cleans the IMU readings so that the are in degrees and in the
# range of [0,359]
def imu_cleaner(imu_reading):
    rad_out = imu_reading
    if rad_out < 0:
        rad_out = rad_out + 2*math.pi
    return math.degrees(rad_out)

    
#######################################################
# Creates Robot
#######################################################
robot = Robot()


#######################################################
# Sets the time step of the current world
#######################################################
timestep = int(robot.getBasicTimeStep())

#######################################################
# Gets Robots Distance Sensors
#######################################################
frontDistanceSensor = robot.getDevice('front distance sensor')
leftDistanceSensor = robot.getDevice('left distance sensor')
rightDistanceSensor = robot.getDevice('right distance sensor')
rearDistanceSensor = robot.getDevice('rear distance sensor')
frontDistanceSensor.enable(timestep)
leftDistanceSensor.enable(timestep)
rightDistanceSensor.enable(timestep)
rearDistanceSensor.enable(timestep)

#######################################################
# Gets Robots Camera
#######################################################
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
      
# Main loop:
while robot.step(timestep) != -1:
    #Gets Distance Sensor readings
    fd = frontDistanceSensor.getValue()
    rd = rightDistanceSensor.getValue()
    bd = rearDistanceSensor.getValue()
    ld = leftDistanceSensor.getValue()
    theta = imu_cleaner(imu.getRollPitchYaw()[2])
    heading = angle_to_heading(theta) 
    sensor_readings = [fd,rd,bd,ld]
    # Gets Distance Sensor readings
    print("########################################################################")
    print("Front Distance Sensor : ",fd)
    print("Right Distance Sensor : ",rd)
    print("Right Distance Sensor : ",rd)
    print("Left Distance Sensor  : ",ld)
    print("Heading : ",heading)
    print("########################################################################")
    print("Predicted Pose:")
    robot_pose.printPose()         
    print("########################################################################")
    
    # Gets the index of the the cell in regards to world map maze  
    r,c = get_rc_from_index(robot_pose.cell_index)
    
    # Maps current wall config
    world_map.set_cell_walls(r,c,sensor_readings,heading)
    robot_pose.add_visited(world_map.maze[r][c])

    # print("Discovered: ", world_map.maze[r][c].discovered)
    
    # Flag used to determin if there is an adjacent cell that is undiscoverd and not
    #   blocked by wall. If there is move into that cell.
    has_next_cell = False
    # TODO: fix to also check if next cell is discovered
    for w in world_map.maze[r][c].walls:
        if not w.valid and not world_map.is_adjacent_cell_discovered(r,c,w.direction):
            possible_heading = w.direction
            has_next_cell = True
            if (turnNeeded(heading,possible_heading) != 0):
                rotate(robot,turnNeeded(heading,possible_heading))
                driveD(robot, 180)
            else:
                driveD(robot, 180)
            print("Possible heading: " + str(possible_heading))
            print("Turn Needed: "+ str(turnNeeded(heading,possible_heading)))
            break
        
    # This is if there are no adjacent undiscoved cells that are unblocked
    #   just navigate untill the robot finds an undiscoved cell, WILL GET STUCK
    # TODO: add path planning to get to closest undiscovered cell through discovered cell
    if not has_next_cell:
        print("Back Tracking")
        needed_rotation = robot_pose.rotation_needed_to_last_cell(heading)
        print(needed_rotation)        
        if (needed_rotation != 0):
            rotate(robot,needed_rotation)
            driveD(robot, 180)
        else:
            driveD(robot, 180)
        robot_pose.moved_to_last_cell()

    
    # Checks to see if all the cells have been discoved and mapped     
    if world_map.is_fully_discovered():
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break
        
sys.exit()
    
