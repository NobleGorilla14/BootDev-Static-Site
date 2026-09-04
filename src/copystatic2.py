import os
import shutil


def copy_files_recursive(source_dir_path: str, dest_dir_path: str, logfile: str) -> None:
    sourcedir_abs = os.path.abspath(source_dir_path)
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        with open(f"{logfile}", "a", encoding="utf-8") as f:
            f.write(f"{dest_dir_path} did not exist\n")
            f.write(f"{dest_dir_path} has be created\n")
    
    for filename in os.listdir(sourcedir_abs):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        with open(f"{logfile}", "a", encoding="utf-8") as f:
            f.write(f" * Copied {from_path} -> {dest_path}\n")
        
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path, logfile)
