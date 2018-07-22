package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
)

var mu sync.Mutex
var count int

func main() {
	http.HandleFunc("/count", counter)
	http.HandleFunc("/", handler)
	http.HandleFunc("/gif", func(w http.ResponseWriter, r *http.Request) { lissajous(w) })
	http.ListenAndServe("localhost:8000", nil)
}

func handler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	count++
	mu.Unlock()
	fmt.Fprintf(w, "Path: %s\n", r.URL.Path)

	fmt.Printf("%s %s %s\n", r.Method, r.URL, r.Proto)
	for k, v := range r.Header {
		fmt.Printf("Header[%q] = %q\n", k, v)
	}

	fmt.Printf("Host = %q\n", r.Host)
	fmt.Printf("RemoteAddr = %q\n", r.RemoteAddr)

	if err := r.ParseForm(); err != nil {
		log.Print(err)
	}

	for k, v := range r.Form {
		fmt.Printf("Form[%q] = %q\n", k, v)
	}

	fmt.Println("===================================")
}

func counter(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	fmt.Fprintf(w, "Count %d\n", count)
	mu.Unlock()

	fmt.Printf("%s %s %s\n", r.Method, r.URL, r.Proto)
	for k, v := range r.Header {
		fmt.Printf("Header[%q] = %q\n", k, v)
	}

	fmt.Printf("Host = %q\n", r.Host)
	fmt.Printf("RemoteAddr = %q\n", r.RemoteAddr)

	if err := r.ParseForm(); err != nil {
		log.Print(err)
	}

	for k, v := range r.Form {
		fmt.Printf("Form[%q] = %q\n", k, v)
	}

	fmt.Println("===================================")
}
