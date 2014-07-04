#!/usr/bin/env python

# with help from https://github.com/msaunby/ble-sensor-pi/blob/master/sensortag/sensortag.py
# Michael Saunby. April 2013

import os
import sys
from ctypes.util import find_library
import pexpect
import traceback
import threading
import Queue
import time
import socket

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
            print 'j: ', j
            if j == 0:
                print self.ble_adr, ': connected!'
            if j == 1:
                print self.ble_adr, ': No route to host, is USB dongle plugged in?'
                self.cleanup()
            if j == 2:
                print self.ble_adr, ': Device busy, is something else already connected to it? Try hitting reset. You have 3 seconds.'
                time.sleep(3)
                self.con.sendline('connect')
                k = self.con.expect(['Connection successful', pexpect.TIMEOUT], timeout = 1)
                print 'k: ', k
                if k == 0:
                    print self.ble_adr, ': connected!'
                if k == 1:
                    print self.ble_adr, ': Could not connect'
                    self.cleanup()
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
        return


    def cleanup( self ):
        print self.ble_adr, ': attempting to disconnect'
        try:
            self.con.sendline('disconnect')
            print self.ble_adr, ': disconnected'
            self.con.sendline('exit')
            self.con.close(force = True)
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
def worker( cmdQueue, connection, run_event ):
    while run_event.is_set():
        cmd = cmdQueue.get()
        connection.char_write_cmd(tupToHex(cmd))
    # when we catch a keyboard interrupt, make sure to close the bluetooth connection


#def ports_init(portnum):

def main():
    run_event = threading.Event()
    run_event.set()

    if len(sys.argv) > 2:
        #ports_init(int(sys.argv[1]))
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = int(sys.argv[1])   # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        addresses = sys.argv[2:]
    else:
        sys.exit("Usage: sudo python btle-server.py $PORTNUM $BLUETOOTH_ADDRESS1 $BTLE_ADR2")


    connections = []
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
        t = threading.Thread(target=worker, args=(cmdQueue, connection, run_event))
        t.daemon = True 
        threads.append(t)
    
    for t in threads:
        t.start()

    try:
        while 1:
            data = conn.recv(1024)
            #print 'rcvd data', data
            if not data: break
            strRGB = data
            cmd = [int(s) for s in strRGB.split(',')]
            #print cmd

            botnum = cmd[0]
            botcmd = cmd[1:4]
            rgbcmd = [0,0,0]
            botcmd = rgbcmd + botcmd
            print 'botcmd', botcmd
            queues[botnum].put(botcmd)
            #queues[0].put([255,0,0,100,100])

            #cmdRed = cmd[0:3]
            #cmdGreen = cmd[3:6]
            #cmdBlue= cmd[6:9]
            #queues[0].put(cmdRed)
            #queues[1].put(cmdGreen)
            #queues[2].put(cmdBlue)
            
        conn.close()
        print 'closing connections',connections
        run_event.clear()
        for c in connections:
            connection.cleanup()
        for t in threads:
            t.join(1) #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print 'serial connection closed'
        sys.exit()

    except (KeyboardInterrupt, ValueError, socket.error) as inst:
        print type(inst)
        print 'closing connections',connections
        run_event.clear()
        for c in connections:
            connection.cleanup()
        for t in threads:
            t.join(1) #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print 'serial connection closed'
        sys.exit()

    #sys.exit(0)


if __name__ == "__main__":
    main()

# help from: http://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
