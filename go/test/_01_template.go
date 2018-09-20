package main

import (
	"html/template"
	"log"
	"net"
	"os"
)


var templateStr = `
{{ block "header" .}} default header {{ end }}
{{ block "body" .}} default body {{ end }}
{{ block "footer" .}}{{ end }}
`

var header1 = `{{ define "header" }} this is {{ .header }} {{ end }}`
var header2 = `{{ define "header" }} this is header2 {{ end }}`

var body1 = `{{ define "body" }} this is {{ .body }} {{ end }}`
var body2 = `{{ define "body" }} this is body2 {{ end }}`

var footer1 = `{{ define "footer" }} this is {{ .footer }} {{ end }}`
var footer2 = `{{ define "footer" }} this is footer2 {{ end }}`

func main() {
	params := make(map[string]string)
	params["header"] = "map header"
	params["body"] = "map body"
	params["footer"] = "map footer"

	paramsBlank := make(map[string]string)
	paramsBlank["header"] = ""
	paramsBlank["body"] = ""
	paramsBlank["footer"] = ""

	tmpl, err := template.New("test_template").Parse(templateStr)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("---- define 1 ----")
	tmpl1, _ := tmpl.Clone()
	tmpl1.Parse(header1)
	tmpl1.Parse(body1)
	tmpl1.Parse(footer1)
	tmpl1.Execute(os.Stdout, params)

	log.Println("---- define 2 ----")
	tmpl2, _ := tmpl.Clone()
	tmpl2.Parse(header2)
	tmpl2.Parse(body2)
	tmpl2.Parse(footer2)
	tmpl2.Execute(os.Stdout, params)

	log.Println("---- define chaos ----")
	tmpl3, _ := tmpl.Clone()
	tmpl3.Parse(header2)
	tmpl3.Parse(body2)
	tmpl3.Parse(body1)
	tmpl3.Parse(footer2)
	tmpl3.Execute(os.Stdout, paramsBlank)

	log.Println("---- define chaos nil ----")
	tmpl4, _ := tmpl.Clone()
	tmpl4.Parse(header2)
	tmpl4.Parse(body2)
	tmpl4.Parse(body1)
	tmpl4.Parse(footer2)
	tmpl4.Execute(os.Stdout, nil)

	log.Println("---- No define ----")
	tmpl.Execute(os.Stdout, nil)

	/////
	addrs, err := net.InterfaceAddrs()
	for _, addr := range addrs {
		log.Println(addr)
	}
}

