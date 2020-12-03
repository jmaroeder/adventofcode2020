package main

import (
	"flag"
	"io/ioutil"
	"os"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/jmaroeder/adventofcode2020/pkg"
	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

// returns part1 and part2
func run(input string) (interface{}, interface{}) {
	part1, part2 := 0, 0

	inputValues := pkg.ParseIntList(input, ",")

	log.Info().Interface("inputValues", inputValues).Msg("")

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
