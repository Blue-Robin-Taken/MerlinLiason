from flask_socketio import ConnectionRefusedError
socketCount = 150
allocatedMem = 10
def memCheck():
    if socketCount*70> allocatedMem*1000 - 10:
        print(f"memory close to being exceeded refusing connection for ")
        print(allocatedMem*1000 -10,socketCount*70)
        return True
    else:
        print("safe amount of memory is being used")
        return False
memCheck()
if memCheck():
    print("yes")
else:
    print("no")