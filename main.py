import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable
import os, subprocess, threading

root = tk.Tk()
root.geometry("450x450")
root.title("Python to EXE converter 2")
root.resizable(False, False)
root.attributes("-topmost", True)
root.attributes("-toolwindow", True)

def log(msg: str = ""):
    try:
        console.config(state="normal")
        console.insert("end", msg + "\n")
        console.see("end")
        console.config(state="disabled")
        return True
    except Exception as e:
        return e

def run_command(cmd: str = "echo Hello, world!", on_done: Callable | None = None):
    def task():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True
            )
            for line in process.stdout:
                log(line.rstrip())
            process.wait()
            if callable(on_done):
                on_done()
        except Exception as e:
            log(f"[BŁĄD] {e}")
    threading.Thread(target=task, daemon=True).start()

def safe_task(val: bool, func: Callable | None = None):
    if val:
        root.protocol("WM_DELETE_WINDOW", func)
    else:
        root.protocol("WM_DELETE_WINDOW", root.destroy)

def end_of_conversion():
    safe_task(False)
    messagebox.showinfo("Info", "Conversion completed.")

def browse_file(entry: tk.Widget):
    dialog = filedialog.askopenfilename(title="Select file...", filetypes=[("Python files", "*.py")])

    if dialog != "" and dialog != None:
        entry.delete(0, tk.END)
        entry.insert(0, os.path.abspath(dialog))

def browse_icon(entry: tk.Widget):
    dialog = filedialog.askopenfilename(title="Select file...", filetypes=[("ICO files", "*.ico")])

    if dialog != "" and dialog != None:
        entry.delete(0, tk.END)
        entry.insert(0, os.path.abspath(dialog))

def browse_folder(entry: tk.Widget):
    dialog = filedialog.askdirectory(title="Select file...")

    if dialog != "" and dialog != None:
        entry.delete(0, tk.END)
        entry.insert(0, os.path.abspath(dialog))

def convert(file_path: str, final_dir: str, icon_path: str | None, no_console: bool):
    button7.config(state="disabled")

    if not os.path.isfile(file_path):
        messagebox.showerror("Error", "The input file does not exist.")
        button7.config(state="normal")
        return
    
    if not os.path.isdir(final_dir):
        messagebox.showerror("Error", "The destination folder does not exist.")
        button7.config(state="normal")
        return
    
    safe_task(
        True,
        lambda: messagebox.showerror("Error", "You cannot close this window during conversion.")
    )
    log("Starting conversion...")

    command = f'pyinstaller --onefile "{file_path}" --distpath "{final_dir}" --workpath "{os.path.join(final_dir, "build")}" --specpath "{final_dir}"'

    if no_console:
        command += " --noconsole"
    
    if icon_path:
        if not os.path.isfile(icon_path):
            log("Warning: The path to the icon is invalid. The icon will be skipped.")
            messagebox.showwarning("Warning", "The path to the icon is invalid. The icon will be skipped.")
        else:
            command += f' --icon={icon_path}'
    
    def cleanup():
        log("\nConversion compleated!")
        end_of_conversion()
        button7.config(state="normal")
        return
    
    run_command(command, on_done=cleanup)

title = ttk.Label(root, text="Python to EXE converter 2", font=("Consolas", 20, "bold"))
title.pack()

label1 = ttk.Label(root, text="Python file path:")
label1.pack(anchor="nw", padx=5, pady=(20, 0))

frame1 = ttk.Frame(root)
frame1.pack(anchor="nw", padx=5, pady=(5, 0))

entry1 = ttk.Entry(frame1, width=30)
entry1.pack(side="left", ipady=1)

button1 = ttk.Button(frame1, text="Browse...", command=lambda: browse_file(entry1))
button1.pack(side="left", padx=1)

button2 = ttk.Button(frame1, text="C", command=lambda: entry1.delete(0, tk.END), width=3)
button2.pack(side="left", padx=1)

label2 = ttk.Label(root, text="Final path:")
label2.pack(anchor="nw", padx=5, pady=(10, 0))

frame2 = ttk.Frame(root)
frame2.pack(anchor="nw", padx=5, pady=(5, 0))

entry2 = ttk.Entry(frame2, width=30)
entry2.pack(side="left", ipady=1)

button3 = ttk.Button(frame2, text="Browse...", command=lambda: browse_folder(entry2))
button3.pack(side="left", padx=1)

button4 = ttk.Button(frame2, text="C", command=lambda: entry2.delete(0, tk.END), width=3)
button4.pack(side="left", padx=1)

label3 = ttk.Label(root, text="Iocn file path (optional):")
label3.pack(anchor="nw", padx=5, pady=(10, 0))

frame3 = ttk.Frame(root)
frame3.pack(anchor="nw", padx=5, pady=(5, 0))

entry3 = ttk.Entry(frame3, width=30)
entry3.pack(side="left", ipady=1)

button5 = ttk.Button(frame3, text="Browse...", command=lambda: browse_icon(entry3))
button5.pack(side="left", padx=1)

button6 = ttk.Button(frame3, text="C", command=lambda: entry3.delete(0, tk.END), width=3)
button6.pack(side="left", padx=1)

checkbutton1_var = tk.BooleanVar()

checkbutton1 = ttk.Checkbutton(root, text="Hidden console", variable=checkbutton1_var)
checkbutton1.pack(anchor="nw", padx=5, pady=(10, 0))

button7 = ttk.Button(root, text="Convert!", command=lambda: root.after(10, lambda: convert(entry1.get(), entry2.get(), (entry3.get() if entry3.get() != "" else None), checkbutton1_var.get())))
button7.pack(side="bottom", anchor="se", ipadx=10, padx=5, pady=5)

console = tk.Text(root, state="disabled", height=10)
console.pack(side="bottom", expand=True, fill="x", anchor="s")

log("Python to EXE converter 2 has been opened.")

root.mainloop()
