import os
import argparse
from rich.console import Console
from rich.tree import Tree

def build_tree(dir_path, tree, ignore_folders, ignore_exts):
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        tree.add("[red][Permission Denied][/]")
        return

    for entry in entries:
        full_path = os.path.join(dir_path, entry)

        if os.path.isdir(full_path):
            if entry in ignore_folders:
                tree.add(f"[bold yellow]{entry}/[/] [dim](ignored folder)[/]")
                continue
            branch = tree.add(f"[bold blue]{entry}/[/]")
            build_tree(full_path, branch, ignore_folders, ignore_exts)
        else:
            if any(entry.endswith(ext) for ext in ignore_exts):
                continue
            tree.add(entry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📁 Pretty print a folder structure using Rich with ignore options."
    )
    parser.add_argument("path", help="Base folder path to visualize")
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="Folder names to ignore (e.g. node_modules .git build)"
    )
    parser.add_argument(
        "--ignore-ext",
        nargs="*",
        default=[],
        help="File extensions to ignore (e.g. .log .png .ico)"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print("[!] Error: Provided path is not a directory")
    else:
        console = Console()
        tree = Tree(f"[bold green]{args.path}[/]")
        build_tree(args.path, tree, args.ignore, args.ignore_ext)
        console.print(tree)
