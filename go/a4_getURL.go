package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

func main() {
	for i, url := range os.Args[1:] {
		if !strings.HasPrefix(url, "http") {
			url = "http://" + url
		}
		fmt.Printf("URL %d: \n", i)

		resp, err := http.Get(url)
		putErr(err)

		//b, err := ioutil.ReadAll(resp.Body)
		written, err := io.Copy(os.Stdout, resp.Body)
		resp.Body.Close()
		putErr(err)
		fmt.Printf("\nstatues: %d\n", resp.StatusCode)
		fmt.Printf("wrtie %d bytes to stdout.\n", written)
	}
}

func putErr(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "fetch: %v\n", err)
		os.Exit(-1)
	}
}
