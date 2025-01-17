# Simulated Linux Terminal for Windows

This project simulates a basic Linux-like terminal environment on a Windows system. It includes a range of commands, including file management, git version control, and terminal operations.

## Features

- **File Operations**: Supports basic commands like `ls`, `pwd`, `cd`, `touch`, `mkdir`, `rm`, and more.
- **Permissions & Ownership**: Change file permissions and ownership using `chmod` and `chown`.
- **Archive Management**: Create and extract tar archives using `tar`.
- **Git Integration**: Supports git commands like `git init`, `git add`, `git commit`, `git push`, and more.
- **Terminal Operations**: Clear the terminal, open Vim in a new terminal window, and more.
- **Color-Coded Output**: Different file types and directories are displayed in different colors for better readability.

## Commands

### File & Directory Operations

- `cd <path>`: Change to the specified directory.
- `pwd`: Print the current working directory.
- `ls`: List files in the current directory.
- `cat <filename>`: Display the contents of the specified file.
- `touch <filename>`: Create a new empty file.
- `mkdir <dirname>`: Create a new directory.
- `rmdir <dirname>`: Remove an empty directory.
- `rm <filename>`: Remove the specified file.
- `cp <src> <dest>`: Copy a file from `<src>` to `<dest>`.
- `mv <src> <dest>`: Move a file from `<src>` to `<dest>`.

### Permissions & Ownership

- `chmod <permissions> <filename>`: Change the permissions of a file.
- `chown <owner> <filename>`: Change the ownership of a file.
- `chown <owner> <group> <filename>`: Change the ownership to `<owner>:<group>`.

### Archiving

- `tar -cvf <archive_name> <files>`: Create a tar archive of the specified files.
- `tar -xvf <archive_name>`: Extract a tar archive.

### Git Operations

- `git init`: Initialize a git repository.
- `git add <files>`: Add files to the git staging area.
- `git commit -m <message>`: Commit changes to the repository.
- `git push`: Push changes to the remote repository.
- `git status`: Check the status of the git repository.
- `git log`: View the git commit log.

### Terminal Operations

- `clear`: Clear the terminal screen.
- `vim`: Start Vim in a new terminal window.
- `help` or `h`: Display the help message.

## License

This project is licensed under the MIT License. See the full license text below:

```plaintext
MIT License

Copyright (c) 2024-2025 Ralph King

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```