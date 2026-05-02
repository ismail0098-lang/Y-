fn main() {
    let source = "a=5; r a;";
    println!("Compiling: {}", source);
    println!("-----------------------------------");

    let mut chars = source.chars().peekable();
    while let Some(&c) = chars.peek() {
        if c.is_whitespace() {
            chars.next();
            continue;
        }

        if c.is_alphabetic() && chars.clone().nth(1) == Some('=') {
            let var = c;
            let offset = (var as u8 - b'a') * 4;
            chars.next(); // skip var
            chars.next(); // skip '='
            
            while let Some(&next) = chars.peek() {
                if next.is_whitespace() { chars.next(); } else { break; }
            }
            
            if let Some(&val_char) = chars.peek() {
                if val_char.is_digit(10) {
                    let val = val_char.to_digit(10).unwrap();
                    println!("MOV_CONST       : C7 41 {:02X} {:02X} 00 00 00", offset, val);
                    chars.next();
                }
            }
            if chars.peek() == Some(&';') { chars.next(); }
        } else if c == 'r' {
            chars.next(); // skip 'r'
            while let Some(&next) = chars.peek() {
                if next.is_whitespace() { chars.next(); } else { break; }
            }
            if let Some(&var) = chars.peek() {
                let offset = (var as u8 - b'a') * 4;
                println!("LOAD_EAX        : 8B 41 {:02X}", offset);
                println!("RET             : C3");
                chars.next();
            }
            if chars.peek() == Some(&';') { chars.next(); }
        } else {
            chars.next();
        }
    }
}
