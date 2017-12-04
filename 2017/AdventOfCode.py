from collections import defaultdict

get_input_for_day = lambda day: open('inputs/day_%s_input.txt' % str(day))
part_2 = False


def day_1():
    input_line = get_input_for_day(1).readline()
    checksum = 0
    if not part_2:
        if input_line[0] == input_line[-1]:
            checksum += int(input_line[0])
        for i in range(len(input_line) - 1):
            if input_line[i] == input_line[i+1]:
                checksum += int(input_line[i])
    else:
        if input_line[0] == input_line[len(input_line)/2]:
            checksum += int(input_line[0])
        for i in range(len(input_line) - 1):
            if input_line[i] == input_line[(i+(len(input_line)/2))%len(input_line)]:
                checksum += int(input_line[i])

    return checksum


def day_2():
    input_file = get_input_for_day(2)
    diffs = []
    for line in input_file:
        nums = map(int, line.split())
        if not part_2:
            diffs.append(max(nums) - min(nums))
        else:
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    if nums[i] % nums[j] == 0 or nums[j] % nums[i] == 0:
                        diffs.append(abs(max(nums[i], nums[j])/min(nums[i], nums[j])))
                        break
    return sum(diffs)


def day_3():
    move_right = lambda (x, y): (x + 1, y)
    move_down = lambda (x, y): (x, y - 1)
    move_left = lambda (x, y): (x - 1, y)
    move_up = lambda (x, y): (x, y + 1)

    moves = [move_right, move_up, move_left, move_down]

    adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def get_location_value(location, location_vals):
        val = 0
        for adj in adjacent:
            val += location_vals[(location[0] + adj[0], location[1] + adj[1])]
        return val

    def gen_spiral(num):
        curr_num = 1
        location = (0, 0)
        times_to_move = 1
        curr_move = 0
        location_values = defaultdict(lambda: 0)
        location_values[location] = curr_num
        while True:
            for _ in range(2):
                move = moves[curr_move]
                for _ in range(times_to_move):
                    if curr_num == num:
                        return location
                    location = move(location)
                    curr_num += 1
                    location_values[location] = get_location_value(location, location_values)
                    if part_2 and location_values[location] > num:
                        return location_values[location]
                curr_move = (curr_move + 1) % 4
            times_to_move += 1

    input_num = 347991
    result = gen_spiral(input_num)
    return sum(map(abs, result)) if not part_2 else result


def day_4():
    input_file = get_input_for_day(4)
    answer = 0
    for line in input_file:
        words = set()
        pieces = line.split()
        for word in pieces:
            if (not part_2 and word in words) or "".join(sorted(word)) in words:
                break
            words.add(word if not part_2 else "".join(sorted(word)))
        else:
            answer += 1
    return answer


if __name__ == '__main__':
    for day in xrange(1, 26):
        if 'day_%s' % day in dir():
            print 'Day %s:' % day
            part_2 = False
            print ' Part 1:', eval('day_%s()' % day)
            part_2 = True
            print ' Part 2:', eval('day_%s()' % day)
