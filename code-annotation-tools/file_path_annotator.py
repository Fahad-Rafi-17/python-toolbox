import os
import shutil
import argparse

# Extensions to process by default
DEFAULT_EXTENSIONS = ['.ts', '.tsx']

# Folders to ignore during traversal
IGNORED_FOLDERS = {'node_modules', 'public', '.git', '.husky', '.next'}

# File comment styles per extension
COMMENT_STYLES = {
    '.ts': '// File: {}',
    '.tsx': '// File: {}',
    '.py': '# File: {}',
    '.js': '// File: {}',
    '.html': '<!-- File: {} -->',
    '.css': '/* File: {} */',
    '.json': '// File: {}',
    '.md': '<!-- File: {} -->',
}

def is_supported_file(filename, allowed_extensions):
    return os.path.splitext(filename)[1] in allowed_extensions

def add_comment_to_file(file_path, relative_path):
    ext = os.path.splitext(file_path)[1]
    comment_template = COMMENT_STYLES.get(ext)
    if not comment_template:
        print(f"Skipping unsupported extension: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        comment = comment_template.format(relative_path)

        if content.strip().startswith(comment.split()[0]):
            print(f"Already commented: {file_path}")
            return

        new_content = comment + '\n' + content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Annotated: {file_path}")
    except Exception as e:
        print(f"Failed to annotate {file_path}: {e}")

def process_directory(base_dir, allowed_extensions, ignored_folders):
    for root, dirs, files in os.walk(base_dir):
        # Modify dirs in-place to exclude ignored folders
        dirs[:] = [d for d in dirs if d not in ignored_folders]

        for file in files:
            if is_supported_file(file, allowed_extensions):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                add_comment_to_file(full_path, rel_path)

def main():
    parser = argparse.ArgumentParser(description="Annotate files with their relative paths.")
    parser.add_argument("base_folder", help="Base folder to process.")
    parser.add_argument("--makeCopy", action="store_true", help="Make a copy of the folder first.")
    parser.add_argument("--extensions", nargs='*', default=DEFAULT_EXTENSIONS,
                        help="List of file extensions to include, e.g. .ts .tsx .js")
    parser.add_argument("--ignore", nargs='*', default=list(IGNORED_FOLDERS),
                        help="List of folders to ignore.")

    args = parser.parse_args()
    base_folder = os.path.abspath(args.base_folder)

    if args.makeCopy:
        copy_folder = base_folder + "_copy"
        if os.path.exists(copy_folder):
            shutil.rmtree(copy_folder)
        shutil.copytree(base_folder, copy_folder)
        print(f"Copied {base_folder} to {copy_folder}")
        base_folder = copy_folder

    process_directory(base_folder, args.extensions, set(args.ignore))

if __name__ == "__main__":
    main()

