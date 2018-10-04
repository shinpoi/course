package main

import (
	"fmt"
	"gitlab.com/golang-commonmark/markdown"
)

var markdownString =
`
# Title

### subsub Title

- 1
- 2
  - a
  - b
  - c

Title2
===========

---

* o1
* o2
* o3

|name |value |
|-----|------|
|n1   |v1    |
|n2   |v2    |
|n3   |v2    |
`

func main() {
	md := markdown.New(markdown.XHTMLOutput(true))
	fmt.Println(md.RenderToString([]byte(markdownString)))
}
