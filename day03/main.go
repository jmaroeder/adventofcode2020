package main

import (
	"flag"
	"io/ioutil"
	"os"
	"strings"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

// returns part1 and part2
func run(input string) (interface{}, interface{}) {
	part1, part2 := 0, 0

	treeMap, width := parse(input)

	log.Debug().Interface("treeMap", treeMap).Interface("width", width).Msg("")

	part1 = countTreesHit(treeMap, width, 3, 1)

	part2 = countTreesHit(treeMap, width, 1, 1) * countTreesHit(treeMap, width, 3, 1) * countTreesHit(treeMap, width, 5, 1) * countTreesHit(treeMap, width, 7, 1) * countTreesHit(treeMap, width, 1, 2)
	return part1, part2
}

func countTreesHit(treeMap []map[int]bool, width int, dx int, dy int) int {
	j := 0
	treesHit := 0

	// for _, row := range treeMap {
	for i := 0; i < len(treeMap); i += dy {
		if treeMap[i][j] {
			treesHit++
		}
		j += dx
		j %= width
	}
	return treesHit
}

func parse(s string) ([]map[int]bool, int) {
	lines := strings.Split(strings.TrimSpace(s), "\n")
	treeMap := make([]map[int]bool, len(lines))
	width := 0
	for i, line := range lines {
		if width == 0 {
			width = len(line)
		}
		treeMap[i] = make(map[int]bool)
		for j, char := range line {
			if string(char) == "#" {
				treeMap[i][j] = true
			}
		}
	}
	return treeMap, width
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
