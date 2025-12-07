# monitor_crowler/monitor_crowler.py
import shutil, tempfile, threading

lock = threading.RLock()

def update_status(wsl_path: str, ip: str, new_status: int):
    with lock:
        import os
        updated_line = None
        dirp = os.path.dirname(wsl_path)
        fd, tmp = tempfile.mkstemp(dir=dirp)
        os.close(fd)
        with open(wsl_path, "r", encoding="utf-8") as src, open(tmp,"w",encoding="utf-8") as dst:
            for line in src:
                parts=line.strip().split(";")
                if len(parts)==4 and parts[0]==ip:
                    updated_line=f"{parts[0]};{parts[1]};{parts[2]};{new_status}\n"
                else:
                    dst.write(line)
            if updated_line:
                dst.write(updated_line)
        shutil.move(tmp, wsl_path)
