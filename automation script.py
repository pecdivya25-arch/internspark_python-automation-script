import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def log_message(message):
    """Generates logs for operations with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    
    # Write to a log file in the script's directory
    with open("automation_log.txt", "a") as log_file:
        log_file.write(log_line)

def organize_folder_gui():
    # Set up a hidden Tkinter window to handle the folder dialog
    root = tk.Tk()
    root.withdraw()
    
    log_message("--- Starting File Organization Automation (GUI) ---")
    
    # Opens a graphical directory selection box (No command line required!)
    target_directory = filedialog.askdirectory(title="Select the Folder to Organize")
    
    # If the user closes the window or hits cancel
    if not target_directory:
        log_message("Operation cancelled by the user.")
        return

    # Check if directory exists
    if not os.path.exists(target_directory):
        messagebox.showerror("Error", f"The directory '{target_directory}' does not exist.")
        log_message(f"ERROR: The directory '{target_directory}' does not exist.")
        return

    try:
        files = os.listdir(target_directory)
        moved_count = 0
        
        for file in files:
            file_path = os.path.join(target_directory, file)
            
            # Skip directories and the log file itself
            if os.path.isfile(file_path) and file != "automation_log.txt":
                _, extension = os.path.splitext(file)
                extension = extension.lower().strip('.')
                
                # Group files without an extension into 'OTHERS'
                if not extension:
                    extension = "OTHERS"
                
                # Create destination path
                folder_name = f"{extension.upper()} Files"
                destination_folder = os.path.join(target_directory, folder_name)
                
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                    log_message(f"Created folder: {folder_name}")
                
                # Move the file
                destination_file_path = os.path.join(destination_folder, file)
                shutil.move(file_path, destination_file_path)
                log_message(f"Moved: '{file}' -> '{folder_name}/'")
                moved_count += 1
                
        log_message(f"Successfully moved {moved_count} files.")
        
        # Graphical Success Alert
        messagebox.showinfo("Success", f"Organization complete!\nTotal files moved: {moved_count}\n\nLog saved to 'automation_log.txt'.")
        
    except PermissionError:
        messagebox.showerror("Permission Error", "Access denied. Please check folder permissions.")
        log_message("ERROR: Permission denied.")
    except Exception as e:
        messagebox.showerror("Critical Error", f"An unexpected error occurred:\n{str(e)}")
        log_message(f"CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    organize_folder_gui()