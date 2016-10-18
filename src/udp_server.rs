use std::net::UdpSocket;
use std::net::IpAddr;
use std::io::Error;
use std::string::String;
use std::time;


fn int_to_char(byte_array: &[u8; 255]) -> String{
    //clean trailing 0s
    let mut new_vec = Vec::new();
    for i in byte_array.iter(){
        if *i != 0 {
            new_vec.push(*i);
        }
    }

    String::from_utf8(new_vec).unwrap()
}

pub fn socket_response(listen_addr: &str, listen_port: i32) -> Result<(), Error> {

    let bind_addr = format!("{}:{}", listen_addr, listen_port);
    let socket = try!(UdpSocket::bind(&bind_addr.as_str()));
    println!("{:?}", socket);

    loop {
        // read from the socket
        let mut buf = [0; 255];
        let (amt, src) = try!(socket.recv_from(&mut buf));

        let message = int_to_char(&buf);
        println!("{:?}", &message);
        println!("{:?}", src);

        // send a reply to the socket we received data from
        let buf = &mut buf[..amt];
        buf.reverse();
        try!(socket.send_to(buf, &src));

        // quit if instructed to do so
        // "&" in front of message converts String type to &str type
        if &message == "QUIT"{
            break;
        }
    }
    Ok(())
}   // the socket is closed here



#[allow(unused_variables)]
pub fn socket_send(data_to_send:&[u8]) -> Result<(), Error> {

    let socket = try!(UdpSocket::bind("0.0.0.0:0"));
    try!(socket.set_broadcast(true));

    try!(socket.send_to(&data_to_send, "255.255.255.255:13389"));

    let mut buf = [0; 255];
    let (amt, src) = try!(socket.recv_from(&mut buf));
    //println!("{:?}", buf);
    println!("Response From: {:?}", src);

    Ok(())
}   // the socket is closed here


#[allow(unused_variables)]
pub fn find_instruments() -> Result<(), Error> {

    let socket = try!(UdpSocket::bind("0.0.0.0:0"));
    try!(socket.set_broadcast(true));

    try!(socket.send_to(b"PING", "255.255.255.255:13389"));

    let mut buf = [0; 255];
    let mut device_list = Vec::new();
    socket.set_read_timeout(Some(time::Duration::from_secs(5)));
    loop {
        let socket_result = socket.recv_from(&mut buf);
        match socket_result {
            Ok((amt,src)) => {
                match src.ip() {
                    IpAddr::V4(ip) => {
                        let ip_str = format!("{}.{}.{}.{}",ip.octets()[0],ip.octets()[1],ip.octets()[2],ip.octets()[3]);
                        let name_str = int_to_char(&buf);
                        device_list.push(format!("{}=>{}",name_str,ip_str));
                    },
                    IpAddr::V6(ip) => {
                        let ip_str = format!("{}:{}:{}:{}:{}:{}:{}:{}",ip.segments()[0],ip.segments()[1],ip.segments()[2],ip.segments()[3],ip.segments()[4],ip.segments()[5],ip.segments()[6],ip.segments()[7]);
                        let name_str = int_to_char(&buf);
                        device_list.push(format!("{}=>{}",name_str,ip_str));
                    },
                }
            },
            Err(_) => break,
        };

    }
    //Print out any found instruments
    println!("{}",device_list.as_slice().join(","));
    Ok(())
}
