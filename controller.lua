function sysCall_init() -- Set timeOut
    timeOut = 10
    -- Robot ID
    ID = 0
    signal = 'signal_'..tostring(ID) endSignal = 'endSignal_'..tostring(ID)
    -- Get joint handles bodyJoints={-1,-1,-1,-1,-1,-1} kneeJoints={-1,-1,-1,-1,-1,-1} footJoints={-1,-1,-1,-1,-1,-1} for i=1,6,1 do
    bodyJoints[i]=sim.getObjectHandle('hexa_joint1_'..i-1) kneeJoints[i]=sim.getObjectHandle('hexa_joint2_'..i-1) footJoints[i]=sim.getObjectHandle('hexa_joint3_'..i-1)
    end
    -- Get body handle
    bodyHandle = sim.getObjectHandle('hexa_body')
    -- Get initial position
    pos1 = sim.getObjectPosition(bodyHandle,-1)
    -- Get initial angles bodyAngles={-1,-1,-1,-1,-1,-1} kneeAngles={-1,-1,-1,-1,-1,-1} footAngles={-1,-1,-1,-1,-1,-1} for i=1,6,1 do
    bodyAngles[i]=sim.getJointTargetPosition(bodyJoints[i]) kneeAngles[i]=sim.getJointTargetPosition(kneeJoints[i]) footAngles[i]=sim.getJointTargetPosition(footJoints[i])
    end
    -- Init Console to Print --consoleHandle=sim.auxiliaryConsoleOpen('ouput stuff',25,2)
    -- Clear param signal sim.clearStringSignal(signal)
    -- Init params
    params = {}
    for i=1,8*3*6 do -- wrong size but works anyway
            params[i]=0
        end
    params = reshape(params)
        -- Init sendPos
        sendPos = true
    -- Debugging here dumpTable(params) dumpTable(pos1)
    end
    function sysCall_cleanup() end
    function sysCall_actuation()
    -- Get time
    t = sim.getSimulationTime()
    -- Check for params in String format packedTable = sim.getStringSignal(signal)
    -- New signal received - update params table if (packedTable ~= null) then
    -- Unpack params from API and reshape --sim.auxiliaryConsolePrint(consoleHandle,'Success! \n') params = sim.unpackFloatTable(packedTable) dumpTable(params)
    params = reshape(params)
    dumpTable(params)
            -- Clear signal
    sim.clearStringSignal(signal) end
    -- Check for timeOut
    check = sim.getIntegerSignal('timeOut') if (check ~= null) then
            timeOut = check
        end
    -- Actual Actuation here:
    -- Setting new target values using params - joints called individually for leg=1,6 do
    -- Calc new target value (sin is in rad)
    bodyAngles[leg] = params[1][leg][1]*math.sin(params[1][leg][2]*t + params[1][leg][3]) + params[1][leg][4]*math.cos(params[1][leg][5]*t + params[1][leg][6]) + params[1][leg][7]
    kneeAngles[leg] = params[2][leg][1]*math.sin(params[2][leg][2]*t + params[2][leg][3]) + params[2][leg][4]*math.cos(params[2][leg][5]*t + params[2][leg][6]) + params[2][leg][7]
    footAngles[leg] = params[3][leg][1]*math.sin(params[3][leg][2]*t + params[3][leg][3]) + params[3][leg][4]*math.cos(params[3][leg][5]*t + params[3][leg][6]) + params[3][leg][7]
    -- Set new target value sim.setJointTargetPosition(bodyJoints[leg],bodyAngles[leg]) sim.setJointTargetPosition(kneeJoints[leg],kneeAngles[leg]) sim.setJointTargetPosition(footJoints[leg],footAngles[leg])
    end
    -- Send position when time is up if (t > timeOut and sendPos) then
    -- Get current position compared to start pos2 = sim.getObjectPosition(bodyHandle,-1)
            -- Calc delta
            endPos = {}
            for i=1,2 do
    endPos[i] = pos2[i]-pos1[i]
    
    end
    -- Get absolute position in endPos[3] = pos2[3]
    -- Send table
    dumpTable(endPos)
    packedTable = sim.packFloatTable(endPos) sim.setStringSignal(endSignal, packedTable)
            --  Stop sending
            sendPos = false
        end
    end
    function reshape(t)
    -- Reshape to joints x legs x params table joints = 3 -- change this when adding cos legs = 6
    params = 7
    n = {} -- new matrix index = 0
    for j=1,joints do
            n[j] = {}
            for l=1,legs do
                n[j][l]={}
                for p=1,params do
    index = index + 1
    n[j][l][p] = t[index] end
    end end
    return n end
    -- Dumping to console function dump(o)
    if type(o) == 'table' then local s = '{ '
    for k,v in pairs(o) do
    if type(k) ~= 'number' then k = '"'..k..'"' end
    s = s .. '['..k..'] = ' .. dump(v) .. ',' end
    return s .. '} ' else
    return tostring(o) end
    end
    function dumpTable(t)
    --sim.auxiliaryConsolePrint(consoleHandle,'Table: \n'..dump(t)..'\n')
    end