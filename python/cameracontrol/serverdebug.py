import os, sys
from ctypes.util import find_library
import pexpect, traceback, threading, Queue, time, socket

print 'this is a test'



#def worker( address, commands ):
def worker( cmdQueue, i, ):
    cmd = cmdQueue.get()
    while True:
        if cmd is None:
            print i,'attempting to clean up'
            return
        else:
            print cmd
            print i, 'is still running' 

def main():
    print 'Server running, ready to accept commands to pass over BTLE to peripherals.'

    queues = []

    threads = []
    for i in range(10):
        q = Queue.Queue()
        queues.append(q)

        cmdQueue = queues[i]
        #t = threading.Thread(target=worker, args=(connection, cmdList))
        t = threading.Thread(target=worker, args=(cmdQueue, i, ))
        t.daemon = True 
        threads.append(t)
    
    for t in threads:
        t.start()

    try:
        while 1:
            print 'running'
        print 'closing normally'
        for t in threads:
            t.join() #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        print 'serial connection closed'
        sys.exit()

    except (KeyboardInterrupt, ValueError, socket.error) as inst:
        print type(inst)
        print 'closing due to error'
        print queues
        print threads
        for q in queues:
            q.put(None)
        for t in threads:
            t.join() #timeout required so that main thread also receives KeyboardInterrupt
        print 'threads closed'
        print 'serial connection closed'
        sys.exit()

    #sys.exit(0)


if __name__ == "__main__":
    main()

# help from: http://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
