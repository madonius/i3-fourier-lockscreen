use gumdrop::Options;

// Defines options that can be parsed from the command line.
//
// `derive(Options)` will generate an implementation of the trait `Options`.
// Each field must either have a `Default` implementation or an inline
// default value provided.
//
// (`Debug` is derived here only for demonstration purposes.)
#[derive(Debug, Options)]
struct Options {
    #[options()]

    #[options(free)]
    free: Vec<String>,

    #[options(help = "print help message")]
    help: bool,

    #[options(help = "give a string argument")]
    string: Option<String>,

    #[options(help = "give a number as an argument", meta = "N")]
    number: Option<i32>,

    #[options(help = "give a list of string items")]
    item: Vec<String>,

    #[options(count, help = "increase a counting value")]
    count: u32,

    #[options(no_short, help = "this option has no short form")]
    long_option_only: bool,
}

fn main() {
    let opts = Options::parse_args_default_or_exit();
    println!("{:#?}", opts);
}
