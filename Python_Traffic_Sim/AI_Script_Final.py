#===========================================================================================
# Author: Ramesh Balachandran
# Script: AI Traffic
# Brief:  Working AI traffic script to simulate extreme traffic behavious in a scene
#===========================================================================================

import maya.cmds as cmds
import random
from math import sqrt

# Maya expression editor: add - python("update("+frame+")");

# preset velocities
velocity1 = (0,0,-1)
velocity1_1 = (0,0,-1.5)
velocity1_2 = (0,0,-0.5)
velocity2 = (0,0,1)
velocity2_1 = (0,0,1.5)
velocity3 = (0,0,-0.2)
velocity3_1 = (0,0,-0.1)
velocitySide = (1,0,0)
velocitySide2 = (-1,0,0)
velocityFar = (0,0,-2)
velocityFarBack = (0,0,2)

# juncList elements
# 0 = junction name
# 1 = junction type
#     ALL, FL, FR, LR, L, R, ILR, IL, IR --> from a 0 rotation perspective
#     ALL             - cars can go straight, turn left or turn right
#     L, R, IL, IR    - cars can only turn left or only turn right dependng on the direction at which it enters the junction
#     FL, FR, LR, ILR - cars can either only turn left or right, or only go straight or turn right, or go straight and turn left depending of direction at which the car enters the junction
juncList = [['junction0', 'ALL'], ['junction1', 'FR'], ['junction2', 'FR'], ['junction3', 'ALL'], ['junction4', 'FL'], ['junction5', 'L'], ['junction6', 'LR'], ['junction7', 'FL'], ['junction8', 'R'], ['junction9', 'ALL'], ['junction10', 'ALL'], ['junction11', 'LR'], ['junction12', 'IL'], ['junction13', 'ILR'], ['junction14', 'ILR'], ['junction15', 'IR']]

# carList elements:
# 0 = car name
# 1 = current state (modified by decision making and events)
# 2 = if currently in a junction (-1 if not in junction, else junction index car is at)
# 3 = count used for different functions to execute actions over time
# 4 = previous state to go back to (if needed)
carList = [['car1',3, -1, 0, 2], ['car2',2, -1, 0, 2], ['car3',2, -1, 0, 2], ['car4',2, -1, 0, 2], ['car5',2, -1, 0, 2], ['car6',2, -1, 0, 2], ['car7',2, -1, 0, 2], ['car8',2, -1, 0, 2], ['car9',2, -1, 0, 2], ['car10',2, -1, 0, 2], ['car11',2, -1, 0, 2], ['car12',2, -1, 0, 2], ['car13',2, -1, 0, 2], ['car14',2, -1, 0, 2], ['car15',2, -1, 0, 2], ['car16',2, -1, 0, 2], ['car17',2, -1, 0, 2], ['car18',2, -1, 0, 2], ['car19',2, -1, 0, 2], ['car20',2, -1, 0, 2], ['taxi1',2, -1, 0, 2], ['taxi2',2, -1, 0, 2]]

# List of all crash locations
crashList = []

# List of building sets
buildingList = ['buildingSet1', 'buildingSet2', 'buildingSet3', 'buildingSet4', 'buildingSet5', 'buildingSet6', 'buildingSet7', 'buildingSet8', 'buildingSet9']

# List of taxi stands
taxiStandList = ['taxiStand1', 'taxiStand2', 'taxiStand3', 'taxiStand4', 'taxiStand5', 'taxiStand6']


#========================================================================
# ACTION AND BEHAVIOUR FUNCTIONS
#========================================================================  
def turnLeft(car):
    """Rotates the car to the left.
    Used when turning at junction.
    State 0"""
    cmds.xform(car, t=velocity1, r=True, os=True)
    cmds.xform(car, ro=(0,10,0), r=True, os=True, p=True)

def turnRight(car):
    """Rotates the car to the right.
    Used when turning at junction.
    State 1"""
    cmds.xform(car, t=velocity3, r=True, os=True)
    cmds.xform(car, ro=(0,-10,0), r=True, os=True, p=True)
    
def goStraight(car):
    """Moves car forward.
    Used for all generic car movement.
    State 2"""
    cmds.xform(car, t=velocity1, r=True, os=True)
    
def goSlow(car):
    """Moves car forward at a slower speed.
    Used for slowing car movement.
    No state. Used in other states."""
    cmds.xform(car, t=velocity1_2, r=True, os=True)

def emergencyStop(carIndex):
    """Emergency stop function.
    Stops the car and adds a slight rotation showing hard application of brakes.
    State 3"""
    cmds.xform(carList[carIndex][0], ro=(-10,0,0), r=True, os=True, p=True)
    carList[carIndex][4] = carList[carIndex][1]
    carList[carIndex][1] = 3

def driveAround(carIndex):
    """Drive around / Overtake function.
    Moves the car to the right to 'overtake' or avoid the car in front of it.
    State 4"""
    cmds.xform(carList[carIndex][0], ro=(0,-14,0), r=True, os=True)
    carList[carIndex][1] = 4

def swerve(carIndex):
    """Swerve function.
    Moves the car back and forth on the local x axis to simulate swerving.
    State 5"""
    cmds.xform(carList[carIndex][0], ro=(0,-14,0), r=True, os=True)
    carList[carIndex][1] = 5
    
def recover(carIndex):
    """Recover from emergency stop function.
    Simulates the car accelerating to its initial speed after stopping.
    State 6"""
    cmds.xform(carList[carIndex][0], t=velocity3_1, r=True, os=True)
    carList[carIndex][1] = 6
    
def crash(carIndex):
    """Crash function.
    Stops the car where it is to show that it has crashed. Crashed cars cannot recover.
    State -1"""
    cmds.xform(carList[carIndex][0], ro=(0,0,0), r=True, os=True, p=True)
    carList[carIndex][1] = -1
    pos = cmds.xform(carList[carIndex][0], t=True, q=True)
    newCrash = cmds.spaceLocator(n='crash1')
    cmds.xform(newCrash, t=(pos[0],pos[1],pos[2]))
    crashList.append(newCrash)
    
def spinOut(carIndex):
    """Crash function.
    Stops the car where it is to show that it has crashed. Crashed cars cannot recover.
    State -2"""
    cmds.xform(carList[carIndex][0], ro=(0,10,0), r=True, os=True, p=True)
    carList[carIndex][1] = -2
    
def lostControl(carIndex):
    """Lost control function.
    Causes a car that didn't right itself after swerving to crash.
    State -3"""
    cmds.xform(carList[carIndex][0], t=(0,0,-1.2), r=True, os=True, p=True)
    cmds.xform(carList[carIndex][0], ro=(0,10,0), r=True, os=True, p=True)
    carList[carIndex][1] = -3
    pos = cmds.xform(carList[carIndex][0], t=True, q=True)
    newCrash = cmds.spaceLocator(n='crash1')
    cmds.xform(newCrash, t=(pos[0],pos[1],pos[2]))
    crashList.append(newCrash)
    
def panic(carIndex):
    """Panic function.
    Causes car to speed up and turn, resulting in eventual crash.
    State -4"""
    carList[carIndex][1] = -4
    
def skid(carIndex):
    """Moves car forward.
    Car is unable to react to other events in the scene.
    Will eventually crash.
    State -5"""
    cmds.xform(carList[carIndex][0], t=velocity1_1, r=True, os=True)
    carList[carIndex][1] = -5
    
def stopForPassengers(carIndex):
    """Moves the car close to the sidewalk.
    Used by taxis to simulate picking up passengers.
    State 99"""
    cmds.xform(carList[carIndex][0], ro=(0,-12,0), r=True, os=True)
    cmds.xform(carList[carIndex][0], t=velocity1, r=True, os=True)
    carList[carIndex][1] = 99

#========================================================================
# CALCULATION FUNCTIONS
#========================================================================  
def distanceBetween(obj1, obj2):
    """Calculates the distance between two objects."""   
    pos1 = cmds.xform(obj1, t=True, q=True)
    pos2 = cmds.xform(obj2, t=True, q=True)
    
    finalX = pos1[0] - pos2[0]
    finalY = pos1[1] - pos2[1]
    finalZ = pos1[2] - pos2[2]
    
    distance = sqrt((finalX*finalX) + (finalY*finalY) + (finalZ*finalZ))
    return distance
 
def detectCollision(car1, car2):
    """Checks bounding box of two cars.
    Returns True if collision between car bounding boxes is detected"""
    bbox1 = cmds.exactWorldBoundingBox(car1)
    bbox2 = cmds.exactWorldBoundingBox(car2)
    
    if (bbox2[2]>=bbox1[2] and bbox2[2]<=bbox1[5] or bbox2[5]>=bbox1[2] and bbox2[5]<=bbox1[5]) and (bbox2[0]>=bbox1[0] and bbox2[0]<=bbox1[3] or bbox2[3]>=bbox1[0] and bbox2[3]<=bbox1[3]):
        return True
    else:
        return False

def inJunction(car, juncIndex):
    """Checks bounding box of car and junction defining plane.
    Returns True if collision between car and junction is detected."""
    bbox1 = cmds.exactWorldBoundingBox(juncList[juncIndex][0])
    bbox2 = cmds.exactWorldBoundingBox(car)
    
    if (bbox2[2]>=bbox1[2] and bbox2[2]<=bbox1[5] or bbox2[5]>=bbox1[2] and bbox2[5]<=bbox1[5]) and (bbox2[0]>=bbox1[0] and bbox2[0]<=bbox1[3] or bbox2[3]>=bbox1[0] and bbox2[3]<=bbox1[3]):
        return True
        
def inWorld(car):
    """Checks if the car is still in the map.
    Returns True if it is still within the bounds of the world / map."""
    bbox1 = cmds.exactWorldBoundingBox('streetMap')
    bbox2 = cmds.exactWorldBoundingBox(car)
    
    if (bbox2[2]>=bbox1[2] and bbox2[2]<=bbox1[5] or bbox2[5]>=bbox1[2] and bbox2[5]<=bbox1[5]) and (bbox2[0]>=bbox1[0] and bbox2[0]<=bbox1[3] or bbox2[3]>=bbox1[0] and bbox2[3]<=bbox1[3]):
        return True
        
def hitBuilding(car, buildingIndex):
    """Checks if the car has hit a building set.
    Returns True if collision between car and a building set is detected."""
    bbox1 = cmds.exactWorldBoundingBox(buildingList[buildingIndex])
    bbox2 = cmds.exactWorldBoundingBox(car)
    
    if (bbox2[2]>=bbox1[2] and bbox2[2]<=bbox1[5] or bbox2[5]>=bbox1[2] and bbox2[5]<=bbox1[5]) and (bbox2[0]>=bbox1[0] and bbox2[0]<=bbox1[3] or bbox2[3]>=bbox1[0] and bbox2[3]<=bbox1[3]):
        return True
   
def fixAngles(obj1, listNum):
    """Checks current angle of car passed in.
    Clamps angle to certain values based on junction turning."""
    rotation = cmds.xform(obj1, ro=True, q=True)
    angle = rotation[1]
    angle = int(angle)
    angleX = rotation[0]
    
    if carList[listNum][1] < 3 and carList[listNum][1] >= 0:
        if angle == 90 or (angle > 85 and angle < 95):
            cmds.xform(obj1, ro=(0,90,0), os=True, p=True)
            carList[listNum][1] == 2 
        elif angle == -90 or (angle > -95 and angle < -85):
            cmds.xform(obj1, ro=(0,-90,0), os=True, p=True)
            carList[listNum][1] == 2 
        elif angle == 0 :
            cmds.xform(obj1, ro=(0,0,0), os=True, p=True)
            carList[listNum][1] == 2 
        elif angle == 180 or (angle >= 175.0 and angle <= 185.0) or (angle >= -185.0 and angle <= -175.0):
            cmds.xform(obj1, ro=(0,180,0), os=True, p=True)
            carList[listNum][1] == 2    
        elif angle == 270 or (angle >= 265.0 and angle <= 275.0):
            cmds.xform(obj1, ro=(0,-90,0), os=True, p=True)
            carList[listNum][1] == 2   
    if angleX < 0:
        cmds.xform(obj1, ro=(0,rotation[1],rotation[2]), os=True, p=True)
        
    if carList[listNum][1] == 2:
        if angle > -45 and angle < 45:
            cmds.xform(obj1, ro=(0,0,0), os=True, p=True)
        elif angle > 45 and angle < 135:
            cmds.xform(obj1, ro=(0,90,0), os=True, p=True)
        elif angle > -135 and angle < -45:
            cmds.xform(obj1, ro=(0,-90,0), os=True, p=True)
        elif angle > 135 and angle < 225:
            cmds.xform(obj1, ro=(0,180,0), os=True, p=True)


#========================================================================
# UPDATE FUNCTION
#========================================================================  
def update(frame):
    """Main AI function that executes all car behaviour.
    Run in expression editor: python("update("+frame+")");"""
    decision = 0
    
    # Check and clamp angle of cars in scene
    for j in range (0, len(carList)):
        fixAngles(carList[j][0], j) 
        # Prevent cars from leaving the world. Cause them to lose control
        if not inWorld(carList[j][0]) and carList[j][1] != -1:
            crash(j)
            
    # Check if the car has hit a building and cause it to crash if so
    for i in range (0, len(carList)):
        if carList[i][1] == -1:
            continue
        for j in range (0, len(buildingList)):
            if (hitBuilding(carList[i][0], j)):
                crash(i)  
                
    # Check if car is a taxi, then check if near a taxi stand
    for i in range (0, len(carList)):
        name = carList[i][0]
        checkName = name[:4]
        if checkName == 'taxi':
            for j in range (0, len(taxiStandList)):
                dist = distanceBetween(name, taxiStandList[j])
                if dist < 7.5 and carList[i][1] != 99 and carList[i][1] > 0:
                    print 'Stopping for passengers'
                    stopForPassengers(i)
    
    
    # Check for collision detection
    for j in range (0, len(carList)):
        for k in range (0, len(carList)):
            if j == k:
                continue
            
            if carList[j][1] == 3 or carList[j][1] < 0:
                continue
            
            dist = distanceBetween(carList[j][0],carList[k][0])
            
            cmds.xform(carList[j][0], t=velocity1_1, r=True, os=True)
            frontDistance = distanceBetween(carList[j][0],carList[k][0])
            cmds.xform(carList[j][0], t=velocity2_1, r=True, os=True)
            
            cmds.xform(carList[j][0], t=velocitySide2, r=True, os=True)
            leftDistance = distanceBetween(carList[j][0],carList[k][0])
            cmds.xform(carList[j][0], t=velocitySide, r=True, os=True)
            
            cmds.xform(carList[j][0], t=velocitySide, r=True, os=True)
            rightDistance = distanceBetween(carList[j][0],carList[k][0])
            cmds.xform(carList[j][0], t=velocitySide2, r=True, os=True)
            
            collided = detectCollision(carList[k][0],carList[j][0])
            
            #What happens if the cars collide
            if collided == True and carList[j][1] >= 0:
                decision = random.randint(0,1)
                if decision == 0:
                    crash(j)
                    crash(k)
                    print 'Crashed'
                elif decision == 1:
                    crash(j)
                    spinOut(k)
                    print 'Spin out of control and crash'
            
            # Drive around breaked / stalled cars if possible
            elif frontDistance < 2.0 and carList[k][1] == 3 and carList[k][3] < 10 and carList[j][1] != 4:
                driveAround(j)
                print 'Drive around breaked / stalled car'
                        
            # Swerve / emergency stop appropriately
            else:
                if frontDistance < 2.0 and carList[j][1] >= 0 and leftDistance > 2.0 and rightDistance > 2.0 and carList[k][1] >= 0 and carList[j][1] != 4:
                    maybeBrakeFail = random.randint(0,20)
                    if maybeBrakeFail >= 10:
                        continue
                    else:
                        emergencyStop(j)
                        print 'Emergency Stopped'
                elif frontDistance < 2.0 and carList[j][1] >= 0 and carList[k][1] == 3  and carList[j][1] != 4:
                    maybeReckless = random.randint(0,20)
                    if maybeReckless > 12:
                        continue
                    else:
                        driveAround(j)
                        print 'Drive Around'
                elif (leftDistance < 2.3 or rightDistance < 2.3) and carList[j][2] == -1 and carList[j][1] == 2: 
                    swerve(j)
                    print 'Swerved'

            
        # Recover after stopping
        if carList[j][1] == 3:
            carList[j][3] = carList[j][3] + 1
            if carList[j][3] >= 35:
                carList[j][3] = 0
                if carList[j][2] == -1:
                    carList[j][1] = 6
                    carList[j][4] = 6
                    print 'Recovering slowly'
                else:
                    carList[j][1] = carList[j][4]
                    carList[j][4] = 2
                    print 'Recovering from Stop'
            
        # Occasionally have some of the cars stall        
        possibleStall = random.randint(0,500)
        if possibleStall > 498 and carList[j][1] == 2 and carList[j][2] == -1:
            emergencyStop(j)
            print 'Oh No! Car Stalled!'
        
        # Drive around
        if carList[j][1] == 4:
            carList[j][3] = carList[j][3] + 1
            if carList[j][3] >= 1 and carList[j][3] <= 3:
                cmds.xform(carList[j][0], ro=(0,-14,0), r=True, os=True)
            elif carList[j][3] >= 8 and carList[j][3] <= 11:
                cmds.xform(carList[j][0], ro=(0,14,0), r=True, os=True)
            elif carList[j][3] >= 14 and carList[j][3] <= 17:
                cmds.xform(carList[j][0], ro=(0,14,0), r=True, os=True)
            elif carList[j][3] >= 22 and carList[j][3] <= 25:
                cmds.xform(carList[j][0], ro=(0,-14,0), r=True, os=True)
            if carList[j][3] == 25:
                carList[j][3] = 0
                carList[j][1] = 2
        
        # Swerve        
        if carList[j][1] == 5:
            carList[j][3] = carList[j][3] + 1
            if carList[j][3] == 3:
                cmds.xform(carList[j][0], ro=(0,28,0), r=True, os=True)
            elif carList[j][3] == 6:
                cmds.xform(carList[j][0], ro=(0,-28,0), r=True, os=True)
            elif carList[j][3] == 9:
                cmds.xform(carList[j][0], ro=(0,14,0), r=True, os=True)
                carList[j][3] = 0
                noControl = random.randint(0,1)
                if noControl == 0:
                    carList[j][1] = 2
                elif noControl == 1:
                    spinOut(j)
        
        # Recover from stopping (not from stopping in a junction)
        if carList[j][1] == 6:
            carList[j][3] = carList[j][3] + 1
            if carList[j][3] < 6:
                cmds.xform(carList[j][0], t = velocity3_1, r=True, os=True)
            elif carList[j][3] >= 6 and carList[j][3] <9:
                cmds.xform(carList[j][0], t = velocity1_2, r=True, os=True)
            elif carList[j][3] == 9:
                carList[j][3] = 0
                carList[j][1] = 2
        
        # Spin out of control
        if carList[j][1] == -2:
            carList[j][3] = carList[j][3] + 1
            carPos = cmds.xform(carList[j][0], t=True, q=True)
            if carList[j][3] >= 2 and carList[j][3] < 20:
                cmds.xform(carList[j][0], ro=(0,24,0), r=True, os=True)
                cmds.xform(carList[j][0], t=(carPos[0]+0.1,carPos[1],carPos[2]+0.1))
            elif carList[j][3] == 20:
                carList[j][3] = 0
                crash(j)
                
        # Resolve panic behaviour and crash
        if carList[j][1] == -4:
            carList[j][3] = carList[j][3] + 1
            if carList[j][3] == 1:
                cmds.xform(carList[j][0], t = velocity1_1, r=True, os=True)
                cmds.xform(carList[j][0], ro = (0,-30,0), r=True, os=True)
            elif carList[j][3] < 8:
                cmds.xform(carList[j][0], t = velocity1_1, r=True, os=True)
            elif carList[j][3] >=8 and carList[j][3] < 18:
                cmds.xform(carList[j][0], t = velocity3_1, r=True, os=True)
                direction = random.randint(0,1)
                if direction == 0:
                    cmds.xform(carList[j][0], ro = (0,14,0), r=True, os=True)
                else:
                    cmds.xform(carList[j][0], ro = (0,-14,0), r=True, os=True)
            elif carList[j][3] == 18:
                carList[j][3] = 0
                skid(j)
                
        # Cause the car to speed forward, skidding and not reacting to additional events
        if carList[j][1] == -5:
            cmds.xform(carList[j][0], t = velocity1_1, r=True, os=True)
            
        # Allows for taxis to stop and pick up passengers
        if carList[j][1] == 99:
            carList[j][3] = carList[j][3] + 1
            if carList[j][3] < 4:
                cmds.xform(carList[j][0], t = velocity1, r=True, os=True)
                cmds.xform(carList[j][0], ro = (0,-12,0), r=True, os=True)
            elif carList[j][3] >= 4 and carList[j][3] < 8:
                cmds.xform(carList[j][0], ro = (0,12,0), r=True, os=True)
                cmds.xform(carList[j][0], t = velocity1, r=True, os=True)
            elif carList[j][3] >= 20 and carList[j][3] < 24:
                cmds.xform(carList[j][0], t = velocity1, r=True, os=True)
                cmds.xform(carList[j][0], ro = (0,12,0), r=True, os=True)
            elif carList[j][3] >= 24 and carList[j][3] < 28:
                cmds.xform(carList[j][0], ro = (0,-12,0), r=True, os=True)
                cmds.xform(carList[j][0], t = velocity1, r=True, os=True)
            if carList[j][3] == 27:
                carList[j][3] = 0
                carList[j][1] = 2
        
    
    #Enable cars to know about crashes that have occured and act accordingly
    if len(crashList) != 0:
        for i in range (0, len(carList)):
            if carList[i][1] < 0:
                continue
            for j in range (0, len(crashList)):
                cmds.xform(carList[i][0], t=velocityFar, r=True, os=True)
                farFrontDistance = distanceBetween(carList[i][0],crashList[j])
                cmds.xform(carList[i][0], t=velocityFarBack, r=True, os=True)
                
                mayPanic = random.randint(0,1)
                if mayPanic == 0:
                    if farFrontDistance < 1.0 and carList[i][1] >= 0:
                        driveAround(i)
                        print 'Driving Around Crash'
                else:
                    if farFrontDistance < 1.6 and carList[i][1] >= 0 and carList[i][1] != 4:
                        panic(i)
                        print 'Panic Due to Crash'
        
    
    # Determines decision for cars to make if at a junction
    # Also updates car if turning or if going straight       
    for i in range (0, len(carList)):
        carRotation = cmds.xform(carList[i][0], ro=True, q=True)
        carAngle = carRotation[1]
        count = 0
        
        if carList[i][1] == 3 or carList[i][1] < 0:
            continue
        
        for j in range (0, len(juncList)):
            if (inJunction(carList[i][0], j)):
                break
            else:
                count = count + 1
        
        if (count == len(juncList)):
            carList[i][2] = -1
        if (count < len(juncList) and carList[i][2] == -1):
            carList[i][2] = j
            
            # Different junction type behaviours
            
            if (juncList[j][1] == 'ALL'):
                decision = random.randint(0,2)
                if decision == 0 :
                    turnLeft(carList[i][0])
                    carList[i][1] = 0
                elif decision == 1:
                    turnRight(carList[i][0])
                    carList[i][1] = 1
                elif decision == 2:
                    carList[i][1] = 2
                    
            elif (juncList[j][1] == 'ILR'):
                if carAngle == 180:
                    decision = random.randint(0,1) 
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                elif carAngle == 90:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                    elif decision == 1:
                        carList[i][1] = 2
                elif carAngle == -90:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        carList[i][1] = 2
                        
            elif (juncList[j][1] == 'IL'):
                if carAngle == 180:
                    turnRight(carList[i][0])
                    carList[i][1] = 1
                elif carAngle == -90:
                    turnLeft(carList[i][0])
                    carList[i][1] = 0
                    
            elif (juncList[j][1] == 'IR'):
                if carAngle == 180:
                    turnLeft(carList[i][0])
                    carList[i][1] = 0
                elif carAngle == 90:
                    turnRight(carList[i][0])
                    carList[i][1] = 1
                    
            elif (juncList[j][1] == 'LR'):
                if carAngle == 0:
                    decision = random.randint(0,1) 
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                elif carAngle == 90:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        carList[i][1] = 2
                elif carAngle == -90:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                    elif decision == 1:
                        carList[i][1] = 2
                        
            elif (juncList[j][1] == 'L'):
                if carAngle == -90:
                    turnRight(carList[i][0])
                    carList[i][1] = 1
                elif carAngle == 0:
                    turnLeft(carList[i][0])
                    carList[i][1] = 0
                    
            elif (juncList[j][1] == 'R'):
                if carAngle == 90:
                    turnLeft(carList[i][0])
                    carList[i][1] = 0
                elif carAngle == 0:
                    turnRight(carList[i][0])
                    carList[i][1] = 1
                    
            elif (juncList[j][1] == 'FL'):
                if carAngle == 0:
                    decision = random.randint(0,1) 
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        carList[i][1] = 2
                elif carAngle == -90:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                elif carAngle == 180:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                    elif decision == 1:
                        carList[i][1] = 2
                        
            elif (juncList[j][1] == 'FR'):
                if carAngle == 0:
                    decision = random.randint(0,1) 
                    if decision == 0 :
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                    elif decision == 1:
                        carList[i][1] = 2
                elif carAngle == 90:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        turnRight(carList[i][0])
                        carList[i][1] = 1
                elif carAngle == 180:
                    decision = random.randint(0,1)
                    if decision == 0 :
                        turnLeft(carList[i][0])
                        carList[i][1] = 0
                    elif decision == 1:
                        carList[i][1] = 2
      
        if carAngle%90.0 > 0.0 and carList[i][1] == 0:
            turnLeft(carList[i][0])
        elif carAngle%90.0 > 0.0 and carList[i][1] == 1:
            turnRight(carList[i][0])         
        elif (carAngle%90.0 == 0.0 or carList[i][1] == 2 or carList[i][1] == 5) and carList[i][1] != 3 and carList[i][1] != 4:
            goStraight(carList[i][0])
        elif carList[i][1] == 4:
            goSlow(carList[i][0])
            
                

#========================================================================
# RESET FUNCTIONS
#========================================================================
def reset():
    cmds.xform('car1', t=(2,1,20), ro=(0,0,0))
    cmds.xform('car2', t=(-30,1,-2), ro=(0,90,0))
    cmds.xform('car3', t=(-2,1,25), ro=(0,180,0))
    cmds.xform('car4', t=(-20,1,2), ro=(0,-90,0))
    cmds.xform('car5', t=(2,1,30), ro=(0,0,0))
    cmds.xform('car6', t=(-2,1,-30), ro=(0,180,0))
    cmds.xform('car7', t=(47,1,60), ro=(0,0,0))
    cmds.xform('car8', t=(92,1,70), ro=(0,0,0))
    cmds.xform('car9', t=(43,1,75), ro=(0,180,0))
    cmds.xform('car10', t=(47,1,-10), ro=(0,0,0))
    cmds.xform('car11', t=(43,1,-30), ro=(0,180,0))
    cmds.xform('car12', t=(20,1,47), ro=(0,-90,0))
    cmds.xform('car13', t=(30,1,43), ro=(0,90,0))
    cmds.xform('car14', t=(-30,1,92), ro=(0,-90,0))
    cmds.xform('car15', t=(70,1,87), ro=(0,90,0))
    cmds.xform('car16', t=(2,1,70), ro=(0,0,0))
    cmds.xform('car17', t=(20,1,-2), ro=(0,90,0))
    cmds.xform('car18', t=(-2,1,60), ro=(0,180,0))
    cmds.xform('car19', t=(20,1,2), ro=(0,-90,0))
    cmds.xform('car20', t=(2,1,-30), ro=(0,0,0))
    cmds.xform('taxi1', t=(43,1,20), ro=(0,180,0))
    cmds.xform('taxi2', t=(-43,1,80), ro=(0,0,0))
        
def clearLocators():
    test = cmds.select('crash*')
    cmds.delete()

reset()
#clearLocators()
