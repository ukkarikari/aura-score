import os
import sys

# OUTPUT_FILE = "dump.txt"
SELF_FILE = "./dump.py"
ROOT_DIR = "."  # change if needed

EXCLUDE_DIRS = {".git", "__pycache__", "venv", ".venv", "copy"}
INCLUDE_EXTENSIONS = {".py"}  # add more if you want


def should_include_file(filename):
    return any(filename.endswith(ext) for ext in INCLUDE_EXTENSIONS)


def should_exclude_dir(dirname):
    return dirname in EXCLUDE_DIRS


def collect_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # modify dirnames in-place to skip excluded dirs
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            if full_path == SELF_FILE:
                continue

            if should_include_file(filename):
                yield full_path


def write_output(files, root_dir):
    for filepath in files:
        rel_path = os.path.relpath(filepath, root_dir)

        sys.stdout.write(f"# ./{rel_path}\n")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                sys.stdout.write(f.read())
        except Exception as e:
            sys.stdout.write(f"# Error reading file: {e}")

        sys.stdout.write("\n\n")


if __name__ == "__main__":
    files = list(collect_files(ROOT_DIR))
    write_output(files, ROOT_DIR)
