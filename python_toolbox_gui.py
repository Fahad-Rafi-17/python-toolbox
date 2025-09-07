#!/usr/bin/env python3
"""
Python Toolbox GUI
A simple GUI interface to run various Python scripts in the toolbox.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import sys
import threading
from pathlib import Path

class PythonToolboxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Toolbox - Script Runner")
        self.root.geometry("800x600")
        
        # Get the directory where this script is located
        self.base_dir = Path(__file__).parent.absolute()
        
        # Script configurations
        self.scripts = {
            "Tree Visualizer": {
                "path": self.base_dir / "directory-tools" / "tree_visualizer.py",
                "description": "Pretty-print folder structure using Rich",
                "inputs": [
                    {"name": "Path", "type": "folder", "required": True, "help": "Folder path to visualize"},
                    {"name": "Ignore Folders", "type": "text", "required": False, "help": "Space-separated folder names to ignore (e.g., node_modules .git)"},
                    {"name": "Ignore Extensions", "type": "text", "required": False, "help": "Space-separated file extensions to ignore (e.g., .log .png)"}
                ]
            },
            "File Path Annotator": {
                "path": self.base_dir / "code-annotation-tools" / "file_path_annotator.py",
                "description": "Add file path comments to code files",
                "inputs": [
                    {"name": "Base Folder", "type": "folder", "required": True, "help": "Base folder to process"},
                    {"name": "Make Copy", "type": "checkbox", "required": False, "help": "Make a copy of the folder first"},
                    {"name": "Extensions", "type": "text", "required": False, "help": "File extensions to include (e.g., .ts .tsx .py)"},
                    {"name": "Ignore Folders", "type": "text", "required": False, "help": "Folder names to ignore (e.g., node_modules .git)"}
                ]
            },
            "File Flattener": {
                "path": self.base_dir / "file-management-tools" / "file_flattener.py",
                "description": "Recursively copy files with path-based renaming",
                "inputs": [
                    {"name": "Source Directory", "type": "folder", "required": True, "help": "Source directory to copy from"},
                    {"name": "Destination Directory", "type": "folder", "required": True, "help": "Destination directory"},
                    {"name": "Common Ignore Folders", "type": "checkbox_group", "required": False, 
                     "help": "Select common folders to ignore", 
                     "options": ["node_modules", ".git", ".vscode", "__pycache__", "dist", "build", ".next", ".nuxt", "target", "bin", "obj"]},
                    {"name": "Custom Ignore Folders", "type": "text", "required": False, "help": "Additional folder names to ignore (space-separated)"},
                    {"name": "Common Ignore Extensions", "type": "checkbox_group", "required": False,
                     "help": "Select common file types to ignore",
                     "options": [".log", ".tmp", ".cache", ".lock", ".DS_Store", ".thumbs.db", ".exe", ".dll", ".so", ".o", ".pyc"]},
                    {"name": "Custom Ignore Extensions", "type": "text", "required": False, "help": "Additional file extensions to ignore (space-separated, e.g., .png .ico)"}
                ]
            }
        }
        
        # Track running process
        self.running_process = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Python Toolbox", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Script selection
        ttk.Label(main_frame, text="Select Script:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.script_var = tk.StringVar()
        self.script_combo = ttk.Combobox(main_frame, textvariable=self.script_var, values=list(self.scripts.keys()), state="readonly", width=50)
        self.script_combo.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.script_combo.bind('<<ComboboxSelected>>', self.on_script_selected)
        
        # Description
        self.description_label = ttk.Label(main_frame, text="", foreground="gray", wraplength=600)
        self.description_label.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Input frame
        self.input_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        self.input_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.input_frame.columnconfigure(1, weight=1)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        self.run_button = ttk.Button(button_frame, text="Run Script", command=self.run_script, state="disabled")
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Stop Script", command=self.stop_script, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.pack(side=tk.LEFT)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, state="disabled")
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main grid weights
        main_frame.rowconfigure(4, weight=1)
        main_frame.rowconfigure(6, weight=2)
        
    def on_script_selected(self, event=None):
        script_name = self.script_var.get()
        if script_name not in self.scripts:
            return
            
        script_config = self.scripts[script_name]
        
        # Update description
        self.description_label.config(text=script_config["description"])
        
        # Clear previous inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        # Create input fields
        self.input_widgets = {}
        row = 0
        
        for input_config in script_config["inputs"]:
            name = input_config["name"]
            input_type = input_config["type"]
            required = input_config["required"]
            help_text = input_config["help"]
            
            # Label
            label_text = f"{name}{'*' if required else ''}:"
            label = ttk.Label(self.input_frame, text=label_text)
            label.grid(row=row, column=0, sticky=tk.W, pady=2, padx=(0, 10))
            
            # Input widget
            if input_type == "folder":
                frame = ttk.Frame(self.input_frame)
                frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
                frame.columnconfigure(0, weight=1)
                
                entry = ttk.Entry(frame)
                entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
                
                browse_btn = ttk.Button(frame, text="Browse", 
                                      command=lambda e=entry: self.browse_folder(e))
                browse_btn.grid(row=0, column=1)
                
                self.input_widgets[name] = entry
                
            elif input_type == "checkbox":
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(self.input_frame, variable=var)
                checkbox.grid(row=row, column=1, sticky=tk.W, pady=2)
                self.input_widgets[name] = var
                
            elif input_type == "checkbox_group":
                # Create a frame for multiple checkboxes
                checkbox_frame = ttk.Frame(self.input_frame)
                checkbox_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
                
                options = input_config.get("options", [])
                checkbox_vars = {}
                
                # Create checkboxes in a grid layout
                cols = 3  # Number of columns
                for i, option in enumerate(options):
                    var = tk.BooleanVar()
                    checkbox = ttk.Checkbutton(checkbox_frame, text=option, variable=var)
                    checkbox.grid(row=i // cols, column=i % cols, sticky=tk.W, padx=(0, 10), pady=1)
                    checkbox_vars[option] = var
                
                self.input_widgets[name] = checkbox_vars
                
            else:  # text
                entry = ttk.Entry(self.input_frame)
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
                self.input_widgets[name] = entry
            
            # Help text
            if help_text:
                help_label = ttk.Label(self.input_frame, text=help_text, foreground="gray", font=("Arial", 8))
                help_label.grid(row=row+1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
                row += 2
            else:
                row += 1
        
        self.run_button.config(state="normal")
    
    def browse_folder(self, entry_widget):
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder)
    
    def validate_inputs(self):
        script_name = self.script_var.get()
        if not script_name:
            messagebox.showerror("Error", "Please select a script first.")
            return False
        
        script_config = self.scripts[script_name]
        
        for input_config in script_config["inputs"]:
            name = input_config["name"]
            required = input_config["required"]
            input_type = input_config["type"]
            
            if required:
                widget = self.input_widgets[name]
                if isinstance(widget, tk.BooleanVar):
                    continue  # Checkboxes are always valid
                elif isinstance(widget, dict):
                    continue  # Checkbox groups are always valid (optional selections)
                elif hasattr(widget, 'get'):
                    value = widget.get().strip()
                    if not value:
                        messagebox.showerror("Error", f"Please provide a value for '{name}'.")
                        return False
                    
                    # Additional validation for folder/file paths
                    if input_type == "folder":
                        if not os.path.exists(value):
                            result = messagebox.askyesno("Path Not Found", 
                                f"The path '{value}' does not exist.\n\n" +
                                "For destination folders, this is normal and will be created.\n" +
                                "For source folders, this may cause an error.\n\n" +
                                "Do you want to continue anyway?")
                            if not result:
                                return False
        
        return True
    
    def build_command(self):
        script_name = self.script_var.get()
        script_config = self.scripts[script_name]
        script_path = script_config["path"]
        
        cmd = [sys.executable, str(script_path)]
        
        # Add arguments based on script type
        if script_name == "Tree Visualizer":
            path = self.input_widgets["Path"].get().strip()
            cmd.append(path)
            
            ignore_folders = self.input_widgets["Ignore Folders"].get().strip()
            if ignore_folders:
                cmd.extend(["--ignore"] + ignore_folders.split())
            
            ignore_exts = self.input_widgets["Ignore Extensions"].get().strip()
            if ignore_exts:
                cmd.extend(["--ignore-ext"] + ignore_exts.split())
        
        elif script_name == "File Path Annotator":
            base_folder = self.input_widgets["Base Folder"].get().strip()
            cmd.append(base_folder)
            
            if self.input_widgets["Make Copy"].get():
                cmd.append("--makeCopy")
            
            extensions = self.input_widgets["Extensions"].get().strip()
            if extensions:
                cmd.extend(["--extensions"] + extensions.split())
            
            ignore_folders = self.input_widgets["Ignore Folders"].get().strip()
            if ignore_folders:
                cmd.extend(["--ignore"] + ignore_folders.split())
        
        elif script_name == "File Flattener":
            source = self.input_widgets["Source Directory"].get().strip()
            dest = self.input_widgets["Destination Directory"].get().strip()
            cmd.extend([source, dest])
            
            # Collect ignore folders from checkboxes and custom input
            ignore_folders = []
            
            # Common ignore folders (checkboxes)
            common_ignore = self.input_widgets["Common Ignore Folders"]
            for folder, var in common_ignore.items():
                if var.get():
                    ignore_folders.append(folder)
            
            # Custom ignore folders (text input)
            custom_ignore = self.input_widgets["Custom Ignore Folders"].get().strip()
            if custom_ignore:
                ignore_folders.extend(custom_ignore.split())
            
            if ignore_folders:
                cmd.extend(["--ignore"] + ignore_folders)
            
            # Collect ignore extensions from checkboxes and custom input
            ignore_exts = []
            
            # Common ignore extensions (checkboxes)
            common_exts = self.input_widgets["Common Ignore Extensions"]
            for ext, var in common_exts.items():
                if var.get():
                    ignore_exts.append(ext)
            
            # Custom ignore extensions (text input)
            custom_exts = self.input_widgets["Custom Ignore Extensions"].get().strip()
            if custom_exts:
                ignore_exts.extend(custom_exts.split())
            
            if ignore_exts:
                cmd.extend(["--ignore-ext"] + ignore_exts)
        
        return cmd
    
    def stop_script(self):
        if self.running_process:
            try:
                self.running_process.terminate()
                self.append_output("\n🛑 Script stopped by user.\n")
                self.running_process = None
            except Exception as e:
                self.append_output(f"\n⚠️ Error stopping script: {str(e)}\n")
        
        # Re-enable run button and disable stop button
        self.run_button.config(state="normal")
        self.stop_button.config(state="disabled")
    
    def append_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")
        self.root.update_idletasks()
    
    def clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
    
    def run_script_thread(self, cmd):
        try:
            self.append_output(f"Running command: {' '.join(cmd)}\n")
            self.append_output("-" * 50 + "\n")
            
            self.running_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in self.running_process.stdout:
                if self.running_process.poll() is not None:
                    break  # Process was terminated
                self.append_output(line)
            
            return_code = self.running_process.wait()
            
            if return_code == 0:
                self.append_output("\n" + "=" * 50 + "\n")
                self.append_output("✅ Script completed successfully!\n")
            elif return_code == -15 or return_code == 1:  # SIGTERM or generic error
                if self.running_process is None:  # User stopped it
                    return  # Already handled in stop_script
                self.append_output("\n" + "=" * 50 + "\n")
                self.append_output(f"❌ Script completed with errors (return code: {return_code})\n")
                self.append_output("\nTips for common issues:\n")
                self.append_output("• Check that all file/folder paths exist\n")
                self.append_output("• Ensure you have write permissions to the destination\n")
                self.append_output("• Try using shorter paths or avoid special characters\n")
                self.append_output("• For OneDrive paths, try using a local folder first\n")
            else:
                self.append_output("\n" + "=" * 50 + "\n")
                self.append_output(f"❌ Script completed with errors (return code: {return_code})\n")
                
        except Exception as e:
            self.append_output(f"\n❌ Error running script: {str(e)}\n")
            self.append_output("\nThis might be due to:\n")
            self.append_output("• Missing Python dependencies\n")
            self.append_output("• Invalid file paths\n")
            self.append_output("• Permission issues\n")
        finally:
            # Reset process and re-enable buttons
            self.running_process = None
            self.root.after(0, lambda: [
                self.run_button.config(state="normal"),
                self.stop_button.config(state="disabled")
            ])
    
    def run_script(self):
        if not self.validate_inputs():
            return
        
        try:
            cmd = self.build_command()
            
            # Update button states
            self.run_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Run script in separate thread
            thread = threading.Thread(target=self.run_script_thread, args=(cmd,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script: {str(e)}")
            self.run_button.config(state="normal")
            self.stop_button.config(state="disabled")

def main():
    root = tk.Tk()
    app = PythonToolboxGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
