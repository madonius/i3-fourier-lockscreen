use gumdrop::Options;
use fft2d::slice::{fft_2d, fftshift, ifft_2d, ifftshift};
use image::*;
use rustfft::num_complex::Complex;
use std::path::Path;
use num;

#[derive(Debug, Options)]
struct FourierOptions {
    #[options(help = "The imagefile(PNG) that will be converted")]
    input_file: Option<String>,
    
    #[options(help = "The file where the output will be written to")]
    output_file: Option<String>,

    #[options(help = "Print this help message")]
    help: bool,
}

fn main() {
    let radius = 0.54;
    let opts = FourierOptions::parse_args_default_or_exit();

    let img = image::open(&Path::new(&opts.input_file.unwrap())).unwrap().to_luma8();
    let (width, height) = img.dimensions();

    // Convert the image buffer to complex numbers to be able to compute the FFT.
    let mut img_buffer: Vec<Complex<f64>> = img
        .into_raw()
        .iter()
        .map(|&pix| Complex::new(pix as f64 / 255.0, 0.0))
        .collect();


    fft_2d(width as usize, height as usize, &mut img_buffer);

   

    let x_center = width/2;
    let y_center = height/2;

    for x in 1..width {
        for y in 1..height {
            if  ((x.abs_diff(x_center).pow(2) + y.abs_diff(y_center).pow(2)) as f64) < radius*radius*((width*width) as f64) {
               img_buffer[coord_to_raw(x,y,width) as usize] = 
                   num::complex::Complex::new(0.0, 0.0); 
            }
        }
    }

    img_buffer = fftshift(height as usize, width as usize, &img_buffer);
    
    img_buffer = ifftshift(height as usize, width as usize, &img_buffer);

    ifft_2d(height as usize, width as usize, &mut img_buffer);

    let fft_coef = 1.0 / (width * height) as f64;
    for x in img_buffer.iter_mut() {
        *x *= fft_coef;
    }

    let img_raw: Vec<u8> = img_buffer
        .iter()
        .map(|c| 255 - (c.norm().min(1.0) * 255.0) as u8)
        .collect();

    let out_img = GrayImage::from_raw(width, height, img_raw).unwrap();

    out_img.save(&Path::new(&opts.output_file.unwrap())).unwrap();
}

fn coord_to_raw(x: u32, y: u32, width: u32) -> u32 {
    let array_pos = (y-1)*width+x;
    return array_pos;
}
