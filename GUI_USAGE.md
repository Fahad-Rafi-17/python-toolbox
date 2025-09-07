# Python Toolbox GUI - Usage Guide

## 🚀 Quick Start

### Option 1: Run the GUI directly
1. Double-click `run_gui.bat`
2. If you see errors, run `setup.bat` first

### Option 2: Create a standalone executable
1. Run `setup.bat` (if you haven't already)
2. Run `build_exe.bat`
3. Find your executable in the `dist/` folder
4. You can copy `Python-Toolbox-GUI.exe` anywhere and run it

## 📖 How to Use the GUI

### 1. Script Selection
- Choose from the dropdown menu:
  - **Tree Visualizer**: Creates a visual tree of your folder structure
  - **File Path Annotator**: Adds file path comments to code files
  - **File Flattener**: Copies files with path-based naming

### 2. Parameter Input
- **Required fields** are marked with `*`
- **Folder fields** have a "Browse" button for easy selection
- **Text fields** accept space-separated values where needed
- **Checkboxes** are optional settings

### 3. Running Scripts
- Click "Run Script" after filling in required parameters
- Output appears in the bottom panel in real-time
- The "Clear Output" button clears the output area

## 🔧 Script Details

### Tree Visualizer
**Purpose**: Creates a beautiful, colored tree view of any folder structure

**Parameters**:
- **Path**: The folder you want to visualize
- **Ignore Folders**: Folders to skip (e.g., "node_modules .git build")
- **Ignore Extensions**: File types to skip (e.g., ".log .tmp .cache")

**Example**: Visualize your project folder while ignoring common build/cache folders

### File Path Annotator
**Purpose**: Adds file path comments to the top of code files

**Parameters**:
- **Base Folder**: The root folder containing your code files
- **Make Copy**: Creates a backup before modifying files
- **Extensions**: File types to process (e.g., ".py .js .ts")
- **Ignore Folders**: Folders to skip during processing

**Example**: Add file path comments to all Python files in your project

### File Flattener
**Purpose**: Copies all files from a nested folder structure into one flat folder

**Parameters**:
- **Source Directory**: The folder to copy from
- **Destination Directory**: Where to put the flattened files
- **Ignore Folders**: Folders to skip
- **Ignore Extensions**: File types to skip

**Example**: Flatten a project folder to easily zip or share all code files

## 🛠️ Troubleshooting

### "No module named 'rich'" error
- Run `setup.bat` to install dependencies

### GUI doesn't start
- Make sure Python is installed
- Try running `python --version` in Command Prompt
- Run `setup.bat` to create a proper environment

### Script fails to run
- Check that all required parameters are filled
- Verify file/folder paths exist
- Check the output panel for specific error messages

### Building executable fails
- Make sure you have enough disk space
- Try running `setup.bat` first
- Check that antivirus isn't blocking PyInstaller

## 📁 File Structure

```
python-toolbox/
├── python_toolbox_gui.py    # Main GUI application
├── setup.bat               # Install dependencies
├── run_gui.bat             # Run GUI directly
├── build_exe.bat           # Create executable
├── requirements.txt        # Python dependencies
├── directory-tools/
│   └── tree_visualizer.py
├── code-annotation-tools/
│   └── file_path_annotator.py
└── file-management-tools/
    └── file_flattener.py
```

## 💡 Tips

1. **Always use "Make Copy"** when running File Path Annotator on important projects
2. **Test with small folders first** to understand how each script works
3. **Use specific ignore patterns** to avoid processing unnecessary files
4. **The executable is portable** - you can copy it to any Windows computer
5. **Check the output panel** for detailed progress and any error messages
