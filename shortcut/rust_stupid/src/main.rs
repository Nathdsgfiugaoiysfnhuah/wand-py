use std::process::Command;

fn main() {
    Command::new("cmd")
        .args([
            "/C",
            "cd",
            r"C:\Users\natha\Documents\code\wand-py",
            "&&",
            "python",
            "./main.py",
        ])
        .spawn()
        .expect("failed to execute process");
}
