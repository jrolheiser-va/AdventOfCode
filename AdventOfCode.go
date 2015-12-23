package main

import (
	"fmt"
	"bufio"
	"os"
	"strings"
	"sort"
	"strconv"
)

func getInputForDay(dayNum int) []string {

	filepath := fmt.Sprintf("inputs/day_%v_input.txt", dayNum)
	file, err := os.Open(filepath)

	if err != nil {
		panic(err)
	}

	defer file.Close()
	var lines []string

	scanner := bufio.NewScanner(file)

	// Read all lines of the file
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	return lines
}

func day_1(){
	lines := getInputForDay(1)
	floor := 0
	first_negative := 0
	found_negative := false
	for _, line := range lines {
		for ind, char := range line {
			if char == '('{
				floor += 1
			} else if char == ')'{
				floor -= 1
			}
			if floor < 0 && !found_negative{
				found_negative = true
				first_negative = ind + 1
			}
		}
	}
	fmt.Printf("Day 1: %v %v\n", floor, first_negative)
}

func day_2() {
	lines := getInputForDay(2)
	wrapping_paper := 0
	ribbon := 0
	for _, line := range lines {
		temp := strings.Split(line, "x")
		var dimensions = []int{}
		tmp := 0
		for _, dimension := range temp {
			tmp, _ = strconv.Atoi(dimension)
			dimensions = append(dimensions, tmp)
		}
		sort.Ints(dimensions)
		wrapping_paper += 2 * (dimensions[0] * dimensions[1] + dimensions[0] * dimensions[2] + dimensions[1] * dimensions[2])
		wrapping_paper += dimensions[0] * dimensions[1]
		ribbon += 2 * (dimensions[0] + dimensions[1]) + dimensions[0] * dimensions[1] * dimensions[2]
	}
	fmt.Printf("Day 2: %v, %v", wrapping_paper, ribbon)
}

func main() {
	day_1()
	day_2()
}
