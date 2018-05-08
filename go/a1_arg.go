package main

import (
	"bufio"
	"fmt"
	"os"
)

func main(){
	var s, sstd, sep string
	
	// Parameter
	sep = " "
	s += "args: "
	/*for i:=2; i<len(os.Args);i++{
		s += sep + os.Args[i]
	}*/
	for _, arg := range os.Args[1:]{
		s += sep + arg
	}
	fmt.Println(s)
	
	// Stdin
	sep = "\n"
	sstd += "stdin: "
	scanStdin := bufio.NewScanner(os.Stdin)
	for scanStdin.Scan() {
		sstd += scanStdin.Text() + sep
	}
	fmt.Println(sstd)
}
