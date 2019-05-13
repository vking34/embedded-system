import sys
import socketio
import json

sio = socketio.Client()

# Change this base on host ip network address 
host = '192.168.1.188'

robot = {}
robot['id'] = sys.argv[1]   # unique robot id
robot['direction'] = 0  # 4 directions
robot['x'] = 0
robot['y'] = 0  
robot['status'] = 0 # 0 is not busy, 1 is busy

is_fake = sys.argv[2]


if is_fake == 'fake':
    from fake_take_action import command_robot
else:
    from take_action import command_robot


def get_robot_status():
    print(robot['status'])
    response_object = {
        'robot_id': robot['id'],
        'robot_direction': robot['direction'],
        'robot_x_pos': robot['x'],
        'robot_y_pos': robot['y'],
        'robot_status': robot['status'],
    }
    return response_object
    


@sio.on('connect')
def on_connect():
    print('connected to server')
    response_object = get_robot_status()
    sio.emit('robot_status', response_object)


@sio.on('disconnect')
def on_disconnect():
    print('disconnected to server')


@sio.on('server_command_robot')
def process_command(request):
    if robot['status'] == 0:
        # At first, notify all client that robot is busy
        robot['status'] = 1
        response_object = get_robot_status()
        sio.emit('robot_status', response_object)
        
        command = request.get('command')
        print(">>> command from server: ", command)
        direction, x_pos, y_pos = command_robot(command)
        
        # After finish, send robot status to client
        robot['status'] = 0
        response_object = get_robot_status()
        sio.emit('robot_status', response_object)


sio.connect('http://'+host+':5000')
sio.wait()