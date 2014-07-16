#!/usr/bin/env python

# with help from https://github.com/msaunby/ble-sensor-pi/blob/master/sensortag/sensortag.py
# Michael Saunby. April 2013

import os, sys
from ctypes.util import find_library
import pexpect, traceback, threading, Queue, time, socket, select
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
        try:
            self.con.read_nonblocking(2048,0) #flush the read pipe!! SUPER IMPORTANT
        except:
            pass
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
                        try:
                            self.con.read_nonblocking(2048,0) #flush the read pipe!! SUPER IMPORTANT
                        except:
                            pass
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
                try:
                    self.con.read_nonblocking(2048,0) #flush the read pipe!! SUPER IMPORTANT
                except:
                    pass
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
            print self.con.read_nonblocking(2048,0) #flush the read pipe!! SUPER IMPORTANT
        except:
            pass
        #print 'After sending command, before: ', self.con.before, 'after :', self.con.after
        return


    def cleanup( self ):
        print self.ble_adr, ': attempting to disconnect'
        try:
            self.con.sendline('disconnect')
            self.con.sendline('exit')
            try:
                self.con.read_nonblocking(2048,0) #flush the read pipe!! SUPER IMPORTANT
            except:
                pass
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
        #print 'queue items left: ', cmdQueue.qsize()
        print connection.ble_adr, 'rcvd from queue:', cmd
        #print connection.ble_adr, ': queue size: ', cmdQueue.qsize()
        if cmd is None:
            print connection.ble_adr, ': attempting to cleanup'
            connection.cleanup()
            return 
        else:
            connection.char_write_cmd(tupToHex(cmd))


#def ports_init(portnum):

def sendRobotCmds(cmd, queues):
    if cmd[1] == constants.PREFIX_COLOR:

        if len(cmd) == constants.LENGTH_CMD_C:
            botID = cmd[0]
            queues[botID].put(cmd[1:])
         ##############
         # for rgb music, because the packets tend to squish together
         # such hack much disgust
        else:
            if len(cmd) == 2*constants.LENGTH_CMD_C:
                cmd1 = cmd[:constants.LENGTH_CMD_C]
                botID = cmd1[0]
                queues[botID].put(cmd1[1:])
                cmd2 = cmd[constants.LENGTH_CMD_C:]
                botID = cmd2[0]
                queues[botID].put(cmd2[1:])


            #if len(cmd) == 2*constants.LENGTH_CMD_C-1:
                #clean = cmd[:constants.LENGTH_CMD_C]
                #clean[constants.LENGTH_CMD_C-1] = int(str(clean[constants.LENGTH_CMD_C-1])[:-1]) #strip final char from int
                #botID = clean[0]
                #queues[botID].put(clean[1:])
                #clean = cmd[constants.LENGTH_CMD_C-1:]
                #clean[0] = int(str(clean[0])[2:]) #strip first two char from int
                #botID = clean[0]
                #queues[botID].put(clean[1:])
            else:
                print 'invalid color command received: ', cmd
    elif cmd[1] == constants.PREFIX_SERVO:
        if len(cmd) == constants.LENGTH_CMD_S:
            botID = cmd[0]
            queues[botID].put(cmd[1:])
        else:
            if len(cmd) == 2*constants.LENGTH_CMD_S:
                cmd1 = cmd[:constants.LENGTH_CMD_S]
                botID = cmd1[0]
                queues[botID].put(cmd1[1:])
                cmd2 = cmd[constants.LENGTH_CMD_S:]
                botID = cmd2[0]
                queues[botID].put(cmd2[1:])
            else:
                print 'invalid servo command received: ', cmd
    else:
        print 'invalid command type (servo or color) received: ', cmd, 'expected: ', constants.CMD_FORMAT
def main():
    print 'Server running, ready to scan for BTLE peripherals.'

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
    print 'expecting port: ', PORT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(constants.MAX_BTLE_CONNECTIONS)
    sockets = []
    sockets.append(server_socket)
    print 'Server ready to accept commands to pass over BTLE to peripherals'

    while 1:
        try:
            read_sockets,write_sockets,error_sockets = select.select(sockets,[],[])
            for sock in read_sockets:
                if sock == server_socket:
                    try:
                        conn, addr = server_socket.accept()
                        sockets.append(conn)
                        print "Client (%s, %s) connect" % addr
                    except (KeyboardInterrupt, ValueError, socket.error) as inst:
                        print "Caught exception: ", type(inst), "closing ble connections"
                        for connection in connections:
                            connection.cleanup()
                        for conn in sockets:
                            conn.shutdown(socket.SHUT_RDWR)
                            conn.close()
                        sys.exit(0)
                    print 'port: ', PORT, '|| Connected by', addr
            
                else:
                    try:
                        data = sock.recv(2048)
                        #print 'received data', data
                        strRGB = data
                        ##############

                        cmd = [int(s) for s in filter(None, strRGB.rstrip().split(','))] #for python 
                        sendRobotCmds(cmd, queues)
                    except Exception as e:
                        print 'Exception', e
                        print "Client (%s, %s) is offline" % addr, 'removing from list of sockets: ', sockets
                        sock.close()
                        sockets.remove(sock)
                        continue
        except (KeyboardInterrupt) as inst:
            print type(inst)
            print 'closing due to error'
            print 'number of robots connected: ', len(connections)
            print 'number of sockets connect: ', len(sockets)
            for q in queues:
                q.put(constants.KILL_CMD_C)
                q.put(constants.KILL_CMD_S)
                q.put(None)
            for t in threads:
                t.join() #timeout required so that main thread also receives KeyboardInterrupt
            print 'threads closed'
            for conn in sockets:
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
                print 'serial connection closed: ', conn
            sys.exit()
    print 'closing normally'
    server_socket.close()



if __name__ == "__main__":
    main()

