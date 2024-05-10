import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import shutil
import subprocess

metadata = []
source_directory = 'sample_output'  # Replace with your source directory
directory_path = 'sample_output'


def media_management(source_directory):
    media_types = {
        '.mp3': 'Audio',
        '.wav': 'Audio',
        '.mp4': 'Video',
        '.avi': 'Video',
        '.jpg': 'Images',
        '.png': 'Images',
        '.pdf': 'pdf files',
        '.docx': 'text files',
        '.txt': 'text files'
    }

    for file in os.listdir(source_directory):
        if os.path.isfile(os.path.join(source_directory, file)):
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in media_types:
                media_directory = media_types[file_extension]
                media_path = os.path.join(source_directory, media_directory)
                if not os.path.exists(media_path):
                    os.makedirs(media_path)
                shutil.move(os.path.join(source_directory, file), os.path.join(media_path, file))


def generate_metadata(directory):
    metadata = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.relpath(file_path, directory)
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(file)[1]
            file_metadata = {
                'filename': file_name,
                'size': file_size,
                'extension': file_extension
            }
            metadata.append(file_metadata)
    return metadata


def select_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)


def add_file():
    global destination_entry
    global status_label
    global file_entry

    if file_entry.get() == "":
        messagebox.showinfo("error", "file is not defined")
        return

    file_path = file_entry.get()

    if destination_entry.get() == "":
        messagebox.showinfo("error", "destination is not defined")
        return

    destination_folder = destination_entry.get()

    try:
        shutil.copy(file_path, destination_folder)
        messagebox.showinfo("success", "file added successfully")
    except Exception as e:
        messagebox.showinfo("error", str(e))


def create_gui():
    global file_entry
    global destination_entry
    global status_label

    window = tk.Tk()
    window.title("Add File to Destination")
    window.geometry("600x200")
    style = ttk.Style(window)
    window.tk.call("source", "forest-light.tcl")
    window.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")
    


    frame = ttk.Frame(window)
    frame.pack(pady=10)
    

    file_label = ttk.Label(frame, text="Select File:")
    file_label.grid(row=0, column=0)

    file_entry = ttk.Entry(frame, width=30)
    file_entry.grid(row=0, column=1)

    file_button = ttk.Button(frame, text="Browse", command=select_file)
    file_button.grid(row=0, column=2)

    dest_label = ttk.Label(frame, text="Destination Folder:")
    dest_label.grid(row=1, column=0)

    destination_entry = ttk.Entry(frame, width=30)
    destination_entry.grid(row=1, column=1)

    add_button = ttk.Button(frame, text="Add File", command=add_file)
    add_button.grid(row=2, column=1, pady=10)

    status_label = ttk.Label(frame, text="")
    status_label.grid(row=3, column=1)


def delete_file():
    global status_label
    if file_entry is None:
        messagebox.showinfo("Error", "File is not defined")
        return

    file_path = file_entry.get()

    if not file_path:
        messagebox.showinfo("Error", "File path is empty")
        return

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Success", "File deleted successfully")
        else:
            messagebox.showinfo("Error", "File not found")
    except Exception as e:
        messagebox.showinfo("Error", str(e))


def create_gui1():
    global file_entry
    global destination_entry
    global status_label

    window = tk.Tk()
    window.title("Search and Delete File")
    window.geometry("400x200")
    style = ttk.Style(window)
    window.tk.call("source", "forest-light.tcl")
    window.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")

    frame = ttk.Frame(window)
    frame.pack(pady=10)

    file_label = ttk.Label(frame, text="File:")
    file_label.grid(row=0, column=0)

    file_entry = ttk.Entry(frame, width=30)
    file_entry.grid(row=0, column=1)

    file_button = ttk.Button(frame, text="Browse", command=select_file)
    file_button.grid(row=0, column=2)

    delete_button = ttk.Button(frame, text="Delete File", command=delete_file)
    delete_button.grid(row=1, column=1, pady=10)

    status_label = ttk.Label(frame, text="")
    status_label.grid(row=2, column=1)


def generate_thumbnail():
    global file_entry, output_entry, width_entry, height_entry
    input_file = file_entry.get()
    output_file = output_entry.get()
    width = int(width_entry.get())
    height = int(height_entry.get())

    if not input_file:
        messagebox.showinfo("Error", "Input file not selected")
        return

    if not output_file:
        messagebox.showinfo("Error", "Output file not specified")
        return

    if not width or not height:
        messagebox.showinfo("Error", "Width and height must be specified")
        return

    try:
        subprocess.run([
            "ffmpeg",
            "-i", input_file,
            "-vf", f"scale={width}:{height}",
            "-vframes", "1",
            output_file
        ], check=True)
        messagebox.showinfo("Success", "Thumbnail generated successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showinfo("Error", f"Error generating thumbnail: {e}")


def select_input_file():
    global file_entry
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


def select_output_file():
    global output_entry
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)


def create_gui3():
    global file_entry, output_entry, width_entry, height_entry
    window = tk.Tk()
    window.title("Thumbnail Generator")
    window.geometry("600x300")
    style = ttk.Style(window)
    window.tk.call("source", "forest-light.tcl")
    window.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")


    title_label = ttk.Label(window, text="Thumbnail Generator", font=("Helvetica", 14, "bold"))
    title_label.pack()

    frame = ttk.Frame(window)
    frame.pack()
    widgets_frame = ttk.LabelFrame(frame, text="Thumbnail")
    widgets_frame.grid(row=0, column=0, padx=20, pady=10)

    input_label = ttk.Label(widgets_frame, text="Input File:")
    input_label.grid(row=0, column=0)

    file_entry = ttk.Entry(widgets_frame, width=30)
    file_entry.grid(row=0, column=1)

    input_button = ttk.Button(widgets_frame, text="Browse", command=select_input_file)
    input_button.grid(row=0, column=2)

    output_label = ttk.Label(widgets_frame, text="Output File:")
    output_label.grid(row=1, column=0)

    output_entry = ttk.Entry(widgets_frame, width=30)
    output_entry.grid(row=1, column=1)

    output_button = ttk.Button(widgets_frame, text="Browse", command=select_output_file)
    output_button.grid(row=1, column=2)

    width_label = ttk.Label(widgets_frame, text="Width:")
    width_label.grid(row=2, column=0)

    width_entry = ttk.Entry(widgets_frame, width=10)
    width_entry.grid(row=2, column=1)

    height_label = ttk.Label(widgets_frame, text="Height:")
    height_label.grid(row=2, column=2)

    height_entry = ttk.Entry(widgets_frame, width=10)
    height_entry.grid(row=2, column=3)

    generate_button = ttk.Button(widgets_frame, text="Generate Thumbnail", command=generate_thumbnail)
    generate_button.grid(row=3, column=1, pady=10)


def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")

def button1_click():
    media_management(source_directory)
    messagebox.showinfo("sorted","The files are sorted based on the file types!")

def button2_click():
    global metadata
    metadata = generate_metadata(directory_path)
    with open ("metadata.txt",'w') as f:
        for file_metadata in metadata:
         f.write(str(file_metadata)+'\n')
    messagebox.showinfo("metadata", "The metadata has been generated!")

    
def button3_click():
    create_gui()

def button4_click():
    create_gui1()

def button5_click():
    create_gui3()



# Create the main window
window = tk.Tk()
window.title("FileFlow")
window.geometry("400x400")

style = ttk.Style(window)
window.tk.call("source", "forest-light.tcl")
window.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

# Heading Label
heading_label = tk.Label(window, text="FileFlow", font=("Helvetica", 18, "bold"))
heading_label.pack(pady=10)
heading_label1 = tk.Label(window, text="The Smart File Manager", font=("Helvetica", 10))
heading_label1.pack(pady=1)

# Button Frame
frame = ttk.Frame(window)
frame.pack()
widgets_frame = ttk.LabelFrame(frame, text="Menu")
widgets_frame.grid(row=0, column=0, padx=20, pady=10)

# Create and configure the buttons
button1 = ttk.Button(widgets_frame, text="Sort Files", command=button1_click)
button2 = ttk.Button(widgets_frame, text="Generate Metadata", command=button2_click)
button3 = ttk.Button(widgets_frame, text="Add File", command=button3_click)
button4 = ttk.Button(widgets_frame, text="Delete File", command=button4_click)
button5 = ttk.Button(widgets_frame, text="Generate Thumbnail", command=button5_click)

# Add the buttons to the window
button1.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
button2.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
button3.grid(row=2, column=0, pady=5, padx=10, sticky="ew")
button4.grid(row=3, column=0, pady=5, padx=10, sticky="ew")
button5.grid(row=4, column=0, pady=5, padx=10, sticky="ew")

mode_switch = ttk.Checkbutton(widgets_frame, text="Mode", style="Switch", command=toggle_mode)
mode_switch.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

# Start the main event loop
window.mainloop()
