import os
import stat
import shutil
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

BLUE = '\033[34m'
GREEN = '\033[32m'
CYAN = '\033[36m'
YELLOW_ON_BLACK = '\033[43m\033[30m'
MAGENTA = '\033[35m'
RED = '\033[31m'
RED_ON_BLACK = '\033[41m\033[37m'
RESET = '\033[0m'

def show_help():
    """Display available commands."""
    help_text = """
    Available commands:
    - cd <path>: Change directory to <path>
    - pwd: Print the current working directory
    - ls: List files in the current directory
    - cat <filename>: Display contents of the specified file
    - touch <filename>: Create a new file with the specified name
    - mkdir <dirname>: Create a new directory with the specified name
    - rmdir <dirname>: Remove the specified directory
    - rm <filename>: Remove the specified file
    - cp <src> <dest>: Copy file from <src> to <dest>
    - mv <src> <dest>: Move file from <src> to <dest>
    - chmod <permissions> <filename>: Change permissions of the specified file
    - chown <owner> <filename>: Change ownership of the specified file to <owner>
    - chown <owner> <group> <filename>: Change ownership of the specified file to <owner>:<group>
    - tar -cvf <archive_name> <files>: Create a tar archive of specified files
    - tar -xvf <archive_name>: Extract a tar archive
    - clear: Clear the terminal screen
    - vim: Start Vim in a new terminal window
    - help: Show this help message
    """
    print(help_text)

def complete_cd(text):
    """Tab completion for the cd command."""
    current_dir = os.getcwd()
    options = [f for f in os.listdir(current_dir) if f.startswith(text)]
    return options

def execute_git_command(command):
    """Execute git commands."""
    commands = {
        'git init': ['git', 'init'],
        'git status': ['git', 'status'],
        'git log': ['git', 'log'],
        'git push': ['git', 'push']
    }

    if command.startswith('git add '):
        files = command[8:].strip().split(' ')
        commands['git add'] = ['git', 'add'] + files
    elif command.startswith('git commit '):
        message = command[11:].strip()
        commands['git commit'] = ['git', 'commit', '-m', message]

    for cmd, args in commands.items():
        if command.startswith(cmd):
            result = subprocess.run(args, shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
            return

    print("Error: Unsupported git command.")

def execute_command(command):
    """Execute shell commands."""
    try:
        if command.startswith('cd '):
            os.chdir(command[3:].strip())
        elif command == 'pwd':
            print(os.getcwd())
        elif command == 'ls':
            list_directory()
        elif command.startswith('cat '):
            display_file_content(command[4:].strip())
        elif command.startswith('touch '):
            create_file(command[6:].strip())
        elif command.startswith('mkdir '):
            create_directory(command[6:].strip())
        elif command.startswith('rmdir '):
            remove_directory(command[6:].strip())
        elif command.startswith('rm '):
            remove_file(command[3:].strip())
        elif command.startswith('cp '):
            copy_file(command)
        elif command.startswith('mv '):
            move_file(command)
        elif command.startswith('chmod '):
            change_permissions(command)
        elif command.startswith('chown '):
            change_ownership(command)
        elif command.startswith('tar '):
            handle_tar(command)
        elif command in ['help', 'h']:
            show_help()
        elif command == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command.startswith('vim'):
            subprocess.run(["start", "cmd", "/K", "vim"], shell=True)
            print("Vim started in new background terminal.")
        elif command.startswith('git '):
            execute_git_command(command)
        else:
            run_external_command(command)
    except Exception as e:
        print(f"Error: {e}")

def list_directory():
    """List files in the current directory with color coding."""
    for item in os.listdir(os.getcwd()):
        file_path = os.path.join(os.getcwd(), item)
        color = get_file_color(file_path, item)
        print(f"{color}{item}{RESET}", end='   ')
    print()

def get_file_color(file_path, item):
    """Determine the color for the file based on its type."""
    if os.path.isdir(file_path):
        return BLUE
    elif stat.S_ISBLK(os.stat(file_path).st_mode) or stat.S_ISCHR(os.stat(file_path).st_mode):
        return YELLOW_ON_BLACK
    elif item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
        return MAGENTA
    elif item.lower().endswith(('.tar', '.gz', '.zip', '.rar', '.bz2', '.7z')):
        return RED
    elif os.access(file_path, os.X_OK):
        return GREEN
    elif os.path.islink(file_path):
        return RED_ON_BLACK if not os.path.exists(file_path) else CYAN
    return RESET

def display_file_content(filename):
    """Display the contents of a file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            print(file.read())
    else:
        print(f"Error: '{filename}' not found.")

def create_file(filename):
    """Create a new file."""
    with open(filename, 'a'):
        pass
    print(f"File '{filename}' created (if it did not already exist).")

def create_directory(dirname):
    """Create a new directory."""
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        print(f"Directory '{dirname}' created.")
    else:
        print(f"Error: Directory '{dirname}' already exists.")

def remove_directory(dirname):
    """Remove a directory."""
    if os.path.isdir(dirname):
        os.rmdir(dirname)
        print(f"Directory '{dirname}' removed.")
    else:
        print(f"Error: Directory '{dirname}' not found.")

def remove_file(filename):
    """Remove a file."""
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' removed.")
    else:
        print(f"Error: File '{filename}' not found.")

def copy_file(command):
    """Copy a file from source to destination."""
    parts = command.split(' ', 2)
    if len(parts) == 3:
        src, dest = parts[1], parts[2]
        if os.path.exists(src):
            shutil.copy(src, dest)
            print(f"Copied '{src}' to '{dest}'.")
        else:
            print(f"Error: Source file '{src}' not found.")
    else:
        print("Error: Invalid arguments for cp.")

def move_file(command):
    """Move a file from source to destination."""
    parts = command.split(' ', 2)
    if len(parts) == 3:
        src, dest = parts[1], parts[2]
        if os.path.exists(src):
            shutil.move(src, dest)
            print(f"Moved '{src}' to '{dest}'.")
        else:
            print(f"Error: Source file '{src}' not found.")
    else:
        print("Error: Invalid arguments for mv.")

def change_permissions(command):
    """Change file permissions."""
    parts = command.split(' ', 2)
    if len(parts) == 3:
        permissions, filename = parts[1], parts[2]
        if os.path.exists(filename):
            os.chmod(filename, int(permissions, 8))
            print(f"Permissions of '{filename}' changed to {permissions}.")
        else:
            print(f"Error: File '{filename}' not found.")
    else:
        print("Error: Invalid arguments for chmod.")

def change_ownership(command):
    """Change file ownership."""
    parts = command.split(' ', 3)
    if len(parts) == 3:
        owner, filename = parts[1], parts[2]
        if os.path.exists(filename):
            shutil.chown(filename, owner)
            print(f"Ownership of '{filename}' changed to {owner}.")
        else:
            print(f"Error: File '{filename}' not found.")
    elif len(parts) == 4:
        owner, group, filename = parts[1], parts[2], parts[3]
        if os.path.exists(filename):
            shutil.chown(filename, owner, group)
            print(f"Ownership of '{filename}' changed to {owner}:{group}.")
        else:
            print(f"Error: File '{filename}' not found.")
    else:
        print("Error: Invalid arguments for chown.")

def handle_tar(command):
    """Handle tar operations."""
    parts = command.split(' ', 3)
    if len(parts) >= 3:
        if parts[1] == '-cvf':
            create_tar_archive(parts[2], parts[3])
        elif parts[1] == '-xvf':
            extract_tar_archive(parts[2])
        else:
            print("Error: Invalid tar operation.")
    else:
        print("Error: Invalid arguments for tar.")

def create_tar_archive(archive_name, files):
    """Create a tar archive."""
    if not os.path.exists(files):
        print(f"Error: File or directory '{files}' does not exist.")
    else:
        shutil.make_archive(archive_name, 'zip', files)
        os.rename(f"{archive_name}.zip", f"{archive_name}.tar")
        print(f"Created archive '{archive_name}.tar' with files: {files}.")

def extract_tar_archive(archive_name):
    """Extract a tar archive."""
    if os.path.exists(archive_name):
        shutil.unpack_archive(archive_name, archive_name.replace('.tar', ''))
        print(f"Extracted archive '{archive_name}'.")
    else:
        print(f"Error: Archive '{archive_name}' not found.")

def run_external_command(command):
    """Run an external command."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)

def main():
    """Main function to run the terminal."""
    print("Welcome to the simulated Linux terminal for Windows!")

    while True:
        cwd = os.getcwd()
        prompt_text = f"{cwd}$ "
        
        completer = WordCompleter(complete_cd(''), ignore_case=True)
        command = prompt(prompt_text, completer=completer).strip()

        if command.lower() == 'exit':
            print("Exiting terminal.")
            break
        else:
            execute_command(command)

if __name__ == "__main__":
    main()