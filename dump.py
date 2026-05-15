import os
import sys

SELF_FILE = os.path.abspath(__file__)
ROOT_DIR = "."

EXCLUDE_DIRS = {".git", "__pycache__", "venv", ".venv", "copy"}
INCLUDE_EXTENSIONS = {".py"}


def should_include_file(filename):
    return any(filename.endswith(ext) for ext in INCLUDE_EXTENSIONS)


def should_exclude_dir(dirname):
    return dirname in EXCLUDE_DIRS


def collect_project_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]

        for filename in filenames:
            full_path = os.path.abspath(os.path.join(dirpath, filename))

            if full_path == SELF_FILE:
                continue

            if should_include_file(filename):
                yield full_path


def normalize_input_files(paths):
    files = []

    for path in paths:
        abs_path = os.path.abspath(path)

        if not os.path.exists(abs_path):
            print(f"Warning: file does not exist: {path}", file=sys.stderr)
            continue

        if os.path.isdir(abs_path):
            print(f"Warning: skipping directory: {path}", file=sys.stderr)
            continue

        if abs_path == SELF_FILE:
            continue

        files.append(abs_path)

    return files


def write_output(files, root_dir):
    for filepath in files:
        rel_path = os.path.relpath(filepath, root_dir)

        sys.stdout.write(f"### ./{rel_path}\n")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                sys.stdout.write(f"```\n")  # noqa: F541
                sys.stdout.write(f.read())
                sys.stdout.write(f"\n```\n")  # noqa: F541
        except Exception as e:
            sys.stdout.write(f"# Error reading file: {e}")

        sys.stdout.write("\n\n")


if __name__ == "__main__":
    # If files are passed as arguments:
    # python dump.py ./services/auth.py ./main.py
    if len(sys.argv) > 1:
        files = normalize_input_files(sys.argv[1:])
    else:
        files = list(collect_project_files(ROOT_DIR))

    write_output(files, ROOT_DIR)
