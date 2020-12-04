package main

import (
	"flag"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
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

	for _, passport := range passports {
		if isPassportValid(passport) {
			part1++
			if areFieldsValid(passport) {
				part2++
			}
		}
	}

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

func mustYear(s string) int {
	res, matchErr := regexp.MatchString(`^\d{4}$`, s)
	if matchErr != nil || !res {
		return -1
	}
	i, atoiErr := strconv.Atoi(s)
	if atoiErr != nil {
		return -1
	}
	return i
}

func isByrValid(s string) bool {
	year := mustYear(s)
	return year >= 1920 && year <= 2002
}

func isIyrValid(s string) bool {
	year := mustYear(s)
	return year >= 2010 && year <= 2020
}

func isEyrValid(s string) bool {
	year := mustYear(s)
	return year >= 2020 && year <= 2030
}

func isHgtValid(s string) bool {
	re := regexp.MustCompile(`(\d+)(cm|in)`)
	res := re.FindAllStringSubmatch(s, -1)
	if len(res) != 1 {
		return false
	}
	height, atoiErr := strconv.Atoi(res[0][1])
	if atoiErr != nil {
		return false
	}
	if res[0][2] == "cm" {
		return height >= 150 && height <= 193
	}
	return height >= 59 && height <= 76
}

func isHclValid(s string) bool {
	res, matchErr := regexp.MatchString(`^#[0-9a-f]{6}$`, s)
	return matchErr == nil && res
}

func isEclValid(s string) bool {
	res, matchErr := regexp.MatchString(`^(amb|blu|brn|gry|grn|hzl|oth)$`, s)
	return matchErr == nil && res
}

func isPidValid(s string) bool {
	res, matchErr := regexp.MatchString(`^\d{9}$`, s)
	return matchErr == nil && res
}

func areFieldsValid(passport map[string]string) bool {
	return isByrValid(passport["byr"]) && isIyrValid(passport["iyr"]) && isEyrValid(passport["eyr"]) && isHgtValid(passport["hgt"]) && isHclValid(passport["hcl"]) && isEclValid(passport["ecl"]) && isPidValid(passport["pid"])
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
