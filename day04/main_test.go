package main

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	os.Exit(m.Run())
}

type FieldTestCase struct {
	Value          string
	ExpectedResult bool
}

func TestIsByrValid(t *testing.T) {
	testCases := map[string]bool{
		"2002": true,
		"2003": false,
	}
	for value, expectedResult := range testCases {
		assert.Equal(t, expectedResult, isByrValid(value), "%s fail", value)
	}
}

func TestIsIyrValid(t *testing.T) {
	testCases := map[string]bool{
		"2010": true,
		"2021": false,
	}
	for value, expectedResult := range testCases {
		assert.Equal(t, expectedResult, isIyrValid(value), "%s fail", value)
	}
}

func TestIsEyrValid(t *testing.T) {
	testCases := map[string]bool{
		"2020": true,
		"2031": false,
	}
	for value, expectedResult := range testCases {
		assert.Equal(t, expectedResult, isEyrValid(value), "%s fail", value)
	}
}

func TestIsHgtValid(t *testing.T) {
	testCases := map[string]bool{
		"60in":  true,
		"190cm": true,
		"190in": false,
		"190":   false,
	}
	for value, expectedResult := range testCases {
		assert.Equal(t, expectedResult, isHgtValid(value), "%s fail", value)
	}
}

func TestIsHclValid(t *testing.T) {
	testCases := map[string]bool{
		"#123abc": true,
		"#123abz": false,
		"123abc":  false,
	}
	for value, expectedResult := range testCases {
		assert.Equal(t, expectedResult, isHclValid(value), "%s fail", value)
	}
}

func TestIsEclValid(t *testing.T) {
	testCases := map[string]bool{
		"brn": true,
		"wat": false,
	}
	for value, expectedResult := range testCases {
		assert.Equal(t, expectedResult, isEclValid(value), "%s fail", value)
	}
}

func TestIsPidValid(t *testing.T) {
	testCases := map[string]bool{
		"000000001":  true,
		"0123456789": false,
	}
	for value, expectedResult := range testCases {
		assert.Equal(t, expectedResult, isPidValid(value), "%s fail", value)
	}
}

type PassportTestCase struct {
	Passport       map[string]string
	ExpectedResult bool
}

func TestIsPassportValid(t *testing.T) {
	testCases := []PassportTestCase{
		{
			Passport: map[string]string{
				"ecl": "gry",
				"pid": "860033327",
				"eyr": "2020",
				"hcl": "#fffffd",
				"byr": "1937",
				"iyr": "2017",
				"cid": "147",
				"hgt": "183cm",
			},
			ExpectedResult: true,
		},
		{
			Passport: map[string]string{
				"iyr": "2013",
				"ecl": "amb",
				"cid": "350",
				"eyr": "2023",
				"pid": "028048884",
				"hcl": "#cfa07d",
				"byr": "1929",
			},
			ExpectedResult: false,
		},
		{
			Passport: map[string]string{
				"hcl": "#ae17e1",
				"iyr": "2013",
				"eyr": "2024",
				"ecl": "brn",
				"pid": "760753108",
				"byr": "1931",
				"hgt": "179cm",
			},
			ExpectedResult: true,
		},
		{
			Passport: map[string]string{
				"hcl": "#cfa07d", "eyr": "2025", "pid": "166559648",
				"iyr": "2011", "ecl": "brn", "hgt": "59in",
			},
			ExpectedResult: false,
		},
	}
	for _, tt := range testCases {
		assert.Equal(t, tt.ExpectedResult, isPassportValid(tt.Passport), "%s fail", tt)
	}
}
