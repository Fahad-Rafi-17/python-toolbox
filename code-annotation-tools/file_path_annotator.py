
# example: python3 /home/fadi/Documents/python-toolbox/code-annotation-tools/file_path_annotator.py '/home/fadi/Documents/portfolio-website' --ignore node_modules public .git .husky .next
import os
import shutil
import argparse
import re

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

# Regex patterns to match existing file comments
COMMENT_PATTERNS = {
    '.ts': r'^// File: (.+)$',
    '.tsx': r'^// File: (.+)$',
    '.py': r'^# File: (.+)$',
    '.js': r'^// File: (.+)$',
    '.html': r'^<!-- File: (.+) -->$',
    '.css': r'^/\* File: (.+) \*/$',
    '.json': r'^// File: (.+)$',
    '.md': r'^<!-- File: (.+) -->$',
}

def is_supported_file(filename, allowed_extensions):
    return os.path.splitext(filename)[1] in allowed_extensions

def find_existing_comment(lines, ext):
    """Find existing file comment in the first 5 lines and return its line number and path."""
    pattern = COMMENT_PATTERNS.get(ext)
    if not pattern:
        return None, None
    
    for i, line in enumerate(lines[:5]):  # Check only first 5 lines
        match = re.match(pattern, line.strip())
        if match:
            return i, match.group(1)  # Return line number and extracted path
    return None, None

def add_or_update_comment(file_path, relative_path):
    ext = os.path.splitext(file_path)[1]
    comment_template = COMMENT_STYLES.get(ext)
    if not comment_template:
        print(f"Skipping unsupported extension: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            # Empty file, just add the comment
            new_content = comment_template.format(relative_path) + '\n'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Annotated empty file: {file_path}")
            return

        comment_line_num, existing_path = find_existing_comment(lines, ext)
        new_comment = comment_template.format(relative_path)

        if comment_line_num is not None:
            # Found existing comment
            if existing_path == relative_path:
                print(f"Already up-to-date: {file_path}")
                return
            else:
                # Update existing comment
                lines[comment_line_num] = new_comment + '\n'
                print(f"Updated path comment: {file_path} (was: {existing_path}, now: {relative_path})")
        else:
            # No existing comment found, add new one at the beginning
            lines.insert(0, new_comment + '\n')
            print(f"Added new comment: {file_path}")

        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def process_directory(base_dir, allowed_extensions, ignored_folders):
    for root, dirs, files in os.walk(base_dir):
        # Modify dirs in-place to exclude ignored folders
        dirs[:] = [d for d in dirs if d not in ignored_folders]

        for file in files:
            if is_supported_file(file, allowed_extensions):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                add_or_update_comment(full_path, rel_path)

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
