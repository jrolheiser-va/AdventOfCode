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


def day_2():
    input_file = get_input_for_day(2)

    x = 1
    y = 1
    input_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    if part_2:
        x = 0
        y = 2
        input_matrix = [
            [0, 0, 1, 0, 0],
            [0, 2, 3, 4, 0],
            [5, 6, 7, 8, 9],
            [0, 'A', 'B', 'C', 0],
            [0, 0, 'D', 0, 0],
        ]

    moves = []
    for line in input_file:
        for char in line:
            if char == "U":
                if not part_2 or (y-1 > -1 and input_matrix[y-1][x] != 0):
                    y = max(y-1, 0)
            if char == "D":
                if not part_2 or (y+1 < len(input_matrix) and input_matrix[y+1][x] != 0):
                    y = min(y+1, len(input_matrix)-1)
            if char == "L":
                if not part_2 or (x-1 > -1 and input_matrix[y][x-1] != 0):
                    x = max(x-1, 0)
            if char == "R":
                if not part_2 or (x+1 < len(input_matrix) and input_matrix[y][x+1] != 0):
                    x = min(x+1, len(input_matrix)-1)
        moves.append(input_matrix[y][x])
    return "".join(str(move) for move in moves)


def day_3():
    input_file = get_input_for_day(3)
    count = 0
    row = 0
    triangles = [
        [],
        [],
        []
    ]
    for line in input_file:
        nums = [piece for piece in line.strip().split(" ") if piece]
        first = int(nums[0])
        second = int(nums[1])
        third = int(nums[2])
        if not part_2:
            if first + second > third and first + third > second and second + third > first:
                count += 1
        else:
            row += 1
            triangles[0].append(first)
            triangles[1].append(second)
            triangles[2].append(third)
            if row % 3 == 0:
                if triangles[0][0] + triangles[0][1] > triangles[0][2] \
                        and triangles[0][0] + triangles[0][2] > triangles[0][1] \
                        and triangles[0][1] + triangles[0][2] > triangles[0][0]:
                    count += 1
                if triangles[1][0] + triangles[1][1] > triangles[1][2] \
                        and triangles[1][0] + triangles[1][2] > triangles[1][1] \
                        and triangles[1][1] + triangles[1][2] > triangles[1][0]:
                    count += 1
                if triangles[2][0] + triangles[2][1] > triangles[2][2] \
                        and triangles[2][0] + triangles[2][2] > triangles[2][1] \
                        and triangles[2][1] + triangles[2][2] > triangles[2][0]:
                    count += 1
                triangles[0] = []
                triangles[1] = []
                triangles[2] = []
    return count


def day_4():
    def cmp_char_counts(x, y):
        diff = (x[1] < y[1]) - (x[1] > y[1])
        if diff == 0:
            diff = (ord(x[0]) > ord(y[0])) - (ord(x[0]) < ord(y[0]))
        return diff

    input_file = get_input_for_day(4)
    count = 0
    for line in input_file:
        pieces = line.strip().rstrip("]").split("[")
        name = pieces[0].rstrip("-1234567890")
        sector_id = int(pieces[0].split("-")[-1])
        checksum = pieces[1]
        char_counts = {}
        for char in name:
            if char != "-":
                char_counts[char] = name.count(char)
        most_commons = sorted(char_counts.items(), cmp=cmp_char_counts)[:len(checksum)]
        if all(most_common[0] in checksum for most_common in most_commons):
            count += sector_id
            if part_2:
                unencrypted_string = ""
                for char in name:
                    if char == "-":
                        unencrypted_string += " "
                    else:
                        normalized_ord = ord(char) % 97
                        rotated_ord = (normalized_ord + sector_id) % 26
                        unencrypted_string += chr(rotated_ord + 97)
                if unencrypted_string == "northpole object storage":
                    return sector_id

    return count


def day_5():
    from hashlib import md5

    input_line = get_input_for_day(5).readline()
    counter = 0
    door_id = []
    if part_2:
        door_id = [None] * 8
    while len(door_id) < 8 or (part_2 and any(id_piece is None for id_piece in door_id)):
        next_hash = md5(input_line + str(counter)).hexdigest()
        if next_hash.startswith("00000"):
            if not part_2:
                door_id.append(next_hash[5])
            else:
                position = next_hash[5]
                if not position.isalpha() and int(position) < 8:
                    if door_id[int(position)] is None:
                        door_id[int(position)] = next_hash[6]
        counter += 1
    return ''.join(door_id)


def day_6():
    input_line = get_input_for_day(6)
    string_holders = [""] * 8
    for line in input_line:
        for ind, char in enumerate(line.strip()):
            string_holders[ind] += char
    commons = []
    from collections import Counter
    for string_holder in string_holders:
        most_common = Counter(string_holder).most_common()
        if not part_2:
            commons.append(most_common[0])
        else:
            commons.append(most_common[-1])
    return "".join(common[0] for common in commons)


def day_7():
    input_file = get_input_for_day(7)
    count = 0
    for line in input_file:
        opening = False
        could_be_valid = False
        bab_blocks = []
        aba_blocks = []
        for index, char in enumerate(line[:-3]):
            if not part_2:
                if char is "[":
                    opening = True
                    continue
                if char is "]":
                    opening = False
                    continue
                if opening and char == line[index + 3] and line[index + 1] == line[index + 2] and char != line[index+1]:
                    could_be_valid = False
                    break
                if not opening and char == line[index + 3] and line[index + 1] == line[index + 2] and char != line[index+1]:
                    could_be_valid = True
            else:
                if char is "[":
                    opening = True
                    continue
                if char is "]":
                    opening = False
                    continue
                if opening and char == line[index+2]:
                    bab_blocks.append(line[index+1] + char + line[index+1])
                if not opening and char == line[index+2]:
                    aba_blocks.append(line[index+1] + char + line[index+1])
                if opening and (char + line[index+1] + line[index+2]) in aba_blocks:
                    count += 1
                    break
                if not opening and (char + line[index + 1] + line[index + 2]) in bab_blocks:
                    count += 1
                    break
        if could_be_valid:
            count += 1
    return count


def day_8():
    input_file = get_input_for_day(8)
    display = [
        ["."] * 50,
        ["."] * 50,
        ["."] * 50,
        ["."] * 50,
        ["."] * 50,
        ["."] * 50
    ]
    for line in input_file:
        if 'rect' in line:
            nums = line.split(' ')[1]
            nums = nums.split('x')
            x = int(nums[0])
            y = int(nums[1])
            for row, row_data in enumerate(display):
                for col, col_data in enumerate(row_data):
                    if y > row and x > col:
                        display[row][col] = "#"
        if 'rotate' in line:
            if 'row' in line:
                pieces = line.split(' ')
                row = int(pieces[2].lstrip('y='))
                rotation = int(pieces[4])
                on_spots = []
                for col, spot in enumerate(display[row]):
                    if spot == "#":
                        display[row][col] = "."
                        on_spots.append(col)
                on_spots = map(lambda x: (x + rotation) % 50, on_spots)
                for col, _ in enumerate(display[row]):
                    if col in on_spots:
                        display[row][col] = "#"
            if 'column' in line:
                pieces = line.split(' ')
                col = int(pieces[2].lstrip('x='))
                rotation = int(pieces[4])
                on_spots = []
                for row, _ in enumerate(display):
                    if display[row][col] == "#":
                        display[row][col] = "."
                        on_spots.append(row)
                on_spots = map(lambda x: (x + rotation) % 6, on_spots)
                for row, _ in enumerate(display):
                    if row in on_spots:
                        display[row][col] = "#"

    count = 0
    for row in display:
        count += row.count("#")
        print " ".join(row)
    return count


def day_9():
    input_line = get_input_for_day(9).readline()
    if not part_2:
        open_index = 0
        full_string = ""
        pass_index = -1
        opening = False
        for index, char in enumerate(input_line):
            if char is "(" and index > pass_index:
                opening = True
                open_index = index
            elif char is ")" and index > pass_index:
                opening = False
                close_index = index
                marker = input_line[open_index+1:close_index]
                pieces = marker.split('x')
                num_chars = int(pieces[0])
                repeat = int(pieces[1])
                chars = input_line[close_index+1:close_index+num_chars+1]
                full_string += (repeat - 1) * chars
                pass_index = close_index + num_chars
            elif not opening:
                full_string += char
        return len(full_string)
    else:
        def count_line(line):
            open_index = 0
            opening = False
            count = 0
            for index, char in enumerate(line):
                if char is "(":
                    opening = True
                    open_index = index
                elif char is ")":
                    opening = False
                    close_index = index
                    marker = line[open_index + 1:close_index]
                    pieces = marker.split('x')
                    num_chars = int(pieces[0])
                    repeat = int(pieces[1])
                    chars = line[close_index + 1:close_index + num_chars + 1]
                    count += (repeat - 1) * count_line(chars)
                elif not opening:
                    count += 1
            return count

        return count_line(input_line)


def day_10():
    from collections import defaultdict
    input_file = get_input_for_day(10)

    bots = defaultdict(lambda: {
        'value': [],
        'low_target': '',
        'low_index': '',
        'high_target': '',
        'high_index': ''
    })

    outputs = defaultdict(list)

    for line in input_file:
        if line.startswith('value'):
            pieces = line.split(' ')
            value = int(pieces[1])
            bot = int(pieces[5])
            bots[bot]['value'].append(value)
        if line.startswith('bot'):
            pieces = line.split(' ')
            this_bot = int(pieces[1])
            low_target = pieces[5]
            low_index = int(pieces[6])
            high_target = pieces[10]
            high_index = int(pieces[11])
            bots[this_bot]['low_target'] = low_target
            bots[this_bot]['low_index'] = low_index
            bots[this_bot]['high_target'] = high_target
            bots[this_bot]['high_index'] = high_index
    while any(len(bots[bot]['value']) > 1 for bot in bots):
        for bot in bots:
            if len(bots[bot]['value']) > 1:
                if not part_2 and sorted(bots[bot]['value']) == [17, 61]:
                    return bot
                if bots[bot]['high_target'] == 'bot':
                    bots[bots[bot]['high_index']]['value'].append(max(bots[bot]['value']))
                else:
                    outputs[bots[bot]['high_index']].append(max(bots[bot]['value']))

                if bots[bot]['low_target'] == 'bot':
                    bots[bots[bot]['low_index']]['value'].append(min(bots[bot]['value']))
                else:
                    outputs[bots[bot]['low_index']].append(min(bots[bot]['value']))
                bots[bot]['value'] = []

    return outputs[0][0] * outputs[1][0] * outputs[2][0]


def day_12():
    input_file = get_input_for_day(12)
    a = b = c = d = 0
    instructions = []
    if part_2:
        instructions.append("cpy 1 c")
    for line in input_file:
        instructions.append(line.strip())
    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        if instruction.startswith('cpy'):
            pieces = instruction.split(' ')
            try:
                value = int(pieces[1])
            except:
                value = pieces[1]
            command = "{register} = {value}".format(
                register=pieces[2],
                value=value
            )
            exec command
        elif instruction.startswith('inc'):
            pieces = instruction.split(' ')
            command = "{register} += 1".format(
                register=pieces[1]
            )
            exec command
        elif instruction.startswith('dec'):
            pieces = instruction.split(' ')
            command = "{register} -= 1".format(
                register=pieces[1]
            )
            exec command
        made_jump = False
        if instruction.startswith('jnz'):
            pieces = instruction.split(' ')
            if eval(pieces[1]) != 0:
                made_jump = True
                i += int(pieces[2])
        if not made_jump:
            i += 1
    return a


def bfs(graph, start, end, depth=1000):
    queue = list()
    queue.append([start])
    visited_locations = set()
    visited_locations.add((start[0], start[1]))
    while queue:
        path = queue.pop(0)
        tail = path[-1]
        if tail == end:
            return path
        for direction in ['up', 'down', 'left', 'right']:
            next_step = [tail[0], tail[1]]
            if direction == 'up':
                next_step[1] -= 1
            if direction == 'down':
                next_step[1] += 1
            if direction == 'left':
                next_step[0] -= 1
            if direction == 'right':
                next_step[0] += 1
            if 0 <= next_step[0] < len(graph) and 0 <= next_step[1] < len(graph):
                if graph[next_step[1]][next_step[0]] != "#":
                    if next_step not in path:
                        visited_locations.add((next_step[0], next_step[1]))
                        next_path = list(path)
                        next_path.append(next_step)
                        if len(next_path) <= depth:
                            queue.append(next_path)
    return visited_locations


def day_13():
    input_number = int(get_input_for_day(13).readline())
    target = [31, 39]
    formula = lambda x, y: x*x + 3*x + 2*x*y + y + y*y + input_number
    num_1_bits = lambda x, y: bin(formula(x, y)).count('1')
    maze = []
    for y in xrange(100):
        row = []
        for x in xrange(100):
            if num_1_bits(x, y) % 2 == 0:
                row.append(' ')
            else:
                row.append('#')
        maze.append(row)
    if not part_2:
        path = bfs(maze, [1, 1], target)
        return len(path) - 1
    else:
        path = bfs(maze, [1, 1], [100, 100], depth=50)
        return len(path)


def day_14():
    from hashlib import md5
    input_line = get_input_for_day(14).readline()
    keys = []
    hash_cache = {}
    index = 0
    while len(keys) < 64:
        index += 1
        md5_hash = hash_cache.get(index)
        if not md5_hash:
            md5_hash = md5(input_line + str(index)).hexdigest()
            if part_2:
                for _ in xrange(2016):
                    md5_hash = md5(md5_hash).hexdigest()
            hash_cache[index] = md5_hash
        same_character = None
        for i in xrange(len(md5_hash)-2):
            if md5_hash[i] == md5_hash[i+1] and md5_hash[i] == md5_hash[i+2]:
                same_character = md5_hash[i]
                break
        if same_character is not None:
            for i in xrange(1, 1000):
                new_hash = hash_cache.get(index + i)
                if not new_hash:
                    new_hash = md5(input_line + str(index + i)).hexdigest()
                    if part_2:
                        for _ in xrange(2016):
                            new_hash = md5(new_hash).hexdigest()
                    hash_cache[index+i] = new_hash
                found_hash = False
                for char in xrange(len(new_hash)-4):
                    if new_hash[char] == same_character and new_hash[char] == new_hash[char+1] and new_hash[char] == new_hash[char+2] and new_hash[char] == new_hash[char+3] and new_hash[char] == new_hash[char+4]:
                        keys.append((md5_hash, index, new_hash, index + i))
                        found_hash = True
                        break
                if found_hash:
                    break
    return index


def day_15():
    input_file = get_input_for_day(15)
    discs = []
    for line in input_file:
        pieces = line.rstrip('.\n').split(' ')
        positions = int(pieces[3])
        start = int(pieces[-1])
        discs.append((start, positions))
    if part_2:
        discs.append((0, 11))
    time = 0
    while not all((disc[0] + time + index + 1) % disc[1] == 0 for index, disc in enumerate(discs)):
        time += 1
    return time


def day_16():
    def grow(a):
        b = "".join(["10"[int(char)] for char in a[::-1]])
        return "".join((a, "0", b))

    def checksum(data):
        new_checksum = "".join(["01"[data[i] == data[i + 1]] for i in xrange(0, len(data), 2)])
        if len(new_checksum) % 2 == 0:
            new_checksum = checksum(new_checksum)
        return new_checksum

    input_line = get_input_for_day(16).readline()
    disk = grow(input_line)
    disk_length = 272 if not part_2 else 35651584
    while len(disk) < disk_length:
        disk = grow(disk)
    return checksum(disk[:disk_length])


if __name__ == '__main__':
    takes_awhile = [5, 8, 12, 14]
    for day in xrange(1, 26):
        if 'day_%s' % day in dir() and day not in takes_awhile:
            print 'Day %s:' % day
            part_2 = False
            print ' Part 1:', eval('day_%s()' % day)
            part_2 = True
            print ' Part 2:', eval('day_%s()' % day)
