import os
import shutil
from datetime import datetime
from copystatic import copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logfile = f"logfile_{timestamp}.txt"
    with open(f"{logfile}", "w", encoding="utf-8") as f:
        f.write(f"Logfile created at {timestamp}")

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
        with open(f"{logfile}", "a", encoding="utf-8") as f:
            f.write(f"{dir_path_public} exists\n")
            f.write(f"{dir_path_public} deleted and recreated\n")

    copy_files_recursive(dir_path_static, dir_path_public, logfile)
    with open(f"{logfile}", "a", encoding="utf-8") as f:
            f.write(f"Files copied to {dir_path_public}\n")
            f.write(f"From {dir_path_static}\n")


main()

