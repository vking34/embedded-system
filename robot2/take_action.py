from ev3dev2.motor import MoveTank,MoveSteering, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.sound import Sound

from time import sleep

# Initial Motor
tank_pair = MoveTank(OUTPUT_A, OUTPUT_D)
motor1 = Motor(OUTPUT_A)
motor2 = Motor(OUTPUT_B)
steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D)
motor = Motor(OUTPUT_B) # small motor

# Initial sound
sound = Sound()

# Initial Sensor
color = ColorSensor()
gyro = GyroSensor()
# gyro.mode = 

def is_green(red, green, blue):
    return red in range(0, 150) and green in range(150, 256) and blue in range(0, 150)


def moveForward(time):
    print("move forward")
    tank_pair.on(left_speed=20, right_speed=20)
    sleep(time)
    tank_pair.off(brake=True)
    

def moveBackward(time):
    print("move backward")
    tank_pair.on(left_speed=-20, right_speed=-20)
    sleep(time)
    tank_pair.off(brake=True)
    

def turnLeft(time):
    print("turn left")
    tank_pair.on(left_speed=-20, right_speed=20)
    sleep(time)
    tank_pair.off(brake=True)
   

def turnRight(time):
    print("turn right")
    tank_pair.on(left_speed=20, right_speed=-20)
    sleep(time)
    tank_pair.off(brake=True)


def handUp(time):
    print("hand up")
    motor.on(speed=10)
    sleep(time)
    motor.off(brake=True)
    

def handDown(time):
    print("hand down")
    motor.on(speed=-10)
    sleep(time)
    motor.off(brake=True)
    

def turn_degree(angle):
    past_gyro = gyro.angle
    ki = 0.5
    max_speed=30

    while True:
        current_gyro = gyro.angle
        changed_angle = current_gyro - past_gyro
        # print(changed_angle)

        error = angle - changed_angle
        if error == 0:
            tank_pair.off(brake=True)
            break

        pid = ki * error
        if pid > max_speed:
            speed = max_speed
        elif pid < max_speed*-1:
            speed = max_speed*-1
        else:
            speed = pid

        tank_pair.on(left_speed=speed, right_speed=speed*-1)


def PIDControl():
    expectation_red = 80
    last_error = 0
    kp = 0.09
    ki = 0
    base_speed = 20
    max_speed = 30

    # default = input("use default: ")
    # if default == 'y':
    #     pass
    # else:
    #     kp = float(input("enter p: "))
    #     ki = float(input("enter i: "))
    #     base_speed = int(input("enter base_speed: "))
    #     max_speed = int(input("enter max_speed: "))

    while True:
        red = color.rgb[0]
        green = color.rgb[1]
        blue = color.rgb[2]
        # print(red, green, blue)

        # Stop if robot enter green area
        if is_green(red, green, blue):
            print('STOP !!!')
            tank_pair.off(brake=True)
            break

        # Stop if color sensor display no color
        # if red == 0:
        #     print('STOP !!!')
        #     tank_pair.off(brake=False)
        #     break
        
        # Calculate for error parameters
        error = red - expectation_red
        if error < 0:
            error = error * 2
        delta_error = error - last_error

        last_error = error

        if error > 100:
            error = 100
        elif error < -100:
            error = -100

        # Calculate pid
        pid = kp * error + ki * delta_error
        
        # Calculate left speed and right speed of motor based on pid
        left_speed = max(0, min(base_speed + pid, max_speed))
        right_speed = max(0, min(base_speed - pid, max_speed))

        tank_pair.on(left_speed=left_speed, right_speed=right_speed)


def moveOutOfGreen():
    while True:
        red = color.rgb[0]
        green = color.rgb[1]
        blue = color.rgb[2]

        if is_green(red, green, blue):
            tank_pair.on(left_speed=20, right_speed=20)
        else:
            print('STOP !!!')
            tank_pair.off(brake=True)
            break


def displayColor():
    red = color.rgb[0]
    green = color.rgb[1]
    blue = color.rgb[2]
    print("Red: " + str(red) + ", Green: " + str(green) + ", Blue: " + str(blue))
    print("Color: " + color.color_name)


def displayAngle():
    print("Angle: " + str(gyro.angle))


def command_robot(command):
    sound.beep()
    if command == "move_forward":
        moveOutOfGreen()
        PIDControl()
        return True
    if command == "move_backward":
        moveOutOfGreen()
        moveBackward(0.1)

        turn_degree(-187)

        moveOutOfGreen()
        PIDControl()
        return True
    elif command == "pick":
        moveOutOfGreen()
        moveForward(1)
        handUp(0.5)
        moveBackward(1)

        turn_degree(-187)
        return True

    elif command == "drop":
        moveOutOfGreen()
        moveForward(1)
        handDown(0.5)
        moveBackward(1)

        turn_degree(-187)
        return True

    elif command == "beep":
        # sound.beep()
        return True

    elif command == "turn_left":
        moveOutOfGreen()
        # moveBackward(0.15)
        
        turn_degree(-92)    # turn left

        return True

    elif command == "turn_right":
        moveOutOfGreen()
        # moveBackward(0.05)

        turn_degree(88)       # turn right

        return True

    elif command == "move_left":
        moveOutOfGreen()
        # moveBackward(0.1)
        
        turn_degree(-92)    # turn left

        moveOutOfGreen()
        PIDControl()
        return True

    elif command == "move_right":
        moveOutOfGreen()
        # moveBackward(0.2)

        turn_degree(87)       # turn right

        moveOutOfGreen()
        PIDControl()
        return True

    return False


sound.beep()
print("ROBOT READYYYYYY !!!!")
print('version 3.0')