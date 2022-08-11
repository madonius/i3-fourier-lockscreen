use gumdrop::Options;

// Defines options that can be parsed from the command line.
//
// `derive(Options)` will generate an implementation of the trait `Options`.
// Each field must either have a `Default` implementation or an inline
// default value provided.
//
// (`Debug` is derived here only for demonstration purposes.)
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
    let opts = FourierOptions::parse_args_default_or_exit();
    println!("{:#?}", opts);
}
