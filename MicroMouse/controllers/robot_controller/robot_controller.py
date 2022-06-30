"""lab2_task1 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import sys
import math
import matplotlib.pyplot as plt


#######################################################
# TA's use you can change the Kp value and set Plots
# to true if you want to generate the plots
#######################################################
Kp = 4
Plots = False


# Used for making the plots for the report
def plotMaker(fd,ld,rd,y):
              
    f = plt.figure()
    plt.plot(y, fd, c='b', label='Front')
    plt.plot(y, ld, c='r', label='Left')
    plt.plot(y, rd, c='g', label='Right')
    plt.title("Task 1: Plots of Time verses Wall Distances")
    plt.legend(loc='upper right')
    plt.xlabel("Time in seconds")
    plt.ylabel("Distance in Inches")
    
    
    f.savefig("Plot_for_distance"+str(Kp)+".pdf", bbox_inches='tight', pad_inches=0.1)

#######################################################
# Sets up varables used in the code
#######################################################
def printf(format, *args):
    sys.stdout.write(format % args)
    

#######################################################
# Converts IMU readings into degrees
#######################################################    
def imu_cleaner(imu_reading):
    rad_out = imu_reading
    if rad_out < 0:
        rad_out = rad_out + 2*math.pi
    return math.degrees(rad_out)

#######################################################
# Saturation function used for PID Control
#######################################################
def satFunc(velocity, phiMax, phiMin):
    velocity = float(velocity)
    if (velocity > phiMax):
        velocity = phiMax
    elif (velocity < phiMin):
        velocity = phiMin
    return velocity
    
#######################################################
# Converts meters to Inches
#######################################################
def meterToinch(value):
    return value*39.37

#######################################################
# Front PID control, takes the current reading from
# front sensor and also the distance we wish to be at
# calculates what the velocity should be to get to the
# desited distance
#######################################################    
def frontPID(distanceFront):

    e = distanceFront - 10
    e = Kp*e
    velocity = e
    phi = velocity/.8
    
    return phi

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


#initialization of motors
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

#distance sensors 
frontDistanceSensor = robot.getDevice('front distance sensor')
leftDistanceSensor = robot.getDevice('left distance sensor')
rightDistanceSensor = robot.getDevice('right distance sensor')
frontDistanceSensor.enable(timestep)
leftDistanceSensor.enable(timestep)
rightDistanceSensor.enable(timestep)



imu = robot.getDevice('inertial unit')
imu.enable(timestep)

# Getting the Max and Min velocity of robot
phiMaxLeft = leftMotor.getMaxVelocity() 
phiMaxRight = rightMotor.getMaxVelocity()

phiMax = min(phiMaxLeft, phiMaxRight)

phiMin = -1*phiMax

t_start = robot.getTime()

front = []
left = []
right = []
time = []
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    

    # Read the sensors
    ld = meterToinch(leftDistanceSensor.getValue())
    rd = meterToinch(rightDistanceSensor.getValue())
    fd = meterToinch(frontDistanceSensor.getValue())
    # Records the data points
    front.append(fd)
    left.append(ld)
    right.append(rd)
    time.append(robot.getTime() - t_start)
    
    # Calculates speed needed using PID control
    # velocity = satFunc(frontPID(fd), phiMax, phiMin)
    
    # If the robot gets to close to a side wall this adds
    # angular velocity to stear away from the wall
    # if(ld < 2.7):
        # leftPhi = satFunc(velocity +  .05*velocity,phiMax, phiMin)
        # rightPhi = satFunc(velocity - .05*velocity,phiMax, phiMin)
    # elif(rd < 2.7):
         # leftPhi = satFunc(velocity - .05*velocity,phiMax, phiMin)
         # rightPhi = satFunc(velocity + .05*velocity,phiMax, phiMin)
    # else:
        # leftPhi = satFunc(velocity,phiMax, phiMin)
        # rightPhi = satFunc(velocity,phiMax, phiMin)
    
    # Stopping conditions, runs for 30 sec and the front wall is
    # 10 inches away +-.1 inches    
    # if((robot.getTime() - t_start) > 30):
    
        # if(9.9 <= fd <= 10.1):
                # leftMotor.setVelocity(0)
                # rightMotor.setVelocity(0)   
                # break
    
    # Process sensor data here.
    printf("Left Distance %f \n",leftDistanceSensor.getValue())
    printf("Right Distance %f \n",rightDistanceSensor.getValue())
    printf("Front Distance %f \n",frontDistanceSensor.getValue())
    printf("Current Heading %f \n", imu_cleaner(imu.getRollPitchYaw()[2]))
    leftMotor.setVelocity(2)
    rightMotor.setVelocity(2)
    
    
    
    pass
    


# Enter here exit cleanup code.
if Plots:
    plotMaker(front,left,right,time)