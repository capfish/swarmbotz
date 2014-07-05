import pexpect, time, sys, signal

def closeall(connection):
    isalive = connection.terminate(force=True)
    print 'process was killed: ', isalive
    #hciout.kill(signal.SIGTERM)
    connection.close(force = True)

def gatheradr(conn):
    print 'Scanning for addresses...'
    start_time = time.time()
    elapsed_time = 0
    ble_adrs = set()
    try: 
        for line in conn:
            address = line.strip().split(' ')[0]
            if address != '':
                ble_adrs.add(address)
    except (pexpect.TIMEOUT):
        print '!!!!!! spawn timeout'
        pass

    #print ble_adrs
    print 'timeout!'
    closeall(conn)
    return ble_adrs

def blescan():
    ble_adrs = set()
    ble_adrs.add('test')
    try:
        hciout = pexpect.spawn('hcitool lescan', timeout=1)
        print 'spawning!'
    except (pexpect.TIMEOUT):
        print '!!! uhm spwan timeout'
    i = hciout.expect(['LE Scan ...','File descriptor in bad state',pexpect.TIMEOUT], timeout=1)
    if i == 0:
        ble_adrs = gatheradr(hciout)
    if i == 1:
        c = True
        while c: #code to check if input acceptable
            inp = raw_input('Check if dongle is plugged in. Type "y" to continue, or type "n" to cancel.')
            if inp.lower().startswith('y'):
                c = False 
                hciout.terminate()
                hciout.close()
                print 'Waiting a second for dongle to initialize'
                time.sleep(1)
                hciout = pexpect.spawn('hcitool lescan')
                j = hciout.expect(['LE Scan ...',pexpect.TIMEOUT], timeout=1)
                if j == 0:
                    ble_adrs = gatheradr(hciout)
                if j == 1:
                    'Dongle not plugged in.'
                    closeall(hciout)
            if inp.lower().startswith('n'):
                c = False 
                closeall(hciout)
            else:
                print 'Did not understand command. Try again.'
                c = True 
    if i == 2:
        print 'Could not scan: ', hciout.after
        closeall(hciout)
    return ble_adrs

        
if __name__ == "__main__":
    ble_adrs = blescan()
    if ble_adrs:
        print ble_adrs
    else:
        print 'No addresses found'
    



        #self.handle = 'b' #!! this is the TX service on the nRF8001 adafruit breakout with callbackEcho sketch
 #= int(sys.argv[1])

 #D1:DC:BF:25:3E:38 UART
 #D1:DC:BF:25:3E:38 (unknown)
