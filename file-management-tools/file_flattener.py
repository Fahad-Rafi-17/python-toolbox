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

    # Normalize paths
    source_dir = os.path.abspath(source_dir)
    dest_dir = os.path.abspath(dest_dir)

    # Normalize extensions (ensure they start with a dot)
    ignore_exts = [ext if ext.startswith('.') else f'.{ext}' for ext in ignore_exts]

    # Create destination directory if it doesn't exist
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            print(f"Created destination directory: {dest_dir}")
    except Exception as e:
        print(f"Error creating destination directory: {e}")
        return

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

            # Replace directory separators and invalid characters in the new filename
            new_name = new_name.replace(os.sep, "_").replace("/", "_")
            # Remove or replace problematic characters for Windows
            invalid_chars = '<>:"|?*'
            for char in invalid_chars:
                new_name = new_name.replace(char, "_")

            # Create the destination file path
            dest_file = os.path.join(dest_dir, new_name)

            # Ensure the filename isn't too long (Windows limit is ~260 chars)
            if len(dest_file) > 250:
                name, ext = os.path.splitext(new_name)
                # Truncate the name but keep the extension
                max_name_len = 250 - len(dest_dir) - len(ext) - 10  # buffer
                if max_name_len > 0:
                    new_name = name[:max_name_len] + ext
                    dest_file = os.path.join(dest_dir, new_name)

            # Copy the file with the new name
            try:
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {src_file} -> {dest_file}")
            except Exception as e:
                print(f"Error copying {src_file}: {e}")
                continue

def main():
    parser = argparse.ArgumentParser(description='Recursively copy files with path-based renaming.')
    parser.add_argument('source', help='Source directory')
    parser.add_argument('destination', help='Destination directory')
    parser.add_argument('--ignore', nargs='*', default=[], help='Folder name(s) to ignore')
    parser.add_argument('--ignore-ext', nargs='*', default=[], help='File extension(s) to ignore (e.g., .png .ico)')

    args = parser.parse_args()

    # Validate source directory
    if not os.path.exists(args.source):
        print(f"Error: Source directory '{args.source}' does not exist.")
        return
    
    if not os.path.isdir(args.source):
        print(f"Error: Source path '{args.source}' is not a directory.")
        return

    print(f"Source: {os.path.abspath(args.source)}")
    print(f"Destination: {os.path.abspath(args.destination)}")
    print(f"Ignoring folders: {args.ignore}")
    print(f"Ignoring extensions: {args.ignore_ext}")
    print("-" * 50)

    # Call the copy function
    copy_and_rename_files(args.source, args.destination, args.ignore, args.ignore_ext)
    print("-" * 50)
    print("Copy operation completed successfully.")

if __name__ == "__main__":
    main()

