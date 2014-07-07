import os, sys
from math import atan2, pi
    

numbots = 3

def main():
# bot1,2,3 for positions. bots is the list of bot1,2,3
    bot1 = []
    bot2 = []
    bot3 = []
    bots = []
    bots = [bot1,bot2,bot3]
    bots.append(bot1)
    bots.append(bot2)
    bots.append(bot3)
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
    for i in zipped:
        print i

    zipped2= zip(bots[0], bots[1], bots[2])
    for i in zipped2:
        print i

    f.close()

    

if __name__ == "__main__":
    main()

