package main

import (
	"flag"
	"io/ioutil"
	"os"
	"regexp"
	"strings"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/jmaroeder/adventofcode2020/pkg"
	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

// returns part1 and part2
func run(input string) (interface{}, interface{}) {
	part1, part2 := 0, 0

	passports := parse(input)

	log.Debug().Interface("passports", passports).Msg("")

	validPassports := 0

	for _, passport := range passports {
		if isPassportValid(passport) {
			validPassports++
		}
	}
	part1 = validPassports

	return part1, part2
}

func parse(s string) []map[string]string {
	lines := strings.Split(strings.TrimSpace(s), "\n")
	var passports []map[string]string
	passport := map[string]string{}
	for _, line := range lines {
		if strings.TrimSpace(line) == "" {
			passports = append(passports, passport)
			passport = map[string]string{}
			continue
		}
		for _, keyValuePair := range strings.Split(line, " ") {
			var key, value string
			pkg.MustScanf(keyValuePair, "%3s:%s", &key, &value)
			passport[key] = value
		}
	}
	passports = append(passports, passport)
	return passports
}

func isPassportValid(passport map[string]string) bool {
	requiredFields := map[string]bool{
		"byr": true,
		"iyr": true,
		"eyr": true,
		"hgt": true,
		"hcl": true,
		"ecl": true,
		"pid": true,
	}

	for field := range passport {
		delete(requiredFields, field)
	}

	return len(requiredFields) == 0
}

func isByrValid(byr string) bool {
	res, err := regexp.MatchString(`^\d{4}$`, byr)
	pkg.Check(err)
	if !res {
		return false
	}
	year := pkg.MustAtoi(byr)
	return year >= 1920 && year <= 2002
}

func areFieldsValid(passport map[string]string) bool {
	return false
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
