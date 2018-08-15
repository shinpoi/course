package main

import "fmt"

func main() {
	fmt.Println(len("abcde"))
	fmt.Println(len("世界"))
	fmt.Println(len("いろは"))
	fmt.Println("汉字"[:3])
	fmt.Println("汉字"[:4])

	fmt.Println("------------------------------")
	for i, r := range "Hello, 世界" {
		fmt.Printf("%3d %10q %6x\n", i, r, r)
	}

	fmt.Println("------------------------------")
	for i, r := range []rune("Hello, 世界") {
		fmt.Printf("%3d %10q %6x\n", i, r, r)
	}

	fmt.Println("------------------------------")
	for i, r := range []byte("Hello, 世界") {
		fmt.Printf("%3d %10q %6x\n", i, r, r)
	}

}
