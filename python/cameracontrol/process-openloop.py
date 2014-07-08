import os, sys
from math import atan2, pi, tan, sqrt
import constants, socket, time

    

numbots = 3

def processwave():
# bot1,2,3 for positions. bots is the list of bot1,2,3
    bot1 = []
    bot2 = []
    bot3 = []
    bots = []
    bots = [bot1,bot2,bot3]
    f = open("./positions.txt", "r")
    for line in f:
        cmd = [int(s) for s in line.split(',')]
        botid = cmd[0]
        bots[botid].append(tuple(cmd[1:]))


    #if delta x and delta y are zero then keep previous heading
    #else check for heading issue
    bot1h = []
    bot2h = []
    bot3h = []
    botheadings = [bot1h, bot2h, bot3h]
    for j in range(len(botheadings)):
        #print 'length', len(bots)
        print j
        bot = bots[j]
        bot_h = []
        headings = []
        prevheading = pi/2

        for i in range(len(bot)):
            x1 = bot[i][0]
            y1 = bot[i][1]
            x2 = bot[(i+1)%len(bot)][0]
            y2 = bot[(i+1)%len(bot)][1]
            deltax = x2-x1
            deltay = y2-y1
            if (deltax==0 and deltay==0):
                heading = prevheading
            else:
                heading = atan2(deltay, deltax)
            headings.append(heading)
            prevheading = heading
            #print heading
            
        #now i have a list of headings. what to do now?
        #flag for reverse:
        reverseFlag = False
        prevheading = pi/2
        initstate = [pi/2]
        headings = initstate + headings
        for k in range(len(headings)-1):
            deltah = abs(headings[k+1]-headings[k])
            #print deltah
            if (deltah > (pi/2)):
                reverseFlag = not reverseFlag
                bot_h.append((reverseFlag, deltah-pi/2))
                prevheading = deltah-pi/2
            else:
                bot_h.append((reverseFlag, prevheading))

        #print bot_h
        botheadings[j] = bot_h[:-1]#dirty hack, last values are wrong and i'm not sure how to fix so just trim for now

    zipped = zip(botheadings[0], botheadings[1], botheadings[2])
    #for i in zipped:
        #print i

    zipped2= zip(bots[0], bots[1], bots[2])
    #for i in zipped2:
        #print i

    f.close()
    return (bots, botheadings)

maxRotSpeed = 30.0
MAXROT_INV = (2.0/pi) * maxRotSpeed
maxSpeed = 30.0
MAXSPEED_INV = (1/10.0) * maxSpeed
RGBCMD = [0,0,0]

def formatCmd(botid, cmd):
    botid = [botid]
    finalcmd = str(botid+RGBCMD+cmd)[1:-1]
    print finalcmd + '\n'
    return str(finalcmd)

def driveServos(sock, botid, reverseFlag, dx, dy, dtheta):
    cmd = rotate(dtheta)
    cmd2= translate(reverseFlag, dx, dy) 
    addedCmd = [int(a+b) for a, b in zip(cmd, cmd2)]
    sock.send(formatCmd(botid, addedCmd))
    return(formatCmd(botid, addedCmd))

def translate(reverseFlag, dx, dy): #at max 10 pixel jump we go full speed
    dist = sqrt(dx**2 + dy**2)
    cmd = [dist * MAXSPEED_INV, dist * MAXSPEED_INV]
    if reverseFlag:
        cmd = [-bar for bar in cmd] 
        print 'reverse!'
    return cmd

def rotate(dtheta): #dtheta in radians -- a full pi/2 rotation = max speed, +- fullRotSpeed
    # pos dtheta = rotate CCW left back right fwd
    cmd = [90 - dtheta * MAXROT_INV, 90 + dtheta * MAXROT_INV]
    return cmd

def main():
    
    fi = open("./positions-python.txt", "w")
    host = constants.HOST_BTLE
    port = constants.PORT_BTLE
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    NUMROBOTS = 3
    sock.connect((host,port))

    bots, botheadings = processwave()
    print 'lengthbots', len(bots)
    print 'lengthboheadingts', len(botheadings)
    bot1, bot2, bot3 = bots
    bot1h, bot2h, bot3h = botheadings
    print 'bot1', bot1
    print 'bot1h', bot1h
    #heading: (False, 1.5707963267948966)
    #x, y = ((160, 328)
    for i in range(len(bot1)-2):
        for j in range(len(bots)):
            #(1,2) and (2,2)
            dx, dy = [foo-bar for foo, bar in zip(bots[j][i+1],bots[j][i])]
            reverseFlag = botheadings[j][i+1][0]
            print i, j
            dtheta = botheadings[j][i+1][1] - botheadings[j][i][1]
            finalcmd = driveServos(sock, j, reverseFlag, dx,dy, dtheta)
            fi.write(finalcmd + '\n')
        time.sleep(.05)

    fi.close()
    fi = open("./positions-python-format.txt", "w")
    data = open("./positions-python.txt", "r").readlines()
    for n, line in enumerate(data):
        if n%3 == 0:
            data[n] = '\n'+line.rstrip()
        else:
            data[n] = line.rstrip()
    fi.write(",".join(data))
    fi.close()
    sock.close()


if __name__ == "__main__":
    main()

