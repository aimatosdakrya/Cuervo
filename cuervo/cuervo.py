import tkinter as tk
import subprocess
import threading
from tkinter import filedialog

# SITES TO BE EXCLUDED FROM OUTPUT
EXCLUDED_SITES = [
    '8tracks: https://8tracks.com',
    'Fiverr: https://www.fiverr.com',
    'HackTheBox: https://forum.hackthebox.eu',
    'HackenProof (Hackers): https://hackenproof.com',
    'HudsonRock: https://cavalier.hudsonrock.com',
    'Kick: https://kick.com',
    'LibraryThing: https://www.librarything.com',
    'Lichess: https://lichess.org',
    'NitroType: https://www.nitrotype.com',
    'TLDR Legal: https://tldrlegal.com',
    'TorrentGalaxy: https://torrentgalaxy.to'
]

def run_sherlock():
    username = username_entry.get()
    output_directory = directory_entry.get()

    if not output_directory:
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, "Error: Select a directory to save the output file.\n")
        result_text.yview(tk.END)
        result_text.config(state=tk.DISABLED)
        return

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    
    def target():
        output_file = f"{output_directory}/{username}_result.txt"
        with subprocess.Popen(['sherlock', username], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            with open(output_file, 'w') as f:
                for line in proc.stdout:
                    if not any(site in line for site in EXCLUDED_SITES):
                        if "[*] Search completed with" in line:
                            line = "END OF THE HUNT.\n"
                        result_text.config(state=tk.NORMAL)
                        result_text.insert(tk.END, line)
                        result_text.yview(tk.END)
                        result_text.config(state=tk.DISABLED)
                        f.write(line)

                for line in proc.stderr:
                    if not any(site in line for site in EXCLUDED_SITES):
                        result_text.config(state=tk.NORMAL)
                        result_text.insert(tk.END, f"Error: {line}")
                        result_text.yview(tk.END)
                        result_text.config(state=tk.DISABLED)
                        f.write(f"Error: {line}")

    threading.Thread(target=target).start()

def select_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

window = tk.Tk()
window.title("Cuervo v1.0")
window.iconbitmap('cuervo.ico')
window.geometry("735x450")
window.resizable(False, False)

# COLORS
background_color = 'black'
text_color = 'white'
button_color = '#333333'
button_text_color = 'white'

# BOLD FONT FOR BUTTON AND LABEL TEXT
bold_font = ('Arial', 12, 'bold')
# NORMAL FONT FOR CONSOLE TEXT
normal_font = ('Arial', 12)

window.configure(bg=background_color)

# FRAME FOR USERNAME INPUT
input_frame = tk.Frame(window, bg=background_color)
input_frame.pack(pady=10)

# USERNAME INPUT FIELD
tk.Label(input_frame, text="TARGET USERNAME:", bg=background_color, fg='red', font=bold_font).pack(side=tk.LEFT, padx=(0, 5))
username_entry = tk.Entry(input_frame, bg='white', fg='red', width=50)
username_entry.pack(side=tk.LEFT)

# SEARCH BUTTON
run_button = tk.Button(input_frame, text="SEARCH", command=run_sherlock, bg='black', fg='red', font=bold_font)
run_button.pack(side=tk.LEFT, padx=(5, 0))

# FRAME FOR OUTPUT DIRECTORY INPUT
directory_frame = tk.Frame(window, bg=background_color)
directory_frame.pack(pady=10)

# OUTPUT DIRECTORY INPUT FIELD
tk.Label(directory_frame, text="OUTPUT DIRECTORY:", bg=background_color, fg='red', font=bold_font).pack(side=tk.LEFT, padx=(0, 5))
directory_entry = tk.Entry(directory_frame, bg='white', fg='red', width=50)
directory_entry.pack(side=tk.LEFT)

# BUTTON TO SELECT DIRECTORY
directory_button = tk.Button(directory_frame, text="SELECT", command=select_directory, bg='black', fg='red', font=bold_font)
directory_button.pack(side=tk.LEFT, padx=(5, 0))

# FRAME FOR RESULTS
output_frame = tk.Frame(window)
output_frame.pack(pady=5)

# TEXT FIELD TO DISPLAY RESULTS
result_text = tk.Text(output_frame, width=80, height=20, bg=background_color, fg='red', insertbackground='white', font=normal_font)
result_text.pack(side=tk.LEFT)

# PREVENT THE TEXT FROM BEING EDITABLE
result_text.config(state=tk.DISABLED)

window.mainloop()
