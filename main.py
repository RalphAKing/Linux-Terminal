import os
import stat
import shutil
import subprocess

BLUE = '\033[34m'
GREEN = '\033[32m'
CYAN = '\033[36m'
YELLOW_ON_BLACK = '\033[43m\033[30m'
MAGENTA = '\033[35m'
RED = '\033[31m'
RED_ON_BLACK = '\033[41m\033[37m'
RESET = '\033[0m'

def show_help():
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

def execute_git_command(command):
    try:
        if command.startswith('git init'):
            result = subprocess.run(['git', 'init'], shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")

        elif command.startswith('git add '):
            files = command[8:].strip().split(' ')
            result = subprocess.run(['git', 'add'] + files, shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")

        elif command.startswith('git commit '):
            message = command[11:].strip()
            result = subprocess.run(['git', 'commit', '-m', message], shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")

        elif command == 'git status':
            result = subprocess.run(['git', 'status'], shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")

        elif command.startswith('git log'):
            result = subprocess.run(['git', 'log'], shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
        elif command.startswith('git push'):
            result = subprocess.run(['git', 'push'], shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")

        else:
            print("Error: Unsupported git command.")
    except Exception as e:
        print(f"Error: {e}")


def execute_command(command):
    try:
        if command.startswith('cd '):
            path = command[3:].strip()
            os.chdir(path)
        elif command == 'pwd':
            print(os.getcwd())
        elif command == 'ls':
            for item in os.listdir(os.getcwd()):
                file_path = os.path.join(os.getcwd(), item)
                color = RESET
                if os.path.isdir(file_path):
                    color = BLUE
                elif stat.S_ISBLK(os.stat(file_path).st_mode) or stat.S_ISCHR(os.stat(file_path).st_mode): 
                    color = YELLOW_ON_BLACK
                elif item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):  
                    color = MAGENTA
                elif item.lower().endswith(('.tar', '.gz', '.zip', '.rar', '.bz2', '.7z')):  
                    color = RED
                elif os.access(file_path, os.X_OK):  
                    color = GREEN
                elif os.path.islink(file_path):  
                    if not os.path.exists(file_path): 
                        color = RED_ON_BLACK
                    else:
                        color = CYAN

                print(f"{color}{item}{RESET}", end='   ')
            print()

        elif command.startswith('cat '): 
            filename = command[4:].strip()
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    print(file.read())
            else:
                print(f"Error: '{filename}' not found.")
        elif command.startswith('touch '): 
            filename = command[6:].strip()
            with open(filename, 'a'):
                pass  
            print(f"File '{filename}' created (if it did not already exist).")
        elif command.startswith('mkdir '): 
            dirname = command[6:].strip()
            if not os.path.exists(dirname):
                os.mkdir(dirname)
                print(f"Directory '{dirname}' created.")
            else:
                print(f"Error: Directory '{dirname}' already exists.")
        elif command.startswith('rmdir '): 
            dirname = command[6:].strip()
            if os.path.isdir(dirname):
                os.rmdir(dirname)
                print(f"Directory '{dirname}' removed.")
            else:
                print(f"Error: Directory '{dirname}' not found.")
        elif command.startswith('rm '): 
            filename = command[3:].strip()
            if os.path.exists(filename):
                os.remove(filename)
                print(f"File '{filename}' removed.")
            else:
                print(f"Error: File '{filename}' not found.")
        elif command.startswith('cp '):  
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
        elif command.startswith('mv '):  
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
        elif command.startswith('chmod '):  
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
        elif command.startswith('chown '): 
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


        elif command.startswith('tar '): 
            parts = command.split(' ', 3)
            if len(parts) >= 3:
                if parts[1] == '-cvf': 
                    if len(parts) >= 4:
                        _, archive_name, files = parts[1], parts[2], parts[3]
                        if not os.path.exists(files):
                            print(f"Error: File or directory '{file}' does not exist.")
                        else:
                            shutil.make_archive(archive_name, 'zip', files)
                            os.rename(f"{archive_name}.zip", f"{archive_name}.tar")
                            print(f"Created archive '{archive_name}.tar' with files: {files}.")
                    else:
                        print("Error: Missing arguments for tar -cvf.")
                    
                elif parts[1] == '-xvf':  
                    _, archive_name = parts[1], parts[2]
                    os.rename(archive_name, f"{archive_name.replace('.tar.tar', '.zip')}")
                    tar_name = f"{archive_name.replace('.tar.tar', '.zip')}"
                    if os.path.exists(tar_name):
                        shutil.unpack_archive(tar_name, archive_name.replace('.tar.tar', ''))
                        print(f"Extracted archive '{archive_name}'.")
                        os.rename(f"{archive_name.replace('.tar.tar', '.zip')}", archive_name)
                    else:
                        print(f"Error: Archive '{archive_name}' not found.")
                else:
                    print("Error: Invalid tar operation.")
            else:
                print("Error: Invalid arguments for tar.")
        elif command == 'help' or command == 'h':
            show_help()
        if command.startswith('git '):
            execute_git_command(command)
        elif command == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command.startswith('vim'):
            subprocess.run(["start", "cmd", "/K", "vim"], shell=True)
            print("Vim started in new background terminal.")
        else:
            if command != 'ls':
                result = subprocess.run(command, shell=True, text=True, capture_output=True)
                print(result.stdout)
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Welcome to the simulated Linux terminal for Windows!")
    while True:
        cwd = os.getcwd()
        prompt = f"{cwd}$ "
        command = input(prompt).strip()

        if command.lower() == 'exit':
            print("Exiting terminal.")
            break
        else:
            execute_command(command)

if __name__ == "__main__":
    main()

