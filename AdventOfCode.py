get_input_for_day = lambda day: open('inputs/day_%s_input.txt' % str(day))
part_1 = True


def day_1():
    input_string = get_input_for_day(1).readline()

    current_floor = 0
    first_negative = None
    for index in xrange(len(input_string)):
        if input_string[index] is '(':
            current_floor += 1
        elif input_string[index] is ')':
            current_floor -= 1
        if current_floor is -1 and first_negative is None:
            first_negative = index + 1

    return current_floor, first_negative

def day_2():
    input_file = get_input_for_day(2)

    required_material_for_box = lambda l,w,h: 3*l*w + 2*w*h + 2*l*h
    required_ribbon_for_box = lambda l,w,h: 2*l + 2*w + l*w*h
    required_material = 0
    required_ribbon = 0
    for line in input_file:
        box = sorted(map(int, line.split('x')))
        required_material += required_material_for_box(*box)
        required_ribbon += required_ribbon_for_box(*box)

    return required_material, required_ribbon

def day_3():
    input_string = get_input_for_day(3).readline()

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
        if not part_1:
            santa_turn = not santa_turn

    return len(locations)

def day_4():
    from hashlib import md5
    secret_key = get_input_for_day(4).readline()
    hash_value = ''
    answer = 0
    zeros = '00000' if part_1 else '000000'
    while not hash_value.startswith(zeros):
        answer += 1
        hash_value = md5(secret_key + str(answer)).hexdigest()
    return answer

def day_5():
    input_file = get_input_for_day(5)
    nice_count = 0
    bad_strings = ['ab', 'cd', 'pq', 'xy']
    vowels = 'aeiou'
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

    return nice_count

def day_6():
    input_file = get_input_for_day(6)

    light_grid = [[0 for _ in xrange(1000)] for _ in xrange(1000)]
    if part_1:
        turn_on = lambda _: 1
        turn_off = lambda _: 0
        toggle = lambda val: val ^ 1
    else:
        turn_on = lambda val: val + 1
        turn_off = lambda val: max(0, val-1)
        toggle = lambda val: val + 2
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

    return sum(sum(row) for row in light_grid)

def day_7():
    input_file = get_input_for_day(7)
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

    return calculate('a')

def day_8():
    input_file = get_input_for_day(8)
    characters = 0
    memory = 0
    difference = 0
    for line in input_file:
        line = line.strip()
        characters += len(line)
        memory += len(eval(line))
        difference += line.count('\\') + line.count('"') + 2

    return characters - memory, difference

def day_9():
    from itertools import permutations
    from collections import defaultdict

    input_file = get_input_for_day(9)
    distances = defaultdict(dict)
    for line in input_file:
        path, distance = line.split(' = ')
        source, sink = path.split(' to ')
        distances[source][sink] = int(distance)
        distances[sink][source] = int(distance)

    shortest_dist = longest_dist = None
    for perm in permutations(distances.keys()):
        potential_dist = 0
        for ind, city in enumerate(perm[:-1]):
            potential_dist += distances[city][perm[ind+1]]

        if shortest_dist is None or potential_dist < shortest_dist:
            shortest_dist = potential_dist
        if longest_dist is None or potential_dist > longest_dist:
            longest_dist = potential_dist

    return shortest_dist, longest_dist

def day_10():
    def look_say(input_sequence):
        result = ''
        digit_count = 0
        prev_digit = input_sequence[0]
        for digit in input_sequence:
            if prev_digit == digit:
                digit_count += 1
            else:
                result += str(digit_count) + prev_digit
                prev_digit = digit
                digit_count = 1
        result += str(digit_count) + prev_digit
        return result

    sequence = get_input_for_day(10).readline()
    repetitions = 40 if part_1 else 50
    for _ in xrange(repetitions):
        sequence = look_say(sequence)
    return len(sequence)

def day_11():
    def valid_password(password):
        if any(bad_char in password for bad_char in 'iol'):
            return False
        found_pair = False
        found_pair_ord = None
        for ind in xrange(0, len(password)-1):
            if ord(password[ind]) == ord(password[ind+1]):
                if found_pair:
                    if ord(password[ind]) != found_pair_ord:
                        break
                else:
                    found_pair_ord = ord(password[ind])
                    found_pair = True
        else:
            return False

        for ind in xrange(0, len(password)-2):
            if ord(password[ind]) == ord(password[ind+1]) - 1 and ord(password[ind]) == ord(password[ind+2]) - 2:
                break
        else:
            return False
        return True

    def next_password(password):
        next_pass = ''
        for ind, char in enumerate(password):
            if char in 'iol':
                next_ord = (ord(char)+1) % 123
                char = chr(next_ord or 97)
                next_pass += char
                for _ in password[ind:-1]:
                    next_pass += 'a'
                return next_pass
            else:
                next_pass += char
        next_pass = ''
        overflow = True
        for ind, char in enumerate(password[::-1]):
            next_ord = (ord(char)+1) % 123
            if overflow:
                next_pass += chr(next_ord or 97)
                if next_ord != 0:
                    overflow = False
            else:
                next_pass += char

        return next_pass[::-1]

    input_password = get_input_for_day(11).readline()
    while not valid_password(input_password):
        input_password = next_password(input_password)
    return input_password

def day_12():
    import json

    def calc_sum(n):
        sum_n = 0
        if type(n) == list:
            for elem in n:
                sum_n += calc_sum(elem)
        elif type(n) == dict:
            if part_1 or ('red' not in n.keys() and 'red' not in n.values()):
                for key in n:
                    sum_n += calc_sum(n[key])
        elif type(n) == int:
            sum_n += n
        return sum_n

    input_file = get_input_for_day(12).readline()
    input_json = json.loads(input_file)
    sum_input = calc_sum(input_json)
    return sum_input

def day_13():
    from collections import defaultdict
    from itertools import permutations

    input_file = get_input_for_day(13)
    happiness = defaultdict(dict)
    for line in input_file:
        parts = line.split()
        happiness[parts[0]][parts[10].rstrip('.')] = int(parts[3])
        if parts[2] == 'lose':
            happiness[parts[0]][parts[10].rstrip('.')] *= -1

    if not part_1:
        happiness['you'] = {}
        for key in happiness:
            happiness[key]['you'] = 0
            happiness['you'][key] = 0

    happiness_max = 0
    for perm in permutations(happiness.keys()):
        happiness_perm = 0
        for ind, person in enumerate(perm[:-1]):
            happiness_perm += happiness[person][perm[ind-1]]
            happiness_perm += happiness[person][perm[ind+1]]
            if happiness_perm > happiness_max:
                happiness_max = happiness_perm
    return happiness_max

def day_14():
    from collections import defaultdict

    input_file = get_input_for_day(14)
    reindeer_data = defaultdict(dict)
    race_time = 2503

    for line in input_file:
        parts = line.split()
        reindeer_data[parts[0]]['speed'] = int(parts[3])
        reindeer_data[parts[0]]['endurance'] = int(parts[6])
        reindeer_data[parts[0]]['rest'] = int(parts[13])
        reindeer_data[parts[0]]['travelled'] = 0
        reindeer_data[parts[0]]['points'] = 0

    for num in xrange(0, race_time):
        for reindeer in reindeer_data:
            total_interval = reindeer_data[reindeer]['endurance'] + reindeer_data[reindeer]['rest']
            fly_interval = total_interval % reindeer_data[reindeer]['rest']
            if num % total_interval < fly_interval:
                reindeer_data[reindeer]['travelled'] += reindeer_data[reindeer]['speed']
        if not part_1:
            current_leaders = []
            current_leader_distance = 0
            for reindeer in reindeer_data:
                if reindeer_data[reindeer]['travelled'] > current_leader_distance:
                    current_leader_distance = reindeer_data[reindeer]['travelled']
                    current_leaders = [reindeer]
                elif reindeer_data[reindeer]['travelled'] == current_leader_distance:
                    current_leaders.append(reindeer)
            for leader in current_leaders:
                reindeer_data[leader]['points'] += 1

    return reindeer_data[max(reindeer_data, key=lambda x: reindeer_data[x]['travelled'])]['travelled'], \
           reindeer_data[max(reindeer_data, key=lambda x: reindeer_data[x]['points'])]['points']


def day_15():
    from collections import defaultdict
    from itertools import product

    input_file = get_input_for_day(15)
    ingredients = defaultdict(dict)
    for line in input_file:
        parts = line.strip(':').replace(',', ' ').split()
        ingredients[parts[0]]['capacity'] = int(parts[2])
        ingredients[parts[0]]['durability'] = int(parts[4])
        ingredients[parts[0]]['flavor'] = int(parts[6])
        ingredients[parts[0]]['texture'] = int(parts[8])
        ingredients[parts[0]]['calories'] = int(parts[10])

    current_best = 0
    best_calorie_wise = 0
    teaspoons = 100

    ingredient_combinations = [xrange(1, teaspoons+1) for _ in xrange(len(ingredients.keys())-1)]
    for combo in product(*ingredient_combinations):
        if sum(combo) > 100:
            continue
        last_ingredient_amount = teaspoons - sum(combo)
        ingredient_amounts = list(combo) + [last_ingredient_amount]

        capacity = durability = flavor = texture = calories = 0

        for index, name in enumerate(ingredients.keys()):
            capacity += ingredients[name]['capacity'] * ingredient_amounts[index]
            durability += ingredients[name]['durability'] * ingredient_amounts[index]
            flavor += ingredients[name]['flavor'] * ingredient_amounts[index]
            texture += ingredients[name]['texture'] * ingredient_amounts[index]
            calories += ingredients[name]['calories'] * ingredient_amounts[index]

        potential = reduce(lambda x, y: x*y, map(lambda num: max(0, num), [capacity, durability, flavor, texture]))
        current_best = max(potential, current_best)
        if calories == 500:
            best_calorie_wise = max(potential, best_calorie_wise)

    return current_best, best_calorie_wise


def day_16():
    from collections import defaultdict
    input_file = get_input_for_day(16)
    sues = defaultdict(dict)
    for line in input_file:
        parts = line.lstrip('Sue ').replace(':', ',').split(', ')
        for index, elem in enumerate(parts[1::2]):
            sues[parts[0]][elem] = int(parts[2*index+2])
    matching_criteria = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }
    matching_sue_num = 0
    for sue_num in sues:
        matching_sue = True
        for compound in sues[sue_num]:
            if part_1:
                if sues[sue_num][compound] == matching_criteria[compound]:
                    continue
                else:
                    matching_sue = False
                    break
            else:
                if compound in ['cats', 'trees']:
                    if sues[sue_num][compound] > matching_criteria[compound]:
                        continue
                    else:
                        matching_sue = False
                        break
                elif compound in ['pomeranians', 'goldfish']:
                    if sues[sue_num][compound] < matching_criteria[compound]:
                        continue
                    else:
                        matching_sue = False
                        break
                elif sues[sue_num][compound] == matching_criteria[compound]:
                    continue
                else:
                    matching_sue = False
                    break
        if matching_sue:
            matching_sue_num = sue_num
            break
    return matching_sue_num

def day_17():
    from itertools import combinations
    input_file = get_input_for_day(17)

    liters = 150
    containers = []
    for line in input_file:
        containers.append(int(line))
    containers = sorted(containers, reverse=True)

    combos = 0
    found_min = False
    for i in xrange(len(containers)):
        for combo in combinations(containers, i+1):
            if sum(combo) == liters:
                found_min = True
                combos += 1
        if found_min and not part_1:
            break
    return combos


def day_18():
    size = 100
    light_grid = [['.' for _ in xrange(size)] for _ in xrange(size)]

    def number_of_on_neighbors(x, y):
        on_neighbors = 0
        bottom = top = left = right = True
        if y == 0:
            left = False
        if y == size-1:
            right = False
        if x == 0:
            top = False
        if x == size-1:
            bottom = False
        if bottom:
            if light_grid[x+1][y] == '#':
                on_neighbors += 1
        if top:
            if light_grid[x-1][y] == '#':
                on_neighbors += 1
        if left:
            if light_grid[x][y-1] == '#':
                on_neighbors += 1
        if right:
            if light_grid[x][y+1] == '#':
                on_neighbors += 1
        if bottom and right and light_grid[x+1][y+1] == '#':
            on_neighbors += 1
        if bottom and left and light_grid[x+1][y-1] == '#':
            on_neighbors += 1
        if top and right and light_grid[x-1][y+1] == '#':
            on_neighbors += 1
        if top and left and light_grid[x-1][y-1] == '#':
            on_neighbors += 1
        return on_neighbors

    input_file = get_input_for_day(18)
    row = 0
    for line in input_file:
        for ind, char in enumerate(line.strip()):
            light_grid[row][ind] = char
        row += 1
    if not part_1:
        light_grid[0][0] = light_grid[0][size-1] = light_grid[size-1][0] = light_grid[size-1][size-1] = '#'
    next_state = [['.' for _ in xrange(size)] for _ in xrange(size)]
    for _ in xrange(100):
        for x in xrange(size):
            for y in xrange(size):
                neighbors = number_of_on_neighbors(x, y)
                if light_grid[x][y] == '.':
                    if neighbors == 3:
                        next_state[x][y] = '#'
                    else:
                        next_state[x][y] = '.'
                elif light_grid[x][y] == '#':
                    if neighbors == 2 or neighbors == 3:
                        next_state[x][y] = '#'
                    else:
                        next_state[x][y] = '.'
        light_grid = next_state
        if not part_1:
            light_grid[0][0] = light_grid[0][size-1] = light_grid[size-1][0] = light_grid[size-1][size-1] = '#'
        next_state = [['.' for _ in xrange(size)] for _ in xrange(size)]
    num = 0
    for x in xrange(size):
        for y in xrange(size):
            if light_grid[x][y] == '#':
                num += 1
    return num


def day_19():
    from collections import defaultdict
    from random import shuffle

    input_file = get_input_for_day(19)
    starting_molecule_atoms = []
    atom_replacements = defaultdict(list)
    molecules = set()

    def do_replacements(molecule):
        next_molecules = []
        for ind, atm in enumerate(molecule):
            if atm in atom_replacements:
                for replace in atom_replacements[atm]:
                    next_molecule = molecule[:ind] + replace + molecule[ind+1:]
                    stringed_molecule = ''.join(next_molecule)
                    if stringed_molecule not in molecules:
                        molecules.add(stringed_molecule)
                        next_molecules.append(next_molecule)
        return next_molecules

    done_replacements = False
    for line in input_file:
        if done_replacements:
            starting_sequence = line.strip()
            while len(starting_sequence):
                char_one = starting_sequence[0]
                if char_one in atom_replacements.keys():
                    starting_molecule_atoms.append(char_one)
                    starting_sequence = starting_sequence[1:]
                else:
                    char_two = starting_sequence[1]
                    if char_one+char_two in atom_replacements.keys():
                        starting_molecule_atoms.append(char_one+char_two)
                        starting_sequence = starting_sequence[2:]
                    else:
                        starting_molecule_atoms.append(char_one)
                        starting_sequence = starting_sequence[1:]
        elif ' => ' in line:
            parts = line.strip().split(' => ')
            atom_replacements[parts[0]].append(parts[1])
        else:
            done_replacements = True
    for atom in atom_replacements:
        for index, replacement in enumerate(atom_replacements[atom]):
            replacement_list = []
            while len(replacement):
                char_one = replacement[0]
                if char_one in atom_replacements.keys():
                    replacement_list.append(char_one)
                    replacement = replacement[1:]
                else:
                    char_two = '' if len(replacement) == 1 else replacement[1]
                    if char_one+char_two in atom_replacements.keys():
                        replacement_list.append(char_one+char_two)
                        replacement = replacement[2:]
                    else:
                        replacement_list.append(char_one)
                        replacement = replacement[1:]
            atom_replacements[atom][index] = replacement_list

    do_replacements(starting_molecule_atoms)
    part_1_num = len(molecules)
    target = 'e'
    current = ''.join(starting_molecule_atoms)
    num_replacements = 0
    replacements = [(atom, ''.join(replacement)) for atom in atom_replacements for replacement in atom_replacements[atom]]
    replacements = sorted(replacements, key=lambda x: len(x[1]), reverse=True)
    while current != target:
        old_current = current
        for atom, replacement in replacements:
            if replacement in current:
                current = current.replace(replacement, atom, 1)
                num_replacements += 1
        if current == old_current:
            current = ''.join(starting_molecule_atoms)
            num_replacements = 0
            shuffle(replacements)

    return part_1_num, num_replacements

def day_20():
    from collections import defaultdict
    number = int(get_input_for_day(20).readline())
    if part_1:
        number /= 10
        modifier = 1
    else:
        modifier = 11
    factors = defaultdict(int)
    lowest = number
    for num in xrange(1, number):
        step_range = range(num, number+1, num)
        if not part_1:
            step_range = step_range[:50]
        for step in step_range:
            factors[step] += num * modifier
            if factors[step] > number:
                lowest = min(step, lowest)
    return lowest

if __name__ == '__main__':
    for day in xrange(1, 26):
        if 'day_%s' % day in dir():
            print 'Day %s:' % day, eval('day_%s()' % day)
