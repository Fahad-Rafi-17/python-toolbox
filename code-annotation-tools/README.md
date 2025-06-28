# File Path Annotator

A Python utility that automatically adds file path comments to the top of source code files, making it easier to identify files when reviewing code or working with large codebases.

## Features

- **Multi-language support**: Supports TypeScript, JavaScript, Python, HTML, CSS, JSON, and Markdown files
- **Smart commenting**: Uses appropriate comment syntax for each file type
- **Selective processing**: Process only specific file extensions
- **Folder filtering**: Ignore common build/dependency folders like `node_modules`, `.git`, etc.
- **Safe backup**: Optional folder copying before annotation
- **Duplicate protection**: Skips files that are already annotated

## Installation

No additional dependencies required - uses only Python standard library.

```bash
# Clone or download the script
# No pip install needed
```

## Usage

### Basic Usage

```bash
python file_path_annotator.py /path/to/your/project
```

### Advanced Options

```bash
# Make a backup copy before annotating
python file_path_annotator.py /path/to/project --makeCopy

# Specify custom file extensions
python file_path_annotator.py /path/to/project --extensions .js .jsx .ts .tsx .py

# Ignore additional folders
python file_path_annotator.py /path/to/project --ignore node_modules dist build .git

# Combine options
python file_path_annotator.py /path/to/project --makeCopy --extensions .ts .js --ignore build temp
```

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `base_folder` | Base folder to process (required) | - |
| `--makeCopy` | Create a backup copy before processing | False |
| `--extensions` | File extensions to include | `.ts .tsx` |
| `--ignore` | Folders to ignore during traversal | `node_modules public .git .husky .next` |

## Supported File Types

| Extension | Comment Style | Example |
|-----------|---------------|---------|
| `.ts`, `.tsx`, `.js` | `//` | `// File: src/components/Button.tsx` |
| `.py` | `#` | `# File: utils/helpers.py` |
| `.html`, `.md` | `<!-- -->` | `<!-- File: pages/index.html -->` |
| `.css` | `/* */` | `/* File: styles/main.css */` |
| `.json` | `//` | `// File: config/package.json` |

## Examples

### Before Processing
```typescript
import React from 'react';

export const Button = () => {
  return <button>Click me</button>;
};
```

### After Processing
```typescript
// File: src/components/Button.tsx
import React from 'react';

export const Button = () => {
  return <button>Click me</button>;
};
```

## Default Ignored Folders

- `node_modules` - Node.js dependencies
- `public` - Static assets
- `.git` - Git repository data
- `.husky` - Git hooks
- `.next` - Next.js build output

## Use Cases

- **Code reviews**: Quickly identify which file you're looking at
- **Documentation**: Generate file listings with clear paths
- **Debugging**: Easier stack trace correlation
- **Large projects**: Navigate codebases more efficiently
- **AI assistance**: Help AI tools understand file context

## Safety Features

- **Backup option**: Use `--makeCopy` to create a safe backup
- **Duplicate detection**: Won't re-annotate already processed files
- **Error handling**: Gracefully handles permission errors and encoding issues
- **Dry-run logging**: Shows which files are processed or skipped

## License

Open source - feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add support for new file types or improve existing functionality
4. Submit a pull request

## Troubleshooting

**Issue**: Permission denied errors
**Solution**: Run with appropriate permissions or exclude protected directories

**Issue**: Encoding errors
**Solution**: Ensure files are UTF-8 encoded or add encoding detection

**Issue**: Unwanted annotations
**Solution**: Use `--extensions` to limit file types or add to ignore list
