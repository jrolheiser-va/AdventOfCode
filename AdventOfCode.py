input_file_path = lambda day: 'inputs/day_%s_input.txt' % str(day)

def day_1():
    input_string = open(input_file_path(1)).readline()

    current_floor = 0
    first_negative = None
    for index in xrange(len(input_string)):
        if input_string[index] is '(':
            current_floor += 1
        elif input_string[index] is ')':
            current_floor -= 1
        if current_floor is -1 and first_negative is None:
            first_negative = index + 1

    print current_floor, first_negative

def day_2():
    input_file = open(input_file_path(2))

    required_material_for_box = lambda l,w,h: 3*l*w + 2*w*h + 2*l*h
    required_ribbon_for_box = lambda l,w,h: 2*l + 2*w + l*w*h
    required_material = 0
    required_ribbon = 0
    for line in input_file:
        box = sorted(map(int, line.split('x')))
        required_material += required_material_for_box(*box)
        required_ribbon += required_ribbon_for_box(*box)

    print required_material, required_ribbon

def day_3():
    input_string = open(input_file_path(3)).readline()

    locations = set()
    santa_pos_x, santa_pos_y = 0, 0
    robo_pos_x, robo_pos_y = 0, 0
    locations.add((santa_pos_x, santa_pos_y))
    santa_turn = True
    for symbol in input_string:
        if santa_turn:
            if symbol is '>':
                santa_pos_x += 1
            elif symbol is '<':
                santa_pos_x -= 1
            elif symbol is '^':
                santa_pos_y += 1
            elif symbol is 'v':
                santa_pos_y -= 1
            locations.add((santa_pos_x, santa_pos_y))
        else:
            if symbol is '>':
                robo_pos_x += 1
            elif symbol is '<':
                robo_pos_x -= 1
            elif symbol is '^':
                robo_pos_y += 1
            elif symbol is 'v':
                robo_pos_y -= 1
            locations.add((robo_pos_x, robo_pos_y))
        santa_turn = not santa_turn

    print len(locations)

def day_4():
    from hashlib import md5
    secret_key = open(input_file_path(4)).readline()
    hash_value = ''
    answer = 0
    while not hash_value.startswith('000000'):
        answer += 1
        hash_value = md5(secret_key + str(answer)).hexdigest()
    print answer

def day_5():
    input_file = open(input_file_path(5))
    nice_count = 0
    bad_strings = ['ab', 'cd', 'pq', 'xy']
    vowels = 'aeiou'
    part_1 = False
    for word in input_file:
        if part_1:
            has_double = False
            if any(bad in word for bad in bad_strings):
                continue
            vowel_count = 0
            for index, char in enumerate(word[:-1]):
                if char in vowels:
                    vowel_count += 1
                if char == word[index+1]:
                    has_double = True
            if vowel_count >= 3 and has_double:
                nice_count += 1
        else:
            xyx_pattern = False
            xyxy_pattern = False
            for index, char in enumerate(word[:-2]):
                if char == word[index+2]:
                    xyx_pattern = True
                if word.count(char + word[index+1]) >= 2:
                    xyxy_pattern = True
            if xyx_pattern and xyxy_pattern:
                nice_count += 1

    print nice_count

def day_6():
    input_file = open(input_file_path(6))

    # part 1 -> 0 for off, 1 for on, use commented out lambda values
    light_grid = [[0 for _ in xrange(1000)] for _ in xrange(1000)]
    turn_on = lambda val: val + 1  # _: 1
    turn_off = lambda val: max(0, val-1)  # _: 0
    toggle = lambda val: val + 2  # val: val ^ 1
    operator = None
    for line in input_file:
        line = line.replace(' through ', ',')
        if line.startswith('toggle '):
            line = line.lstrip('toggle ')
            operator = toggle
        elif line.startswith('turn off '):
            line = line.lstrip('turn off ')
            operator = turn_off
        elif line.startswith('turn on '):
            line = line.lstrip('turn on ')
            operator = turn_on
        start_x, start_y, end_x, end_y = map(int, line.split(','))
        for x in xrange(start_x, end_x+1):
            for y in xrange(start_y, end_y+1):
                light_grid[x][y] = operator(light_grid[x][y])

    print sum(sum(row) for row in light_grid)

def day_7():
    input_file = open(input_file_path(7))
    signals = {}
    gates = {}

    def calculate(variable):
        try:
            var = int(variable)
            return var
        except:
            pass
        if variable in signals.keys():
            signals[variable] = calculate(signals[variable])
        else:
            gate = gates[variable]
            if gate[1] == 'NOT':
                signals[variable] = ~calculate(gate[0]) & 0xFFFF
            elif gate[1] == 'AND':
                signals[variable] = calculate(gate[0]) & calculate(gate[2])
            elif gate[1] == 'OR':
                signals[variable] = calculate(gate[0]) | calculate(gate[2])
            elif gate[1] == 'RSHIFT':
                signals[variable] = calculate(gate[0]) >> gate[2]
            elif gate[1] == 'LSHIFT':
                signals[variable] = calculate(gate[0]) << gate[2]
        return signals[variable]

    for line in input_file:
        parts = line.split(' -> ')
        if parts[0].startswith('NOT'):
            pieces = parts[0].split()
            gates[parts[1].strip()] = (pieces[1], 'NOT')
        elif 'OR' in parts[0]:
            pieces = parts[0].split()
            gates[parts[1].strip()] = (pieces[0], 'OR', pieces[2])
        elif 'AND' in parts[0]:
            pieces = parts[0].split()
            gates[parts[1].strip()] = (pieces[0], 'AND', pieces[2])
        elif 'LSHIFT' in parts[0]:
            pieces = parts[0].split()
            gates[parts[1].strip()] = (pieces[0], 'LSHIFT', int(pieces[2]))
        elif 'RSHIFT' in parts[0]:
            pieces = parts[0].split()
            gates[parts[1].strip()] = (pieces[0], 'RSHIFT', int(pieces[2]))
        else:
            try:
                signals[parts[1].strip()] = int(parts[0])
            except Exception as e:
                signals[parts[1].strip()] = parts[0]

    print calculate('a')
