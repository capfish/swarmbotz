NUM_ROBOTS = 2
PORT_BTLE = 5207
PORT_SWISS = 3000
HOST_SWISS = 'localhost'
HOST_BTLE = '127.0.0.1'
# botID, rval, gval, bval, lservo, rservo
LENGTH_CMD_C = 4
#KILL_CMD = [0,0,0,90,90]
#Command format: botID, cmdType=10, rval, gval, bval
CMD_FORMAT ='botID, cmdType=10 or 20, lservo, rservo'
PREFIX_COLOR = 10 
PREFIX_SERVO = 20
LENGTH_CMD_C = 3+2 #1 for botid, 1 for cmdType 
LENGTH_CMD_S = 2+2
KILL_CMD_C = [PREFIX_COLOR] + [0,0,0]
KILL_CMD_S = [PREFIX_SERVO] + [90,90]
MAX_BTLE_CONNECTIONS = 2
