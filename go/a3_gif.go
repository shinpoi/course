package main

import (
	"image"
	"image/color"
	"image/gif"
	"io"
	"math"
	"math/rand"
	"os"
)

var palette = []color.Color{color.Black, color.White,
	color.RGBA{0xFF, 0, 0, 0xFF},
	color.RGBA{0, 0xFF, 0, 0xFF},
	color.RGBA{0, 0, 0xFF, 0xFF}}

const (
	whiteIndex = 1 // next color in palette
	redIndex   = 2 // first color in palette
	greenIndex = 3 // first color in palette
	blueIndex  = 4 // first color in palette
)

const (
	cycles  = 5
	res     = 0.001
	size    = 100
	nframes = 64
	delay   = 8
)

var freq = rand.Float64() * 3

func main() {
	lissajous(os.Stdout)
}

func lissajous(out io.Writer) {
	anim := gif.GIF{LoopCount: nframes}
	phase := 0.0
	for i := 0; i < nframes; i++ {
		rect := image.Rect(0, 0, 2*size+1, 2*size+1)
		img := image.NewPaletted(rect, palette)
		paint(img, whiteIndex, 0.0, cycles*math.Pi/2, phase)
		paint(img, redIndex, cycles*math.Pi/2, cycles*math.Pi, phase)
		paint(img, greenIndex, cycles*math.Pi, cycles*math.Pi*1.5, phase)
		paint(img, blueIndex, cycles*math.Pi*1.5, cycles*math.Pi*2, phase)
		phase += 0.1
		anim.Delay = append(anim.Delay, delay)
		anim.Image = append(anim.Image, img)
	}
	gif.EncodeAll(out, &anim)
}

func paint(img *image.Paletted, index uint8, st float64, end float64, phase float64) {
	for t := st; t < end; t += res {
		x := math.Cos(t)
		y := math.Cos(t*freq + phase)
		img.SetColorIndex(size+int(x*size+0.5), size+int(y*size+0.5), index)
	}
}
