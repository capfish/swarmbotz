import os, sys
from ctypes.util import find_library
import pexpect, traceback, threading, Queue, time, socket
import constants

print 'this is a test'



#def worker( address, commands ):
def worker( cmdQueue, i,  stop_event ):
    while not stop_event.is_set():
        print 'stop_event not set'
        cmd = cmdQueue.get()
    print i,'attempting to clean up'



def main():
    print 'Server running, ready to accept commands to pass over BTLE to peripherals.'
    stop_event = threading.Event()
    stop_event.clear()

    queues = []

    threads = []
    for i in range(10):
        q = Queue.Queue()
        queues.append(q)

        cmdQueue = queues[i]
        #t = threading.Thread(target=worker, args=(connection, cmdList))
        t = threading.Thread(target=worker, args=(cmdQueue, i, stop_event))
        t.daemon = True 
        threads.append(t)
    
    for t in threads:
        t.start()

    try:
        while 1:
            print 'running'
            queues[0].put('1')
            queues[1].put('1')
        stop_event.set()
        print 'closing normally'
        for t in threads:
            t.join(1) #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        print 'serial connection closed'
        sys.exit()

    except (KeyboardInterrupt, ValueError, socket.error) as inst:
        print type(inst)
        print 'closing due to error'
        #print threads
        stop_event.set()
        print 'is stop set?', stop_event.is_set()
        for t in threads:
            t.join(1) #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        print 'serial connection closed'
        sys.exit()

    #sys.exit(0)


if __name__ == "__main__":
    main()

# help from: http://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
