import os
import string
import random
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror

directory = ""


class CheckboxValueError(Exception):
    """
    Raised when there is something wrong with the checkboxes
    """
    pass


class TextboxValueError(Exception):
    """
    Raised when there is something wrong with the text boxes
    """
    pass


def show_error(self, exc, val, tb):
    """
    Shows an error message when there is an exception
    """
    showerror("Error", message=str(val))


def get_directory():
    global directory
    directory = filedialog.askdirectory(parent=window, title="Please select directory") + "/"
    show_directory_text["text"] = directory


def _get_new_filename():
    """
    Helper function for rando(). Creates filenames according to
    the attributes given from the checkboxes and text box.
    Returns filename as a str.
    """
    rand_str = ""
    length = 0
    text = textbox.get()
    if (len(text) == 0) or (text.isnumeric() is False):
        raise TextboxValueError("You need to enter a number into the textbox!")
    else:
        length = int(text)
        if length == 0:
            raise TextboxValueError("Value in textbox cannot be 0!")

    if (var1.get() == 1) and (var2.get() == 0):  # if letters only
        rand_str = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))
    elif (var1.get() == 0) and (var2.get() == 1):  # if numbers only
        rand_str = ''.join(random.choices(string.digits, k=length))
    elif (var1.get() == 1) and (var2.get() == 1):  # if letters and numbers
        rand_str = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    else:
        raise CheckboxValueError("You need to check one of the boxes!")

    return rand_str


def randomize_filename():
    """
    Renames the files in the chosen directory. Uses _get_new_filename()
    to generate a new filename for each file.
    """
    for count, filename in enumerate(os.listdir(directory)):
        rand_name = _get_new_filename()
        path_segments = os.path.splitext(filename)
        src = directory + filename
        dst = directory + str(rand_name) + path_segments[1]

        os.rename(src, dst)


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("500x225")
    window.resizable(False, False)
    window.title("File Name Randomizer")

    tk.Tk.report_callback_exception = show_error

    frame1 = tk.Frame(window)
    frame2 = tk.Frame(window)
    frame3 = tk.Frame(window)
    frame4 = tk.Frame(window)

    checkboxLabel = tk.Label(frame1, text="File Names will be generated with:")
    var1 = tk.IntVar()
    var2 = tk.IntVar()
    checkbox1 = tk.Checkbutton(frame1, text="Letters", variable=var1, onvalue=1, offvalue=0)
    checkbox2 = tk.Checkbutton(frame1, text="Numbers", variable=var2, onvalue=1, offvalue=0)

    checkboxLabel.pack()
    checkbox1.pack(anchor="w")
    checkbox2.pack(anchor="w")

    textboxLabel = tk.Label(frame2, text="Length of new file name:")
    textbox = tk.Entry(frame2, width=5)
    textbox.insert(0, "8")
    file_explorer_label = tk.Label(frame2, text="Folder directory:")
    file_explorer_button = tk.Button(frame2, text="Browse", width=5, height=1, command=get_directory)

    textboxLabel.grid(row=0, column=0, sticky="w")
    textbox.grid(row=0, column=1, sticky="e")
    file_explorer_label.grid(row=1, column=0, sticky="w")
    file_explorer_button.grid(row=1, column=1, sticky="e")

    show_directory_text = tk.Label(frame3, text="")
    show_directory_text.pack()

    randomize = tk.Button(frame4, text="Randomize", width=25, height=3, command=randomize_filename)
    randomize.pack()

    frame1.pack()
    frame2.pack(padx=10, pady=10)
    frame3.pack()
    frame4.pack(padx=10, pady=10)

    window.mainloop()
