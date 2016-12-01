get_input_for_day = lambda day: open('inputs/day_%s_input.txt' % str(day))
part_2 = False


def day_1():
    x = 0
    y = 0
    locations = set()

    facing = "N"
    facing_to_incrementation = {
        "N": 1,
        "E": 1,
        "S": -1,
        "W": -1
    }
    facing_to_axis = {
        "N": "y",
        "E": "x",
        "S": "y",
        "W": "x"
    }
    rotate_facing_right = {
        "N": "E",
        "E": "S",
        "S": "W",
        "W": "N"
    }
    rotate_facing_left = {
        "N": "W",
        "E": "N",
        "S": "E",
        "W": "S"
    }

    input_line = get_input_for_day(1).readline()
    for instruction in input_line.split(','):
        instruction = instruction.strip()
        rotation = instruction[0]
        distance = int(instruction[1:])

        if rotation == "R":
            facing = rotate_facing_right[facing]
        else:
            facing = rotate_facing_left[facing]

        for _ in xrange(distance):
            command = "{axis} += {incrementation}".format(
                axis=facing_to_axis[facing],
                incrementation=facing_to_incrementation[facing]
            )
            exec command
            if part_2 and (x, y) in locations:
                return abs(x) + abs(y)
            locations.add((x, y))

    total_dist = abs(x) + abs(y)
    return total_dist

if __name__ == '__main__':
    for day in xrange(1, 26):
        if 'day_%s' % day in dir():
            print 'Day %s:' % day
            part_2 = False
            print ' Part 1:', eval('day_%s()' % day)
            part_2 = True
            print ' Part 2:', eval('day_%s()' % day)
