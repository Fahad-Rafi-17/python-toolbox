# Directory Tree Visualizer

A beautiful Python utility that creates colorful, interactive directory tree visualizations using the Rich library. Perfect for exploring project structures, documenting folder layouts, and understanding codebase organization.

## Features

- **Rich Visual Output**: Colorful, Unicode-based tree visualization
- **Smart Filtering**: Ignore folders and file extensions
- **Permission Handling**: Gracefully handles restricted directories
- **Color Coding**: Different colors for folders, files, and ignored items
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Requirements
```bash
pip install rich
```

### Download Script
```bash
# Clone or download the script
# Requires Rich library for beautiful output
```

## Usage

### Basic Usage
```bash
python tree_visualizer.py /path/to/directory
```

### Advanced Options
```bash
# Ignore common development folders
python tree_visualizer.py ~/my-project --ignore node_modules .git dist

# Ignore specific file types
python tree_visualizer.py ~/my-project --ignore-ext .log .tmp .cache

# Combine filters for clean output
python tree_visualizer.py ~/my-project --ignore node_modules .git build --ignore-ext .map .log .tmp
```

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `path` | Directory path to visualize (required) | - |
| `--ignore` | Folder names to ignore | `[]` |
| `--ignore-ext` | File extensions to ignore | `[]` |

## Visual Output

The tool creates a beautiful tree structure with color coding:

```
📁 my-awesome-project/
├── 📁 src/
│   ├── 📁 components/
│   │   ├── Button.tsx
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── 📁 utils/
│   │   └── helpers.ts
│   └── App.tsx
├── 📁 public/
│   └── index.html
├── 📁 node_modules/ (ignored folder)
├── package.json
└── README.md
```

## Color Scheme

- **🔵 Blue Folders**: Regular directories
- **🟢 Green Root**: Root directory name
- **🟡 Yellow Ignored**: Ignored folders (with label)
- **⚪ White Files**: Regular files
- **🔴 Red Errors**: Permission denied indicators

## Examples

### Basic Project Visualization
```bash
python tree_visualizer.py ./my-react-app
```

### Clean Node.js Project View
```bash
python tree_visualizer.py ./my-app --ignore node_modules .git dist build .next
```

### Python Project (Hide Bytecode)
```bash
python tree_visualizer.py ./my-python-app --ignore __pycache__ .git venv --ignore-ext .pyc .pyo
```

### Documentation-Focused View
```bash
python tree_visualizer.py ./project --ignore-ext .log .tmp .cache .lock
```

## Common Ignore Patterns

### JavaScript/Node.js Projects
```bash
--ignore node_modules .git dist build .next .nuxt coverage --ignore-ext .map .log
```

### Python Projects
```bash
--ignore __pycache__ .git venv env .pytest_cache dist --ignore-ext .pyc .pyo
```

### General Development
```bash
--ignore .git .vscode .idea .DS_Store tmp temp --ignore-ext .log .tmp .cache
```

### Documentation Projects
```bash
--ignore .git node_modules --ignore-ext .log .tmp .backup
```

## Use Cases

### Development
- **Project Overview**: Quickly understand codebase structure
- **Code Reviews**: Visualize changes in directory structure
- **Documentation**: Include tree diagrams in README files
- **Onboarding**: Help new team members understand project layout

### System Administration
- **Directory Auditing**: Visualize system directory structures
- **Backup Planning**: Understand folder hierarchies before backup
- **Disk Usage**: Identify directory structures for cleanup
- **File Organization**: Plan directory restructuring

### Education & Training
- **Teaching**: Show file system concepts visually
- **Tutorials**: Document project structures in courses
- **Presentations**: Include directory diagrams in slides
- **Learning**: Explore unfamiliar codebases

## Advanced Features

### Permission Handling
The tool gracefully handles directories with restricted permissions:
```
📁 protected-folder/
└── [Permission Denied]
```

### Large Directory Handling
- Efficiently processes large directory trees
- Sorts entries alphabetically for consistent output
- Handles deeply nested structures

### Cross-Platform Compatibility
- Works on Windows, macOS, and Linux
- Handles different path separators automatically
- Unicode tree characters display correctly

## Integration Examples

### In Documentation
```markdown
## Project Structure
\`\`\`
my-project/
├── src/
│   ├── components/
│   └── utils/
└── docs/
\`\`\`
```

### With Other Tools
```bash
# Save output to file
python tree_visualizer.py ./project > project-structure.txt

# Combine with grep for specific files
python tree_visualizer.py ./project | grep -i "component"
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Generate Project Structure
  run: |
    pip install rich
    python tree_visualizer.py . --ignore .git node_modules > STRUCTURE.md
```

## Performance Tips

- Use `--ignore` for large dependency folders like `node_modules`
- Filter out generated files with `--ignore-ext`
- Process smaller subdirectories for faster results
- Use specific paths rather than root directories

## Troubleshooting

**Issue**: Missing colors or Unicode characters
**Solution**: Ensure your terminal supports Unicode and colors

**Issue**: Permission errors
**Solution**: Tool handles these gracefully - no action needed

**Issue**: Output too verbose
**Solution**: Use ignore patterns to filter unwanted files/folders

**Issue**: Rich library not found
**Solution**: Install with `pip install rich`

## Customization

The script can be easily modified to:
- Add new color schemes
- Change tree symbols
- Add file size information
- Include modification dates
- Filter by file patterns

## License

Open source - feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Add features like file sizes, dates, or custom themes
3. Improve filtering options or add export formats
4. Submit a pull request
