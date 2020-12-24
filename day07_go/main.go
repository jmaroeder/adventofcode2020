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

	return part1, part2
}

type bagContent struct {
	n   int
	bag *Bag
}

// Bag is a node in a BagTree
type Bag struct {
	Name        string
	Contains    []bagContent
	ContainedBy []*Bag
}

// BagTree is a tree structure for storing bag rules
type BagTree struct {
	Bags map[string]*Bag
}

func getOrMakeBag(bagTree BagTree, key string) *Bag {
	bag := bagTree.Bags[key]
	if bag != nil {
		return bag
	}
	bag = new(Bag)
	bagTree.Bags[key] = bag
	bag.Name = key
	bag.Contains = []bagContent{}
	bag.ContainedBy = []*Bag{}
	return bag
}

func parseRules(s string) BagTree {
	re := regexp.MustCompile(`^(.*) bags contain (.*).$`)
	innerRe := regexp.MustCompile(`^(\d+) (.*) bags?.$`)
	bagTree := BagTree{}
	for _, line := range strings.Split(strings.TrimSpace(s), "\n") {
		// dark orange bags contain 3 bright white bags, 4 muted yellow bags.
		// faded blue bags contain no other bags.
		result := re.FindStringSubmatch(line)
		if result == nil {
			panic("No match")
		}
		outerKey := result[1]
		outerBag := getOrMakeBag(bagTree, outerKey)
		if result[2] == "no other bags" {
			continue
		}
		for _, bagDesc := range strings.Split(result[2], ", ") {
			innerResult := innerRe.FindStringSubmatch(bagDesc)
			if innerResult == nil {
				panic("No match")
			}
			innerKey := result[2]
			innerBag := getOrMakeBag(bagTree, innerKey)
			outerBag.Contains = append(outerBag.Contains, bagContent{pkg.MustAtoi(result[1]), innerBag})
			innerBag.ContainedBy = append(innerBag.ContainedBy, outerBag)
		}
	}
	return bagTree
}

func canContain(bagTree BagTree, outerKey string, innerKey string) bool {

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
