from astar import astar

maze = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]] # 4x6


class directions:
    WEST = 'west'
    EAST = 'east'
    NORTH = 'north'
    SOUTH = 'south'
# each point is stored as (x, y)
def get_direction(current_point, next_point):
    if current_point[0] == next_point[0] and current_point[1] > next_point[1]:
        return directions.WEST
    if current_point[0] == next_point[0] and current_point[1] < next_point[1]:
        return directions.EAST
    if current_point[0] > next_point[0] and next_point[1] == current_point[1]:
        return directions.NORTH
    if current_point[0] < next_point[0] and next_point[1] == current_point[1]:
        return directions.SOUTH

def get_command(current_direction, next_direction):
    command = []
    turn_left_combinations = [(directions.NORTH, directions.WEST), (directions.WEST, directions.SOUTH), \
        (directions.SOUTH, directions.EAST), (directions.EAST, directions.NORTH)]
    turn_right_combinations = [(directions.NORTH, directions.EAST), (directions.EAST, directions.SOUTH),\
        (directions.SOUTH, directions.WEST), (directions.WEST, directions.NORTH)]
    go_straight_combinations = [(directions.EAST,directions.EAST), (directions.SOUTH,directions.SOUTH), \
        (directions.NORTH, directions.NORTH), (directions.WEST, directions.WEST)]
    go_backward_combinations = [(directions.NORTH, directions.SOUTH), (directions.SOUTH, directions.NORTH), \
        (directions.WEST, directions.EAST), (directions.EAST, directions.WEST)]

    if (current_direction, next_direction) in turn_left_combinations:
        command = ['turn_left', 'move_forward']
    elif (current_direction, next_direction) in turn_right_combinations:
        command = ['turn_right', 'move_forward']
    elif (current_direction, next_direction) in go_straight_combinations:
        command = ['move_forward']
    elif (current_direction, next_direction) in go_backward_combinations:
        command = ['move_backward']
    return command

def get_path(starting_point, destination_point): # path must follow the line ( no diagonal )
    astar_path = astar(maze, starting_point, destination_point)
    # print(astar_path)
    i = 0
    point = astar_path[i]
    next_point = astar_path[i + 1]
    while next_point is not None:

        if point[0] != next_point[0] and point[1] != next_point[1]:
            astar_path.insert(i+1, (point[0], next_point[1]))

        i += 1
        try:
            point = astar_path[i]
            next_point = astar_path[i + 1]

        except IndexError:
            break
    return astar_path

def run(starting_point, starting_headto_point, destination_point):
    command_list = []
    initial_direction = get_direction(starting_point, starting_headto_point)
    path = get_path(starting_point, destination_point)
    current_direction = initial_direction
    for i in range(0, len(path)):
        current_point = path[i]
        if i < len(path)-1:
            next_point = path[i+1]
        else:
            break
        next_direction = get_direction(current_point, next_point)
        # print('next direction is: %s' %next_direction)
        command = get_command(current_direction, next_direction)
        command_list.append(command)
        headto_point = ()
        if next_point[0] > current_point[0]:
            headto_point_x = next_point[0] + 1
            headto_point_y = next_point[1]
            headto_point = (headto_point_x, headto_point_y)
        elif next_point[0] < current_point[0]:
            headto_point_x = next_point[0] - 1
            headto_point_y = next_point[1]
            headto_point = (headto_point_x, headto_point_y)
        elif next_point[1] > current_point[1]:
            headto_point_y = next_point[1] + 1
            headto_point_x = next_point[0]
            headto_point = (headto_point_x, headto_point_y)
        elif next_point[1] < current_point[1]:
            headto_point_y = next_point[1] - 1
            headto_point_x = next_point[0]
            headto_point = (headto_point_x, headto_point_y)
        # print('head to point is: %s' % (headto_point,))
        current_direction = get_direction(next_point, headto_point)
        # print('current direction is: %s', current_direction)
    # for i in range(0,len(command_list)):
    #     if command_list[i] == ['move_backward']: # move backward == turn 180 degree so need to add this
    #         if command_list[i+1] == ['turn_left', 'move_forward']:
    #             command_list[i+1] = ['turn_right', 'move_forward']
    #         elif command_list[i+1] == ['turn_right', 'move_forward']:
    #             command_list[i+1] = ['turn_left', 'move_forward']

    if destination_point[0] == 0: # direction when arrives need to be NORTH
        if current_direction == directions.EAST:
            command_list.append(['turn_left'])
        elif current_direction == directions.WEST:
            command_list.append(['turn_right'])
    elif destination_point[0] == 5: # direction when arrives need to be SOUTH
        if current_direction == directions.EAST:
            command_list.append(['turn_right'])
        elif current_direction == directions.WEST:
            command_list.append(['turn_left'])
    elif destination_point[1] == 3: # direction when arrives need to be EAST
        if current_direction == directions.NORTH:
            command_list.append(['turn_right'])
        elif current_direction == directions.SOUTH:
            command_list.append(['turn_left'])
    elif destination_point[1] == 0: # direction when arrives need to be WEST
        if current_direction == directions.NORTH:
            command_list.append(['turn_left'])
        elif current_direction == directions.SOUTH:
            command_list.append(['turn_right'])

    return command_list, path


def get_head_point(start_point):
    if start_point[0] == 0:
        head_point = (start_point[0] + 1, start_point[1])
    elif start_point[0] == 5:
        head_point = (start_point[0] - 1, start_point[1])
    elif start_point[1] == 0:
        head_point = (start_point[0], start_point[1] + 1)
    elif start_point[1] == 3:
        head_point = (start_point[0], start_point[1] - 1)
    else:
        x = start_point[0] - 1
        if x >= 0:
            head_point = (x, start_point[0])
        else:
            head_point = (x+ 2, start_point[0])

    return head_point


def get_next_point(start_point, head_point, command):
    if command == 'turn_left' and start_point[0] == head_point[0] and start_point[1] > head_point[1]:
        next_point = (start_point[0] + 1, start_point[1])
        new_head_point = (start_point[0] + 2, start_point[1])
    elif command == 'turn_left' and start_point[0] == head_point[0] and start_point[1] < head_point[1]:
        next_point = (start_point[0] - 1, start_point[1])
        new_head_point = (start_point[0] - 2, start_point[1])
    elif command == 'turn_left' and start_point[1] == head_point[1] and start_point[0] < head_point[0]:
        next_point = (start_point[0], start_point[1] + 1)
        new_head_point = (start_point[0], start_point[1] + 2)
    elif command == 'turn_left' and start_point[1] == head_point[1] and start_point[0] > head_point[0]:
        next_point = (start_point[0], start_point[1] - 1)
        new_head_point = (start_point[0], start_point[1] - 2)
    elif command == 'turn_right' and start_point[0] == head_point[0] and start_point[1] > head_point[1]:
        next_point = (start_point[0] - 1, start_point[1])
        new_head_point = (start_point[0] - 2, start_point[1])
    elif command == 'turn_right' and start_point[0] == head_point[0] and start_point[1] < head_point[1]:
        next_point = (start_point[0] + 1, start_point[1])
        new_head_point = (start_point[0] + 2, start_point[1])
    elif command == 'turn_right' and start_point[1] == head_point[1] and start_point[0] < head_point[0]:
        next_point = (start_point[0], start_point[1] - 1)
        new_head_point = (start_point[0], start_point[1] - 2)
    elif command == 'turn_right' and start_point[1] == head_point[1] and start_point[0] > head_point[0]:
        next_point = (start_point[0], start_point[1] + 1)
        new_head_point = (start_point[0], start_point[1] + 2)
    elif command == 'move_backward' and start_point[0] == head_point[0] and start_point[1] > head_point[1]:
        next_point = (start_point[0], start_point[1] + 1)
        new_head_point = (start_point[0], start_point[1] + 2)
    elif command == 'move_backward' and start_point[0] == head_point[0] and start_point[1] < head_point[1]:
        next_point = (start_point[0], start_point[1] - 1)
        new_head_point = (start_point[0], start_point[1] - 2)
    elif command == 'move_backward' and start_point[1] == head_point[1] and start_point[0] < head_point[0]:
        next_point = (start_point[0] - 1, start_point[1])
        new_head_point = (start_point[0] - 2, start_point[1])
    elif command == 'move_backward' and start_point[1] == head_point[1] and start_point[0] > head_point[0]:
        next_point = (start_point[0] + 1, start_point[1])
        new_head_point = (start_point[0] + 2, start_point[1])
    elif command == 'move_forward' and start_point[0] == head_point[0] and start_point[1] > head_point[1]:
        next_point = (start_point[0], start_point[1] - 1)
        new_head_point = (start_point[0], start_point[1] - 2)
    elif command == 'move_forward' and start_point[0] == head_point[0] and start_point[1] < head_point[1]:
        next_point = (start_point[0], start_point[1] + 1)
        new_head_point = (start_point[0], start_point[1] + 2)
    elif command == 'move_forward' and start_point[1] == head_point[1] and start_point[0] < head_point[0]:
        next_point = (start_point[0] + 1, start_point[1])
        new_head_point = (start_point[0] + 2, start_point[1])
    elif command == 'move_forward' and start_point[1] == head_point[1] and start_point[0] > head_point[0]:
        next_point = (start_point[0] - 1, start_point[1])
        new_head_point = (start_point[0] - 2, start_point[1])
    elif command == 'pick':
        next_point = start_point
        new_head_point = get_head_point(start_point)
    else:
        next_point = start_point
        new_head_point = head_point

    return next_point, new_head_point

def main():
    starting_point = (0, 0)
    starting_headto_point = (0, 1)
    # next_point, new_head_point = get_next_point(starting_point, starting_headto_point, 'move_forward')
    # print(next_point)
    # print(new_head_point)

    destination_point = (3, 3)
    # # check validation of destination point
    # if not destination_point[0] in [0, 5] and not destination_point[1] in [0, 3]:
    #     print('invalid destination point.')
    #     return
    #
    command_list, path = run(starting_point, starting_headto_point, destination_point)
    print(command_list)
    print(path)


if __name__ == '__main__':
    main()

