from time import sleep


def moveForward():
    print("move forward")
    sleep(1)
    

def moveBackward():
    print("move backward")
    sleep(1)
    

def turnLeft():
    print("turn left")
    sleep(1)
   

def turnRight():
    print("turn right")
    sleep(1)


def handUp():
    print("hand up")
    sleep(1)
    

def handDown():
    print("hand down")
    sleep(1)


def turn_degree(angle):
    print("turn degree ", angle)
    sleep(1)


def PIDControl():
    print("PID control")
    sleep(1)


def moveOutOfGreen():
    print("move out of green")
    sleep(1)


def command_robot(command):
    if command == "move_forward":
        moveOutOfGreen()
        PIDControl()
        return True
    if command == "move_backward":
        moveOutOfGreen()
        moveBackward()

        turn_degree(-92)    # turn left
        turn_degree(-92)    # turn left

        moveOutOfGreen()
        PIDControl()
        return True
    elif command == "move_left":
        moveOutOfGreen()
        moveBackward()
        
        turn_degree(-92)    # turn left

        moveOutOfGreen()
        PIDControl()
        return True
    elif command == "move_right":
        moveOutOfGreen()
        moveForward()

        turn_degree(87)       # turn right

        moveOutOfGreen()
        PIDControl()
        return True
    elif command == "pick":
        handUp()
    elif command == "drop":
        moveForward()
        handDown()
        moveBackward()
    elif command == "beep":
        # sound.beep()
        return True
    return False


print("ROBOT READYYYYYY !!!!")
print('version 3.0')