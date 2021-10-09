package main

import (
	"flag"
	"github.com/mjibson/go-dsp/dsputils"
	"github.com/mjibson/go-dsp/fft"
	"github.com/nfnt/resize"
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
	log.Println("Hi")

	var input_file string
	var output_file string
	var radius float64
	var final_size uint

	flag.StringVar(&input_file, "input-file", "", "The imagefile(PNG) that will be converted")
	flag.StringVar(&output_file, "output-file", "", "The file where the output will be written to")
	flag.Float64Var(&radius, "radius", 0.2, "The radius that is going to be cut off (e.g. 0.1)")
	flag.UintVar(&final_size, "final-size", 0, "The final size of the image, if 0 the original size will be used")
	flag.Parse()

	log.Println("Parsed the flags")

	reader, err := os.Open(input_file)
	if err != nil {
		log.Fatal(err)
	}

	orig_m, _, err := image.Decode(reader)
	if err != nil {
		log.Fatal(err)
	}

	m := orig_m
	if final_size > 0 {
		m = resize.Resize(final_size, 0, orig_m, resize.Bicubic)
	}

	bounds := m.Bounds()
	log.Println("Read the image file")

	x_size := bounds.Max.X - bounds.Min.X
	y_size := bounds.Max.Y - bounds.Min.Y
	log.Printf("Image size %d %d", x_size, y_size)

	img_mtrx := dsputils.MakeEmptyMatrix([]int{1, x_size, y_size})

	log.Println("Generated the empty matrix")

	// Split the image to it's separate components
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, b, g, a := m.At(x, y).RGBA()
			img_mtrx.SetValue(complex((float64(a)/255.)*(float64(r)+float64(b)+float64(g))/3., 0), []int{0, x, y})
		}
	}

	log.Println("Read the image")

	defer reader.Close()
	img_fft := fft.FFTN(img_mtrx)
	log.Println("Fourier transformed the image")

	xhalf := x_size / 2.0
	yhalf := y_size / 2.0

	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			d := math.Sqrt(math.Pow(float64(x-xhalf), 2)+math.Pow(float64(y-yhalf), 2)) - float64(xhalf)*radius
			if d > 0 {
				img_fft.SetValue(complex(0, 0), []int{0, x, y})
			}
		}
	}

	log.Println("Wiped the central area")

	out_image := image.NewRGBA(image.Rect(bounds.Min.X, bounds.Min.Y, bounds.Max.X, bounds.Max.Y))
	img_ifft := fft.IFFTN(img_fft)
	log.Println("Inverted the fourier transform")
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			out_image.Set(x, y,
				color.RGBA{
					uint8(cmplx.Abs(img_ifft.Value([]int{0, x, y}))),
					uint8(cmplx.Abs(img_ifft.Value([]int{0, x, y}))),
					uint8(cmplx.Abs(img_ifft.Value([]int{0, x, y}))),
					uint8(0xff),
				},
			)
		}
	}
	log.Println("Read the inverse fourier to the image buffer")

	f, err := os.Create(output_file)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	if err := png.Encode(f, out_image); err != nil {
		log.Fatal(err)
	}
	log.Println("Wrote the image")
	log.Println("Bye!")
}
