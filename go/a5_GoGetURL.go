package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	start := time.Now()
	ch := make(chan string)
	for i, url := range os.Args[1:] {
		fmt.Printf("URL %d: \n", i)
		go fetch(url, ch)
	}

	for range os.Args[1:] {
		fmt.Println(<-ch)
	}

	fmt.Printf("time(sum): %2fs\n", time.Since(start).Seconds())
}

func fetch(url string, ch chan<- string) {
	start := time.Now()

	if !strings.HasPrefix(url, "http") {
		url = "http://" + url
	}

	resp, err := http.Get(url)
	printErr(err)

	written, err := io.Copy(ioutil.Discard, resp.Body)
	resp.Body.Close()
	printErr(err)

	secs := time.Since(start).Seconds()
	ch <- fmt.Sprintf("time: %.2fs || bytes: %7d  ||  url: %s", secs, written, url)
}

func printErr(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "fetch: %v\n", err)
		os.Exit(-1)
	}
}
