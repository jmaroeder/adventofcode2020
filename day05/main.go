package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

type boardingPass struct {
	Row, Col, ID int
}

func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}

func parseBinaryString(s string, off rune, on rune) int {
	ret := 0
	for _, c := range s {
		ret <<= 1
		if c == on {
			ret++
		}
	}
	return ret
}

func parseBoardingPass(s string) boardingPass {
	row := parseBinaryString(s[0:7], 'F', 'B')
	col := parseBinaryString(s[7:10], 'L', 'R')
	return boardingPass{
		Row: row,
		Col: col,
		ID:  row*8 + col,
	}
}

func printGrid(seatGrid map[int]map[int]*(boardingPass), width int, height int) {
	for i := 0; i < height; i++ {
		fmt.Printf("%3d ", i)
		for j := 0; j < width; j++ {
			if seatGrid[i][j] != nil {
				fmt.Print("#")
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Print("\n")
	}
}

// returns part1 and part2
func run(input string) (interface{}, interface{}) {
	part1, part2 := 0, 0

	passes := strings.Split(strings.TrimSpace(input), "\n")

	seatGrid := map[int]map[int]*boardingPass{}
	width, height := 0, 0

	for _, pass := range passes {
		parsedPass := parseBoardingPass(pass)
		part1 = Max(part1, parsedPass.ID)
		width = Max(width, parsedPass.Col)
		height = Max(height, parsedPass.Row)
		if seatGrid[parsedPass.Row] == nil {
			seatGrid[parsedPass.Row] = make(map[int]*boardingPass)
		}
		seatGrid[parsedPass.Row][parsedPass.Col] = &parsedPass
	}
	width++
	height++

	printGrid(seatGrid, width, height)

	return part1, part2
}

func main() {
	debug := flag.Bool("debug", false, "sets log level to debug")
	flag.Parse()
	if *debug {
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	} else {
		zerolog.SetGlobalLevel(zerolog.InfoLevel)
	}

	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal().Err(err).Msg("")
	}
	var puzzle = string(content)

	execute.Run(run, tests, puzzle, true)
}
