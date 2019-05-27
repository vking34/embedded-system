from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit, join_room, rooms
from auto import *
import cv2

host = '0.0.0.0'
port = 8080

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# global vars
status_dict = {}
manual_dict = {}
auto_dict = {}


#======================================================================
# Server get any connect or disconnect request, then update the online 
# list to client

@socketio.on('connect')
def connect():
    emit('server_update_status', status_dict, broadcast=True)
    print('connected')


@socketio.on('disconnect')
def disconnect():
    for room_id in status_dict.keys():
        if room_id in rooms():
            status_dict.pop(room_id)
            break

    print(rooms())   
    emit('server_update_status', status_dict, broadcast=True)
    print('disconnected')


# In auto mode, we have to initialize starting point, head point, and target point
# head point is the point right in front of robot
# in other word, the init direction of robot is starting point -> head point
@socketio.on('init_auto_points')
def init_auto_point(data):
    print(data)
    start_point = data.get('start_point')
    head_point = data.get('head_point')
    target_point = data.get('target_point')
    dest_point = data.get('dest_point')
    robot_id = data.get('robot_id')

    xy_start_point = start_point.split(',')
    x_start_point = int(xy_start_point[0])
    y_start_point = int(xy_start_point[1])

    xy_head_point = head_point.split(',')
    x_head_point = int(xy_head_point[0])
    y_head_point = int(xy_head_point[1])

    xy_target_point = target_point.split(',')
    x_target_point = int(xy_target_point[0])
    y_target_point = int(xy_target_point[1])

    xy_dest_point = dest_point.split(',')
    x_dest_point = int(xy_dest_point[0])
    y_dest_point = int(xy_dest_point[1])

    start_point = (x_start_point, y_start_point)
    head_point = (x_head_point, y_head_point)
    target_point = (x_target_point, y_target_point)
    dest_point = (x_dest_point, y_dest_point)

    status_dict[robot_id] = {
        'robot_x_pos': x_start_point,
        'robot_y_pos': y_start_point,
        'robot_status': 1
    }

    emit('server_update_status', status_dict, broadcast=True)

    # global current_index, path, command_list

    print('start point: ' + str(start_point))
    print('head point: ' + str(head_point))
    command_list, path = run(start_point, head_point, target_point, dest_point)
    current_index = 0
    auto_dict[robot_id] = {
        'command_list': command_list,
        'path': path,
        'current_index': current_index,
        'is_picking': False,
        'is_finished': False
    }

    print(command_list)
    print(path)
    print('command robot: ' + str(command_list[current_index]))
    command_robot_auto(command_list[current_index], path[current_index+1], robot_id)


@socketio.on('init_manual_points')
def init_manual_point(data):
    print(data)
    start_point = data.get('start_point')
    head_point = data.get('head_point')
    robot_id = data.get('robot_id')

    xy_start_point = start_point.split(',')
    x_start_point = int(xy_start_point[0])
    y_start_point = int(xy_start_point[1])

    xy_head_point = head_point.split(',')
    x_head_point = int(xy_head_point[0])
    y_head_point = int(xy_head_point[1])

    payload = {
        'x_start_point': x_start_point,
        'y_start_point': y_start_point
    }

    emit('init_robot', payload, room=robot_id)

    start_point = (x_start_point, y_start_point)
    head_point = (x_head_point, y_head_point)

    manual_dict[robot_id] = {
        'start_point': start_point,
        'head_point': head_point
    }

    status_dict[robot_id]['robot_x_pos'] = x_start_point
    status_dict[robot_id]['robot_y_pos'] = y_start_point

    emit('server_update_status', status_dict, broadcast=True)


# Server take request from client
@socketio.on('client_command')
def client_command(request):
    print('client command')
    robot_id = request.get('robot_id')
    commands = request.get('commands')
    print(request)
    command_robot_manual(commands, robot_id)


# for auto control
def command_robot_auto(commands, next_point, robot_id):
    payload = {
        'commands': commands,
        'next_point': next_point
    }
    print(payload)
    emit('server_command_robot', payload, room=robot_id)


# Server process the request from client and then send command to robot
def command_robot_manual(commands, robot_id):
    start_point = manual_dict[robot_id].get('start_point')
    head_point = manual_dict[robot_id].get('head_point')
    command = commands[0]
    next_point, new_head_point = get_next_point(start_point, head_point, command)

    payload = {
        'commands': commands,
        'next_point': next_point
    }
    print(payload)
    emit('server_command_robot', payload, room=robot_id)

    manual_dict[robot_id]['start_point'] = next_point
    manual_dict[robot_id]['head_point'] = new_head_point


# Server take request from robot
@socketio.on('robot_status')
def robot_update_status(request):
    # global current_index, path, command_list, is_picking, is_finished

    robot_id = request.get('robot_id')
    # robot_direction = request.get('robot_direction')
    robot_x_pos = request.get('robot_x_pos')
    robot_y_pos = request.get('robot_y_pos')
    robot_status = request.get('robot_status')

    # Update the onlines dict and return to client
    join_room(robot_id)

    status_dict[robot_id] = {
        'robot_x_pos': robot_x_pos,
        'robot_y_pos': robot_y_pos,
        'robot_status': robot_status
    }
    print('robot: ', status_dict[robot_id])

    # print('current point: ' + str((robot_x_pos, robot_y_pos)))

    emit('server_update_status', status_dict, broadcast=True)

    try:
        robot = auto_dict[robot_id]
    except KeyError:
        return

    current_index = auto_dict[robot_id]['current_index']
    command_list = auto_dict[robot_id]['command_list']
    path = auto_dict[robot_id]['path']
    is_picking = auto_dict[robot_id]['is_picking']
    is_finished = auto_dict[robot_id]['is_finished']

    # When robot stop, command robot to go on
    if robot_status == 0:
        # not reach the destination yet
        path_length = len(path)
        if current_index < path_length - 1:
            current_index += 1
            auto_dict[robot_id]['current_index'] = current_index

            try:

                next_point = path[current_index+1]
            except IndexError:
                next_point = path[current_index]

            try:
                command = command_list[current_index]
                command_robot_auto(command, next_point, robot_id)
            except IndexError:
                return

        # robot reached the destination and picking the object
        elif current_index == path_length - 1:
            current_index += 1
            auto_dict[robot_id]['current_index'] = current_index
            print('robot' + robot_id + ' reached destination')

            # is_picking is True, robot has just dropped the object
            if is_picking is False:
                commands = ['pick']
                is_picking = True
                auto_dict[robot_id]['is_picking'] = is_picking
                command_robot_auto(commands, path[current_index - 2], robot_id)

        # robot picked object and come back
        elif current_index == path_length:
            if is_finished is False:
                current_index = 0
                auto_dict[robot_id]['current_index'] = current_index
                path_length = len(path)
                head_point = get_head_point(path[path_length - 1])
                command_list, path = run(path[path_length-1], head_point, path[0])
                command_list.append(['drop'])
                auto_dict[robot_id]['command_list'] = command_list
                auto_dict[robot_id]['path'] = path
                print(command_list)
                print(path)
                command_robot_auto(command_list[current_index], path[current_index + 1], robot_id)

#=======================================================================


def generate_frame():
    # for external camera app
    # camera_ip = '192.168.137.181'
    # cap = cv2.VideoCapture('http://' + camera_ip + ':8080/video')

    # for webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (600, 400))

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    socketio.run(app, host=host, port=port, debug=True)