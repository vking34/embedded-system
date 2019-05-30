import sys
import socketio
from time import sleep

sio = socketio.Client()

# Change this base on host ip network address 
host = '192.168.1.245'
port = '8080'
print(host + ':' + port)

robot = {}
robot['id'] = sys.argv[1]  # unique robot id
# robot['direction'] = 0  # 4 directions
robot['x'] = 0
robot['y'] = 0
robot['status'] = 0  # 0 is not busy, 1 is busy

is_fake = sys.argv[2]

if is_fake == 'fake':
    from fake_take_action import command_robot
else:
    from take_action import command_robot


def get_robot_status():
    # print(robot['status'])
    response_object = {
        'robot_id': robot['id'],
        'robot_x_pos': robot['x'],
        'robot_y_pos': robot['y'],
        'robot_status': robot['status']
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


@sio.on('init_robot')
def init_robot(data):
    print('init robot...')
    robot['x'] = data.get('x_start_point')
    robot['y'] = data.get('y_start_point')
    response_object = get_robot_status()
    # sio.emit('robot_status', response_object)


@sio.on('server_command_robot')
def process_command(request):
    print('command from server: ', request.get('commands'))
    if robot['status'] == 0:
        # receive commands and move
        robot['status'] = 1
        response_object = get_robot_status()
        sio.emit('robot_status', response_object)

        commands = request.get('commands')
        print(">>> command from server: ", commands)

        for command in commands:
            command_robot(command)

        # After finish, send robot status to client

        next_point = request.get('next_point')
        robot['x'] = next_point[0]
        robot['y'] = next_point[1]

        robot['status'] = 0
        response_object = get_robot_status()
        sio.emit('robot_status', response_object)


sio.connect('http://' + host + ':' + port)
sio.wait()