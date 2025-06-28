import os
import shutil
import argparse

def copy_and_rename_files(source_dir, dest_dir, ignore_dirs=None, ignore_exts=None):
    """
    Recursively copy files from source_dir to dest_dir, 
    renaming them with their path relative to source_dir.
    Skips folders listed in ignore_dirs and files with extensions in ignore_exts.
    """
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_exts is None:
        ignore_exts = []

    # Normalize extensions (ensure they start with a dot)
    ignore_exts = [ext if ext.startswith('.') else f'.{ext}' for ext in ignore_exts]

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Get the relative path from source directory
        rel_path = os.path.relpath(root, source_dir)

        for file in files:
            # Skip file if it has an ignored extension
            if os.path.splitext(file)[1].lower() in ignore_exts:
                continue

            src_file = os.path.join(root, file)

            # Create the new filename
            if rel_path == ".":
                new_name = f"{os.path.basename(source_dir)}_{file}"
            else:
                new_name = f"{os.path.basename(source_dir)}/{rel_path}_{file}"

            # Replace directory separators in the new filename
            new_name = new_name.replace(os.sep, "_")

            # Create the destination file path
            dest_file = os.path.join(dest_dir, new_name)

            # Copy the file with the new name
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} -> {dest_file}")

def main():
    parser = argparse.ArgumentParser(description='Recursively copy files with path-based renaming.')
    parser.add_argument('source', help='Source directory')
    parser.add_argument('destination', help='Destination directory')
    parser.add_argument('--ignore', nargs='*', default=[], help='Folder name(s) to ignore')
    parser.add_argument('--ignore-ext', nargs='*', default=[], help='File extension(s) to ignore (e.g., .png .ico)')

    args = parser.parse_args()

    # Call the copy function
    copy_and_rename_files(args.source, args.destination, args.ignore, args.ignore_ext)
    print("Copy operation completed successfully.")

if __name__ == "__main__":
    main()

