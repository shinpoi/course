package main

import (
	"fmt"
	"gitlab.com/golang-commonmark/markdown"
)

var markdownString = `
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

<h1 class="someClass"> html tag test </h1>
<p class="someClass"> html tag test </p>
<script type="xxx" src="yyy"> html tag test </script>
`

func main() {
	// out put XHTML & allow raw HTML
	md := markdown.New(markdown.XHTMLOutput(true), markdown.HTML(true))
	fmt.Println(md.RenderToString([]byte(markdownString)))
}
