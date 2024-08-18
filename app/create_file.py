import os
import sys
from datetime import datetime


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def prompt_content() -> list:
    lines = []
    line_number = 1
    while True:
        content = input("Enter content line: ")
        if content.lower() == "stop":
            break
        lines.append(f"{line_number} {content}")
        line_number += 1
    return lines


def create_file_with_content(filepath: str) -> None:
    file_exists = os.path.exists(filepath)

    with open(filepath, "a" if file_exists else "w") as f:
        timestamp = get_timestamp()
        f.write(f"{timestamp}\n")
        content_lines = prompt_content()
        f.write("\n".join(content_lines) + "\n\n")

    print(f"File created/updated at: {filepath}")


def display_usage() -> None:
    usage_message = """
    Usage:
    1. To create a directory:
       python create_file.py -d dir1 dir2
       This creates a directory structure 'dir1/dir2'
       inside the current directory.

    2. To create a file with content:
       python create_file.py -f file.txt
       This creates or appends content to 'file.txt' in the current directory.

    3. To create a directory and file with content:
       python create_file.py -d dir1 dir2 -f file.txt
       This creates a directory 'dir1/dir2' and then creates
       or appends content to 'file.txt' inside that directory.
    """
    print(usage_message)


def main() -> None:
    args = sys.argv[1:]

    if not args or ("-d" not in args and "-f" not in args):
        print("Error: Missing or invalid command.")
        display_usage()
        sys.exit(1)

    try:
        if "-d" in args:
            dir_index = args.index("-d") + 1
            directories = []
            while dir_index < len(args) and args[dir_index] != "-f":
                directories.append(args[dir_index])
                dir_index += 1
            path = os.path.join(*directories)
            os.makedirs(path, exist_ok=True)
            print(f"Directory created: {path}")

        if "-f" in args:
            file_index = args.index("-f") + 1
            if file_index < len(args):
                filename = args[file_index]
                if "-d" in args:
                    filepath = os.path.join(path, filename)
                else:
                    filepath = filename
                create_file_with_content(filepath)
            else:
                print("Error: Missing file name after '-f' flag.")
                display_usage()
                sys.exit(1)
    except TypeError:
        display_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
