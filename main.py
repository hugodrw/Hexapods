
# Testing the API (works 8PopCos)
# This script works in continuous API mode
# To run in headless mode:
# /Applications/coppeliaSim.app/Contents/MacOS/coppeliaSim -h /Users/guy/Documents/3rd\ Year/FYP/Scenes/8Pop.ttt

# Import relevant modules
import sim
import numpy as np
import ctypes
import sys
import time
import random
import math

def connectToAPI():

    # Init connection
    sim.simxFinish(-1)   # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5)   # Connect to CoppeliaSim

    if clientID != -1:
        print('Connected to remote API server')
    else:
        print('Connection unsuccessful')
        sys.exit()

    return clientID

def initPop(popSize):
    # Init with random params
    # Returns list of members
    members = []
    for i in range(popSize):
        # Create new member:
        m = Member(i)

        # Initial 3 sin params, A B C G change this later
        p = 7

        # Init array
        params = np.zeros((3, 6, p))

        # Create Sin Param Array with random values
        # Body Joints
        for leg in range(6):
            params[0, leg, 0] = round(random.uniform(0, 0.5), 2)  # A
            params[0, leg, 1] = round(random.randrange(0, 8, 2), 2)    # B
            params[0, leg, 2] = round(random.uniform(0, 3.14), 2)    # C
            params[0, leg, 3] = round(random.uniform(0, 0.5), 2)  # D
            params[0, leg, 4] = round(random.randrange(0, 4, 1), 2)    # E
            params[0, leg, 5] = round(random.uniform(0, 3.14), 2)    # F
            params[0, leg, 6] = round(random.uniform(-1, 1), 2)   # G

        # Knee Joints
        for leg in range(6):
            params[1, leg, 0] = round(random.uniform(0, 0.5), 2)  # A
            params[1, leg, 1] = round(random.randrange(0, 8, 2), 2)    # B
            params[1, leg, 2] = round(random.uniform(0, 3.14), 2)    # C
            params[1, leg, 3] = round(random.uniform(0, 0.5), 2)  # D
            params[1, leg, 4] = round(random.randrange(0, 8, 2), 2)    # E
            params[1, leg, 5] = round(random.uniform(0, 3.14), 2)    # F
            params[1, leg, 6] = round(random.uniform(0, 1), 2)    # G

        # Foot Joints
        for leg in range(6):
            params[2, leg, 0] = round(random.uniform(0, 0.5), 2)  # A
            params[2, leg, 1] = round(random.randrange(0, 8, 2), 2)    # B
            params[2, leg, 2] = round(random.uniform(0, 3.14), 2)    # C
            params[2, leg, 3] = round(random.uniform(0, 0.5), 2)  # D
            params[2, leg, 4] = round(random.randrange(0, 8, 2), 2)    # E
            params[2, leg, 5] = round(random.uniform(0, 3.14), 2)    # F
            params[2, leg, 6] = round(random.uniform(0, 1), 2)    # G

        m.params = params

        members.append(m)

    return members

def initPopTripod(popSize):
    # To initialize with tripod gait
    # Returns list of members

    offset = math.pi/6


    members = []
    for i in range(popSize):
        # Create new member:
        m = Member(i)

        # Initial 3 sin params, A B C G change this later
        p = 7

        # Init array
        params = np.zeros((3, 6, p))

        # Create Sin Param Array with tripod values

        freqency = 8

        # Start with legs 0,2,4

        # Body Joints
        for leg in [0,2,4]:
            params[0, leg, 0] = 0.2 # A
            params[0, leg, 1] = freqency          # B
            params[0, leg, 2] = math.pi    # C
            params[0, leg, 3] = 0 # D
            params[0, leg, 4] = 0 # E
            params[0, leg, 5] = 0  # F
            params[0, leg, 6] = 0  # G

        # Knee Joints
        for leg in [0,2,4]:
            params[1, leg, 0] = 0.2  # A
            params[1, leg, 1] = freqency    # B
            params[1, leg, 2] = math.pi*5/2   # C
            params[1, leg, 3] = 0  # D
            params[1, leg, 4] = 0    # E
            params[1, leg, 5] = 0   # F
            params[1, leg, 6] = 0    # G

        # Foot Joints
        for leg in [0,2,4]:
            params[2, leg, 0] = 1.3  # A
            params[2, leg, 1] = 0   # B
            params[2, leg, 2] = math.pi*5/2    # C
            params[2, leg, 3] = 0 # D
            params[2, leg, 4] = 0  # E
            params[2, leg, 5] = 0   # F
            params[2, leg, 6] = 0   # G

        # Offset outside legs (0 and 4)
        params[0, 0, 6] = - math.pi/4  # G
        params[0, 4, 6] = math.pi/4  # G

        # Reverse middle leg (2)
        params[0, 2, 0] = - params[0, 2, 0]  # A

        # Legs 1,3,5

        # Body Joints
        for leg in [1,3,5]:
            params[0, leg, 0] =  0.2 # A
            params[0, leg, 1] = freqency          # B
            params[0, leg, 2] = 0  # C
            params[0, leg, 3] = 0 # D
            params[0, leg, 4] = 0 # E
            params[0, leg, 5] = 0  # F
            params[0, leg, 6] = 0  # G

        # Knee Joints
        for leg in [1,3,5]:
            params[1, leg, 0] = 0.2  # A
            params[1, leg, 1] = freqency    # B
            params[1, leg, 2] = math.pi*3/2   # C
            params[1, leg, 3] = 0  # D
            params[1, leg, 4] = 0    # E
            params[1, leg, 5] = 0   # F
            params[1, leg, 6] = 0    # G

        # Foot Joints
        for leg in [1,3,5]:
            params[2, leg, 0] = 1.3  # A
            params[2, leg, 1] = 0   # B
            params[2, leg, 2] = math.pi*5/2    # C
            params[2, leg, 3] = 0 # D
            params[2, leg, 4] = 0  # E
            params[2, leg, 5] = 0   # F
            params[2, leg, 6] = 0   # G

        # Offset outside legs (1 and 5)
        params[0, 1, 6] =  math.pi/4  # G
        params[0, 3, 6] = - math.pi/4  # G

        # Reverse middle leg (3)
        params[0, 3, 0] = - params[0, 3, 0]  # A

        # Reverse leg 1
        params[0, 1, 0] = - params[0, 1, 0]

        m.params = params

        members.append(m)

    return members

def testPop(members,timeOut):
    # Start simulation
    returnCode = sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print('Start Sim ReturnCode ' + str(returnCode))

    # Send timeOut
    returnCode = sim.simxSetIntegerSignal(clientID, 'timeOut', timeOut, sim.simx_opmode_oneshot_wait)
    print('TimeOut ReturnCode ' + str(returnCode))

    # Send params to all members
    for member in members:
        # Format params
        params = member.params
        packedData = sim.simxPackFloats(params.flatten())
        raw_bytes = (ctypes.c_ubyte * len(packedData)).from_buffer_copy(packedData)
        signal = 'signal_' + str(member.id)

        # Send param packets
        returnCode = sim.simxSetStringSignal(clientID, signal, raw_bytes, sim.simx_opmode_oneshot_wait)
        print('params sent to ' + str(member.id))
        print('ReturnCode ' + str(returnCode))

def uniformCross(members):
    # Number of params, change when adding cos
    p = 7

    # Remove bottom half of list
    members = members[:len(members) // 2]
    # Generate new Gen
    for i in range(0, len(members), 2):
        p1 = members[i].params.flatten()
        p2 = members[i+1].params.flatten()
        # Go through all params and attribute randomly to child
        c1 = uniformChild(p1, p2)
        c2 = uniformChild(p1, p2)
        # Assign new values to children and add to list
        m1 = Member(100+i)
        m2 = Member(101+i)
        m1.params = c1.reshape(3, 6, p)
        m2.params = c2.reshape(3, 6, p)
        members.append(m1)
        members.append(m2)

    # Reassign IDs
    i = 0
    for member in members:
        member.id = i
        i += 1
    return members


def singlePointCross(members):
    # Number of params, change when adding cos

    # Remove bottom half of list
    members = members[:len(members) // 2]
    # Generate new Gen
    for i in range(0, len(members), 2):
        p1 = members[i].params
        p2 = members[i+1].params
        c1 = singlePointChild(p1,p2)
        c2 = singlePointChild(p1,p2)
        m1 = Member(100+i)
        m2 = Member(101+i)
        m1.params = c1
        m2.params = c2
        members.append(m1)
        members.append(m2)


    # Reassign IDs
    i = 0
    for member in members:
        member.id = i
        i += 1

    return members

def singlePointChild(p1,p2):

    params = np.zeros((3, 6, 7))
    for leg in range(6):
        for joint in range (3):
            x = random.randrange(0,6,1)
            for coef in range (7):
                if coef > x:
                    params[joint,leg,coef] = p1[joint,leg,coef]
                else:
                    params[joint,leg,coef] = p2[joint,leg,coef]

    # Mutating in here
    mut = initPop(1)[0].params.flatten()
    params = params.flatten()

    for j in range(len(params)):
        x = random.random()
        if x > 0.95:
            params[j] = mut[j]

    params = params.reshape(3, 6, 7)

    return params

def uniformChild(p1,p2):

    c = np.zeros(len(p1))
    mut = initPop(1)[0].params.flatten()
    for j in range(len(p1)):
        x = random.random()
        if x < 0.5:
            c[j] = p1[j]
        elif x < 0.95:
            c[j] = p2[j]
        else:
            c[j] = mut[j]

    return c

def checkStatus():
    while True:
        # poll the useless signal (to receive a message from server)
        sim.simxGetIntegerSignal(clientID, 'Status', sim.simx_opmode_blocking)

        # check server state (within the received message)
        e = sim.simxGetInMessageInfo(clientID, sim.simx_headeroffset_server_state)

        # check bit0
        not_stopped = e[1] & 1

        if not not_stopped:
            break
        else:
            print('Waiting for sim to stop')

class Member:
    def __init__(self, id):
        self.params = []
        self.id = id
        self.position = None
        self.score = None

    def getPosition(self):
        signal = 'endSignal_' + str(self.id)
        returnCode, endSignal = sim.simxGetStringSignal(clientID, signal, sim.simx_opmode_oneshot_wait)
        position = list(sim.simxUnpackFloats(endSignal))
        while returnCode == 8 or len(position) == 0:
            print('waiting for position from member ' + str(self.id))
            time.sleep(3)
            returnCode, endSignal = sim.simxGetStringSignal(clientID, signal, sim.simx_opmode_oneshot_wait)
            position = list(sim.simxUnpackFloats(endSignal))

        self.position = position

    def calcScore(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        self.score = x
        if z < 0:
            print('Man down')
            print(self.id)
            self.score = -10




# MAIN SCRIPT:

# HyperParams
popSize = 8   # Needs to be a multiple of 4
scoreLimit = 20
timeOut = 10
increment = 0.3
startIncrement = 1

# Check for existing connection
if 'clientID' not in globals():
    clientID = connectToAPI()

# setup Status Signal
sim.simxSetIntegerSignal(clientID,'Status',1,sim.simx_opmode_blocking)

# --------Init Phase--------

# Initialise population with random parameters
members = initPopTripod(popSize)

# Test the population
testPop(members, timeOut)

# Get final position for each member
for member in members:
    member.getPosition()

# Stop Sim
returnCode = sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot_wait)
print('End Sim ReturnCode ' + str(returnCode))

# Calc score based on position
for member in members:
    member.calcScore()

# Sort members by score (highest score will get lowest index in list)
members.sort(key=lambda x: x.score, reverse=True)

# Fetch highest score
highScore = members[0].score

# Set Gen counter and scoreList
gen = 0
scoreList = []
floatTime = timeOut
print('Finished testing Generation ' + str(gen) + ' \nHighscore:  ' + str(highScore))

# --------Loop Phase--------
# Loop until score limit is reached
while highScore < scoreLimit:
    gen += 1
    # Set timeOut
    if gen % 2 == 0:
        timeOut = round(floatTime+random.randrange(-1,3,1))
        print('----floatTime')
        print(floatTime)
        print('----timeOut')
        print(timeOut)
    else:
        timeOut = floatTime

    print('Start testing Generation ' + str(gen))
    # Generate new members
    members = uniformCross(members)

    # Wait for sim to restart:
    checkStatus()

    # Test the population and get results (same as Init Phase)
    testPop(members, timeOut)
    for member in members:
        member.getPosition()

    # Stop Sim
    returnCode = sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print('End Sim ReturnCode ' + str(returnCode))

    for member in members:
        member.calcScore()
    members.sort(key=lambda x: x.score, reverse=True)

    # Update console:
    print('Finished testing Generation ' + str(gen) + ' \nScoreList:')
    for member in members:
        print(member.score)

    # Add highscore to list
    highScore = members[0].score
    if timeOut == 10:
        scoreList.append(highScore)
        print('added high score to list')
    np.save('ScoreList', scoreList)


# Debugging here
for member in members:
    print(member.score)
