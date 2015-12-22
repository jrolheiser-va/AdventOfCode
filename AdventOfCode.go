package main

import (
    "fmt"
    "bufio"
    "os"
)

func getInput(filepath string) []string {

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
    lines := getInput("inputs/day_1_input.txt")
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

func main() {
    day_1()
}
