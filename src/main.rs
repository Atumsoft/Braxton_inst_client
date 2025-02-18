extern crate getopts;
use getopts::Options;
use std::env;
use std::path;
use std::fs;
use std::io;
use std::io::Write;
pub mod udp_server;

fn print_args_usage(program_name: &str, options: Options) {
    let brief = format!("Usage: {} [options]", program_name);
    print!("{}", options.usage(&brief));
}

fn open_file(file_path: String) -> Result<fs::File, io::Error> {
    Ok(try!(fs::File::create(&file_path)))
}

#[allow(unused_variables)]
pub fn main() {
    let raw_args: Vec<String> = env::args().collect();
    let program_name = raw_args[0].clone();

    let mut accepted_program_options = Options::new();
    accepted_program_options.optflag("h","help","Find out all the cool things this program can do!");
    accepted_program_options.optflag("f", "find-instruments", "Search and list all discovered instruments.");
    accepted_program_options.optopt("c","connect", "Connect to instrument at address", "ADDRESS");
    accepted_program_options.optopt("o","output-file", "File to output filtered CSV to", "FILE");
    accepted_program_options.optopt("s","start-filter", "Beginning date to filter CSV data on", "MM/DD/YYYY");
    accepted_program_options.optopt("e","end-filter", "Ending date to filter CSV data on", "MM/DD/YYYY");
    let found_options = match accepted_program_options.parse(&raw_args[1..]) {
        Ok(matches) => {matches}
        Err(failure) => {panic!(failure.to_string())}
    };
    if found_options.opt_present("h") {
        print_args_usage(&program_name, accepted_program_options);
        return;
    }

    else if found_options.opt_present("f") {
        udp_server::find_instruments();
        return;
    }

    else if found_options.opt_present("c") {
        let start_date = found_options.opt_str("s").unwrap();
        let end_date = found_options.opt_str("e").unwrap();
        let output_file_path = found_options.opt_str("o").unwrap();
        let ip_addr = found_options.opt_str("c").unwrap();

        //Check if file exists. Don't overwrite existing file and instead exit.
        if path::Path::new(&output_file_path).exists() {
            println!("File already exists. Please specify another file.");
            std::process::exit(1);
        }

        //Create file and open for writing.
        let output_file = open_file(output_file_path);

        match output_file {
            Ok(mut file) => {
                let date_range = format!("{}-{}", start_date, end_date);
                let data = udp_server::request_csv(ip_addr, date_range).unwrap();
                file.write(data.as_slice());
            },
            Err(fail) => {},
        }

        return;
    }

    else {
        print_args_usage(&program_name, accepted_program_options);
        return;
    }
}