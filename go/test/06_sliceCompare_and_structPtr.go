package main

import "fmt"

type DD struct {
	X int
	Y *int
}

var (
	s1 []int
	s2 []int

	n  int
	d  DD
	pd *DD
)

func main() {
	n = 1
	d = DD{X: n, Y: &n}
	pd = &d
	fmt.Println("d.X == pd.X:", d.X == pd.X)
	fmt.Println("d.X == pd.Y:", d.Y == pd.Y)
	fmt.Println("d.X == (*pd).X:", d.X == (*pd).X)
	fmt.Println("d.X == (*pd).Y:", d.Y == (*pd).Y)

	s1 = []int{0, 1}
	s2 = []int{0, 1}
	// fmt.Println("s1 == s2:", s1 == s2)
	// >> invalid operation: s1 == s2 (slice can only be compared to nil)
}
