#!/usr/bin/env python

# with help from https://github.com/msaunby/ble-sensor-pi/blob/master/sensortag/sensortag.py
# Michael Saunby. April 2013

import os, sys
from ctypes.util import find_library
import pexpect, traceback, threading, Queue, time, socket
import constants, blescan


if not os.geteuid() == 0:
    sys.exit("script only works as root")

btlib = find_library("bluetooth")
if not btlib:
    raise Exception(
        "Can't find required bluetooth libraries"
    )
    
class bleBot:

    def __init__( self, ble_adr ):
        self.ble_adr = ble_adr
        self.con = pexpect.spawn('gatttool -b ' + self.ble_adr + ' -I -t random')
        self.con.delaybeforesend = 0 #THIS LINE IS SUPER IMPORTANT
        self.con.expect('\[LE\]', timeout=1)
        self.handle = 'b' #!! this is the TX service on the nRF8001 adafruit breakout with callbackEcho sketch

    def connect( self ):
        # OH HEXAPOD this is so sketchy, it will break if bluez gatttool changes at all. I have version 5.20
        print "Preparing to connect. Address: " + self.ble_adr
        self.con.sendline('connect')
        i = self.con.expect(['Attempting', 'Error'], timeout=1)
        if i == 0:
            #print 'Attempting to connect'
            j = self.con.expect(['Connection successful', 'No route', 'busy', pexpect.TIMEOUT], timeout = 1)
            if j == 0:
                print self.ble_adr, ': connected!'
            if j == 1:
                print self.ble_adr, ': No route to host, is USB dongle plugged in?'
                self.cleanup()
            if j == 2:
                print self.ble_adr, ': Device busy, is something else already connected to it?'
                c = True
                while c:
                    inp = raw_input('Try hitting reset. Type "y" to continue or "n" to quit.')
                    if inp.lower().startswith('y'):
                        self.con.sendline('connect')
                        k = self.con.expect(['Connection successful', pexpect.TIMEOUT], timeout = 1)
                        print 'k: ', k
                        if k == 0:
                            print self.ble_adr, ': connected!'
                        if k == 1:
                            print self.ble_adr, ': Could not connect'
                            self.cleanup()
                        break
                    elif inp.lower().startswith('n'):
                        self.cleanup()
                        break
                    else:
                        print 'Did not understand command. Try again.'
            if j == 3:
                print 'Attempting to connect, is device on and in range? '
                #foostr = raw_input('Type anything to continue, or enter to cancel')
                self.con.sendline('connect')
                k = self.con.expect(['Connection successful', pexpect.TIMEOUT], timeout = 3)
                print 'k: ', k
                if k == 0:
                    print self.ble_adr, ': connected!'
                if k == 1:
                    print self.ble_adr, ': Could not connect'
                    self.cleanup()
        if i == 1:
            print 'Is USB dongle plugged in?'
            self.cleanup()
        return self
         
    def char_write_cmd( self, value ):
        # The 0%x for value is VERY naughty!  Fix this!
        cmd = 'char-write-cmd 0x%s %s' % (self.handle, value)
        #print self.ble_adr, cmd
        self.con.sendline( cmd )
        try:
            print self.con.read_nonblocking(1024,0)
        except:
            pass
        #print 'After sending command, before: ', self.con.before, 'after :', self.con.after
        return


    def cleanup( self ):
        print self.ble_adr, ': attempting to disconnect'
        try:
            self.con.sendline('disconnect')
            self.con.sendline('exit')
            isalive = self.con.terminate(force=True)
            print self.ble_adr, ': has been terminated? ', isalive
            self.con.close(force=True)
            #print self.ble_adr, 'is alive: ', self.con.isalive()
        except OSError:
            print self.ble_adr, ': OSError'
            pass
        return



def tupToHex( foolist ):
    hexed = ''
    for i in foolist :
        hexed += format(i, '02x')
    #print hexed
    return hexed

#def worker( address, commands ):
def worker( cmdQueue, connection):
    while True:
        cmd = cmdQueue.get()
        print connection.ble_adr, 'rcvd from queue:', cmd
        #print connection.ble_adr, ': queue size: ', cmdQueue.qsize()
        if cmd is None:
            print connection.ble_adr, ': attempting to cleanup'
            connection.cleanup()
            return 
        else:
            connection.char_write_cmd(tupToHex(cmd))


#def ports_init(portnum):

def main():
    print 'Server running, ready to accept commands to pass over BTLE to peripherals.'

    connections = []

    addresses = blescan.blescan()
    while len(addresses) < constants.NUM_ROBOTS:
        c = True
        while c:
            inp = raw_input('Expected ' + str(constants.NUM_ROBOTS) + ', found ' + str(len(addresses)) + ' robots. Try hitting reset on the robots. Type "y" to continue or "n" to quit.')
            if inp.lower().startswith('y'):
                addresses = blescan.blescan()
                break
            elif inp.lower().startswith('n'):
                sys.exit('User cancelled program when told not enough robots found.')
                break
            else:
                print 'Did not understand command. Try again.'
    if len(addresses) > constants.NUM_ROBOTS:
        culled_adr = []
        c = True
        while c:
            addresses = list(addresses)
            print addresses
            inp = raw_input('Expected ' + str(constants.NUM_ROBOTS) + ', found ' + str(len(addresses)) + ' robots. \
                    Enter numbers of the robots you want, separated by commas. e.g. "0,4"')
            indices = inp.split(',')
            if inp.lower().startswith('n'):
                sys.exit('User cancelled program when told too many robots found.')
                break
            for i in indices:
                culled_adr = addresses[int(i)] 
            break
            #else:
                #print 'Did not understand command. Try again.'
        print 'culled', culled_adr
        addresses = set()
        addresses.add(culled_adr)
    for address in addresses:
        b = bleBot(address)
    # first connect them all because that takes the longest
        connection = b.connect()
        connections.append(connection)

    queues = []

    threads = []
    for i in range(len(addresses)):
        q = Queue.Queue()
        queues.append(q)

        cmdQueue = queues[i]
        connection = connections[i]
        #t = threading.Thread(target=worker, args=(connection, cmdList))
        t = threading.Thread(target=worker, args=(cmdQueue, connection))
        t.daemon = True 
        threads.append(t)
    
    for t in threads:
        t.start()

    #ports_init(int(sys.argv[1]))
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = constants.PORT_BTLE # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'port: ', PORT, '|| Connected by', addr


    try:
        while 1:
            data = conn.recv(1024)
            #print 'rcvd data', data
            if not data: break
            #print 'received data', data
            strRGB = data
            cmd = [int(s) for s in strRGB.split(',')]
            if len(cmd) == constants.LENGTH_CMD:
                botID = cmd[0]
                queues[botID].put(cmd[1:])
            else:
                print 'invalid command received: ', cmd

            #print cmd

            #botnum = cmd[0]
            #botcmd = cmd[1:4]
            #rgbcmd = [0,0,0]
            #botcmd = rgbcmd + botcmd
            #print 'botcmd', botcmd
            #queues[botnum].put(botcmd)
            
            #queues[0].put([255,0,0,92,92])
            #queues[1].put([255,0,0,92,92])

            #cmdRed = cmd[0:3]
            #cmdGreen = cmd[3:6]
            #cmdBlue= cmd[6:9]
            #queues[0].put(cmdRed)
            #queues[1].put(cmdGreen)
            #queues[2].put(cmdBlue)
            
        print 'closing normally'
        print 'number of connections: ', len(connections)
        for q in queues:
            q.put(constants.KILL_CMD)
            q.put(None)
        for t in threads:
            t.join() #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print 'serial connection closed'
        sys.exit()

    except (KeyboardInterrupt, ValueError, socket.error) as inst:
        print type(inst)
        print 'closing due to error'
        print 'number of connections: ', len(connections)
        for q in queues:
            q.put(constants.KILL_CMD)
            q.put(None)
        for t in threads:
            t.join() #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print 'serial connection closed'
        sys.exit()

    #sys.exit(0)


if __name__ == "__main__":
    main()

