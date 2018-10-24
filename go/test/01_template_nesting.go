package main

import (
	"log"
	"os"
	"text/template"
)

var tmpStr = `
{{ block "c1" .}} default c1 {{ end }}
`

var c1 = `< {{ block "c2" .}} default c2 {{ end }} >`
var c2 = `
{{ define "c2" }}
< {{ block "c3" .}} default c3 {{ end }} >
{{ end }}
`

var c31 = `
{{ define "c3" }}< this is block c3-1 >{{ end }}
`

var c32 = `
{{ define "c3" }}< this is block c3-2 >{{ end }}
`

func main() {
	tmpl, err := template.New("test_template").Parse(tmpStr)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("\n\n---- define 1 ----")
	tmpl1, _ := tmpl.Clone()
	tmpl1.Parse(c32)
	tmpl1.Parse(c31)
	tmpl1.Parse(c2)
	tmpl1.Parse(c1)
	tmpl1.Execute(os.Stdout, nil)

	log.Println("\n\n---- define 2 ----")
	tmpl2, _ := tmpl.Clone()
	tmpl2.Parse(c1)
	tmpl2.Parse(c2)
	tmpl2.Parse(c31)
	tmpl2.Parse(c32)
	tmpl2.Execute(os.Stdout, nil)

	log.Println("\n\n---- define 2 ----")
	tmpl3, _ := tmpl.Clone()
	tmpl3.Parse(c1)
	tmpl3.Parse(c2)
	tmpl3.Parse(c32)
	tmpl3.Parse(c31)
	tmpl3.Execute(os.Stdout, nil)

}
