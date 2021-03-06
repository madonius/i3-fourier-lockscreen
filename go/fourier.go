package main

import (
	"flag"
	"fmt"
	"github.com/mjibson/go-dsp/fft"
	"image"
	"image/color"
	"image/png"
	_ "image/png"
	"log"
	"math"
	"math/cmplx"
	"os"
)

func main() {
	var input_file string
	var output_file string
	var radius float64

	flag.StringVar(&input_file, "input-file", "", "The imagefile(PNG) that will be converted")
	flag.StringVar(&output_file, "output-file", "", "The file where the output will be written to")
	flag.Float64Var(&radius, "radius", 0.2, "The radius that is going to be cut off (e.g. 0.1)")

	flag.Parse()

	reader, err := os.Open(input_file)
	if err != nil {
		log.Fatal(err)
	}

	m, _, err := image.Decode(reader)
	if err != nil {
		log.Fatal(err)
	}
	bounds := m.Bounds()

	x_size := bounds.Max.X - bounds.Min.X
	y_size := bounds.Max.Y - bounds.Min.Y

	red := make([][]float64, x_size)
	for i := range red {
		red[i] = make([]float64, y_size)
	}

	green := make([][]float64, x_size)
	for i := range green {
		green[i] = make([]float64, y_size)
	}

	blue := make([][]float64, x_size)
	for i := range blue {
		blue[i] = make([]float64, y_size)
	}

	alpha := make([][]float64, x_size)
	for i := range alpha {
		alpha[i] = make([]float64, y_size)
	}

	// Split the image to it's separate components
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, a := m.At(x, y).RGBA()
			red[x][y] = float64(r)
			green[x][y] = float64(g)
			blue[x][y] = float64(b)
			alpha[x][y] = float64(a)
		}
	}

	defer reader.Close()
	redfft := fft.FFT2Real(red)
	greenfft := fft.FFT2Real(green)
	bluefft := fft.FFT2Real(blue)
	alphafft := fft.FFT2Real(alpha)

	xhalf := (bounds.Max.X - bounds.Min.X) / 2.0
	yhalf := (bounds.Max.Y - bounds.Min.Y) / 2.0

	fft_image := image.NewRGBA(image.Rect(bounds.Min.X, bounds.Min.Y, bounds.Max.X, bounds.Max.Y))
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			d := math.Sqrt(math.Pow(float64(x-xhalf), 2)+math.Pow(float64(y-yhalf), 2)) - float64(xhalf)*radius
			if d < 0 {
				redfft[x][y] = 0
				greenfft[x][y] = 0
				bluefft[x][y] = 0
				alphafft[x][y] = 0
			} else {
				fft_image.Set(x, y,
					color.RGBA{
						uint8(100 * cmplx.Abs(redfft[x][y])),
						uint8(100 * cmplx.Abs(greenfft[x][y])),
						uint8(100 * cmplx.Abs(bluefft[x][y])),
						uint8(100 * cmplx.Abs(alphafft[x][y])),
					},
				)
			}
		}
	}

	out_image := image.NewRGBA(image.Rect(bounds.Min.X, bounds.Min.Y, bounds.Max.X, bounds.Max.Y))
	redifft := fft.IFFT2(redfft)
	greenifft := fft.IFFT2(greenfft)
	blueifft := fft.IFFT2(bluefft)
	alphaifft := fft.IFFT2(alphafft)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			out_image.Set(x, y,
				color.RGBA{
					uint8(cmplx.Abs(redifft[x][y])),
					uint8(cmplx.Abs(greenifft[x][y])),
					uint8(cmplx.Abs(blueifft[x][y])),
					uint8(cmplx.Abs(alphaifft[x][y])),
				},
			)
		}
	}

	fmt.Println("Hi!")
	f, err := os.Create(output_file)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	if err := png.Encode(f, out_image); err != nil {
		log.Fatal(err)
	}
}
