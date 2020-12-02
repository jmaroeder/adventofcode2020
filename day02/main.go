package main

import (
	"flag"
	"io/ioutil"
	"os"
	"strings"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/jmaroeder/adventofcode2020/pkg"
	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

type InputLine struct {
	Min      int
	Max      int
	Letter   string
	Password string
}

// returns part1 and part2
func run(input string) (interface{}, interface{}) {
	part1, part2 := 0, 0

	inputValues := parse(input)

	log.Debug().Interface("inputValues", inputValues).Msg("")

	for _, inputLine := range inputValues {
		if checkPass1(inputLine.Min, inputLine.Max, inputLine.Letter, inputLine.Password) {
			part1++
		}
		if checkPass2(inputLine.Min, inputLine.Max, inputLine.Letter, inputLine.Password) {
			part2++
		}
	}

	return part1, part2
}

func parse(s string) []InputLine {
	lines := strings.Split(strings.TrimSpace(s), "\n")
	list := make([]InputLine, len(lines))
	for i, line := range lines {
		log.Debug().Str("line", line).Msg("")
		pkg.MustScanf(line, "%d-%d %1s: %s", &list[i].Min, &list[i].Max, &list[i].Letter, &list[i].Password)
	}
	return list
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

func checkPass1(min int, max int, letter string, password string) bool {
	occurences := strings.Count(password, letter)
	return occurences >= min && occurences <= max
}

func checkPass2(pos1 int, pos2 int, letter string, password string) bool {
	return (string(password[pos1-1]) == letter) != (string(password[pos2-1]) == letter)
}
