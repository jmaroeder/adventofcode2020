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

	part1Surveys := parsePart1(input)

	for _, survey := range part1Surveys {
		part1 += len(survey)
	}

	part2Surveys := parsePart2(input)
	for _, survey := range part2Surveys {
		part2 += len(survey)
	}

	return part1, part2
}

func parsePart1(s string) []map[rune]bool {
	ret := []map[rune]bool{}
	lines := strings.Split(strings.TrimSpace(s), "\n")
	currentSurvey := map[rune]bool{}
	for _, line := range lines {
		if line == "" {
			ret = append(ret, currentSurvey)
			currentSurvey = map[rune]bool{}
			continue
		}
		for _, c := range line {
			currentSurvey[c] = true
		}
	}
	ret = append(ret, currentSurvey)
	return ret
}

func intersection(set []map[rune]bool) map[rune]bool {
	ret := map[rune]bool{}
	for c := range set[0] {
		missing := false
		for _, other := range set[1:] {
			if !other[c] {
				missing = true
				break
			}
		}
		if !missing {
			ret[c] = true
		}
	}
	return ret
}

func parsePart2(s string) []map[rune]bool {
	ret := []map[rune]bool{}
	lines := strings.Split(strings.TrimSpace(s), "\n")

	currentGroup := []map[rune]bool{}
	for _, line := range lines {
		if line == "" {
			ret = append(ret, intersection(currentGroup))
			currentGroup = []map[rune]bool{}
			continue
		}
		currentSurvey := map[rune]bool{}
		for _, c := range line {
			currentSurvey[c] = true
		}
		currentGroup = append(currentGroup, currentSurvey)
	}
	ret = append(ret, intersection(currentGroup))
	return ret
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
