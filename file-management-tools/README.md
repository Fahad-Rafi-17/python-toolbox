\# File Flattener

A Python utility that recursively copies files from a nested directory structure into a flat destination directory, renaming files to preserve their original path information in the filename.

## Features

- **Recursive copying**: Processes all subdirectories automatically
- **Path preservation**: Original directory structure encoded in filenames
- **Selective filtering**: Ignore specific folders and file extensions
- **Collision handling**: Unique naming prevents file overwrites
- **Metadata preservation**: Maintains original file timestamps and permissions

## Installation

No additional dependencies required - uses only Python standard library.

```bash
# Clone or download the script
# No pip install needed
```

## Usage

### Basic Usage

```bash
python file_flattener.py /path/to/source /path/to/destination
```

### Advanced Options

```bash
# Ignore specific folders
python file_flattener.py /source /dest --ignore node_modules .git build

# Ignore file extensions
python file_flattener.py /source /dest --ignore-ext .png .jpg .ico .log

# Combine options
python file_flattener.py /source /dest --ignore dist temp --ignore-ext .map .lock
```

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `source` | Source directory to copy from (required) | - |
| `destination` | Destination directory to copy to (required) | - |
| `--ignore` | Folder names to ignore | `[]` |
| `--ignore-ext` | File extensions to ignore | `[]` |

## How It Works

The tool transforms nested file paths into flat filenames by replacing directory separators with underscores:

### Original Structure
```
my-project/
├── src/
│   ├── components/
│   │   └── Button.tsx
│   └── utils/
│       └── helpers.js
└── docs/
    └── readme.md
```

### Flattened Result
```
flattened/
├── my-project_src_components_Button.tsx
├── my-project_src_utils_helpers.js
└── my-project_docs_readme.md
```

## Examples

### Basic File Flattening
```bash
python file_flattener.py ./web-app ./flattened-app
```

**Input**: `web-app/src/pages/auth/login.tsx`
**Output**: `flattened-app/web-app_src_pages_auth_login.tsx`

### Ignoring Build Artifacts
```bash
python file_flattener.py ./project ./flat --ignore node_modules dist .git --ignore-ext .map .log
```

This will:
- Skip `node_modules/`, `dist/`, and `.git/` folders entirely
- Ignore all `.map` and `.log` files
- Copy and rename all other files

### Processing Multiple Projects
```bash
# Flatten multiple projects into one directory
python file_flattener.py ./project-a ./combined
python file_flattener.py ./project-b ./combined
python file_flattener.py ./project-c ./combined
```

## Use Cases

### Code Analysis
- **AI Training**: Prepare codebases for machine learning models
- **Static Analysis**: Feed files to analysis tools that expect flat structures
- **Documentation**: Generate comprehensive file listings

### Migration & Backup
- **Legacy Systems**: Extract files from complex nested structures
- **Archive Creation**: Create flat backups of project files
- **Data Migration**: Prepare files for systems with flat file requirements

### Development Workflows
- **Code Review**: Easier batch processing of files
- **Build Tools**: Prepare assets for tools expecting flat inputs
- **Testing**: Create simplified test fixtures

## File Naming Convention

Files are renamed using this pattern:
```
{source_folder_name}_{relative_path_with_underscores}_{original_filename}
```

**Examples**:
- `src/components/ui/Button.tsx` → `project_src_components_ui_Button.tsx`
- `docs/api/users.md` → `project_docs_api_users.md`
- `config.json` → `project_config.json`

## Common Ignore Patterns

### Node.js Projects
```bash
--ignore node_modules .git dist build .next --ignore-ext .log .map
```

### Python Projects
```bash
--ignore __pycache__ .git dist build venv --ignore-ext .pyc .pyo
```

### General Development
```bash
--ignore .git .vscode .idea node_modules --ignore-ext .DS_Store .log
```

## Safety Features

- **Non-destructive**: Never modifies source files
- **Automatic directory creation**: Creates destination directory if needed
- **Error handling**: Graceful handling of permission issues
- **Progress logging**: Shows each file being processed
- **Metadata preservation**: Maintains file timestamps and permissions

## Performance Considerations

- **Large repositories**: Use ignore patterns to skip unnecessary files
- **Network drives**: Local destinations perform better than network locations
- **Memory usage**: Processes files individually - suitable for large directories

## Troubleshooting

**Issue**: Permission denied errors
**Solution**: Ensure read access to source and write access to destination

**Issue**: Filename too long errors
**Solution**: Use shorter source paths or limit directory depth

**Issue**: Duplicate filenames
**Solution**: Tool handles this automatically with path-based naming

## License

Open source - feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Add features like progress bars, compression, or advanced filtering
3. Improve error handling or add resume functionality
4. Submit a pull request
