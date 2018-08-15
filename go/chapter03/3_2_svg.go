package main

import (
	"fmt"
	"math"
)

const (
	width, height = 1000, 560           // pixel
	cells         = 100                 // number
	xyrange       = 30.0                // number
	xyscale       = width / 2 / xyrange // pixel
	zscale        = height * 0.4        // pixel
	angle30       = math.Pi / 6         // 30
)

var sin30, cos30 = math.Sin(angle30), math.Cos(angle30)

func main() {
	fmt.Printf("<svg xmlns='http://www.w3.org/2000/svg' "+
		"style='stroke: grey; fill: white; stroke-width: 0.7' "+
		"width='%d' height='%d'>\n", width, height)

	for i := 0; i < cells; i++ {
		for j := 0; j < cells; j++ {
			ax, ay, _ := corner(i+1, j)
			bx, by, color := corner(i, j)
			cx, cy, _ := corner(i, j+1)
			dx, dy, _ := corner(i+1, j+1)
			fmt.Printf("<polygon points='%g,%g %g,%g %g,%g %g,%g' stroke='%s'/>\n",
				ax, ay, bx, by, cx, cy, dx, dy, color)
		}
	}
	fmt.Println("</svg>")
}

func corner(i, j int) (float64, float64, string) {
	x := xyrange * (float64(i)/cells - 0.5)
	y := xyrange * (float64(j)/cells - 0.5)
	z := f(x, y)

	sx := width/2 + (x-y)*cos30*xyscale
	sy := height/2 + (x+y)*sin30 - z*zscale
	return sx, sy, color(z)
}

func f(x, y float64) float64 {
	r := math.Hypot(x, y)
	return math.Sin(r) / r

}

func color(z float64) string {
	z += 0.4
	if z < 0 {
		return fmt.Sprint("#000000")
	} else if z > 1 {
		return fmt.Sprint("#ff0000")
	} else if z >= 0.5 {
		return fmt.Sprintf("#%2.2x0000", int((z-0.5)*2*0xff))
	} else {
		return fmt.Sprintf("#0000%2.2x", int(z*2*0xff))
	}
}
