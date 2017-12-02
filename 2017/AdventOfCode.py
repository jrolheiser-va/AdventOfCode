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


if __name__ == '__main__':
    for day in xrange(1, 26):
        if 'day_%s' % day in dir():
            print 'Day %s:' % day
            part_2 = False
            print ' Part 1:', eval('day_%s()' % day)
            part_2 = True
            print ' Part 2:', eval('day_%s()' % day)
