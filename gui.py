import tkinter as tk
import os
import cv2
import time
from tkinter.filedialog import askopenfilename, asksaveasfilename

from PIL import Image
class gui:

    def save_file():
        global filename
        global dirname
        print(ent_orientation.get())
        print(ent_shape.get())
        print(ent_shapecolor.get())
        print(ent_letter.get())
        print(ent_lettercolor.get())
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        f = open()
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = ent_orientation.get()
            text += ", " + ent_shape.get()
            text += ", " + ent_shapecolor.get()
            text += ", " + ent_letter.get()
            text += ", " + ent_lettercolor.get()
            output_file.write(text)
        window.title(f"Backup Classification - {filepath}")

    window = tk.Tk()
    window.title("Backup Classification")

    frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
    frm_form.pack()

    imgFilePath = ""
    # imgFilePathSpilt = imgFil

    filename = "sample"  # global variable
    dirname = "classified"  # global variable

    labels = [
        "Orientation:",
        "Shape:",
        "Shape Color:",
        "Letter:",
        "Letter Color:"
    ]
    lbl_orientation = tk.Label(master=frm_form, text="Orientation:")
    ent_orientation = tk.Entry(master=frm_form, width=20)
    lbl_orientation.grid(row=0, column=0, sticky="e")
    ent_orientation.grid(row=0, column=1)

    lbl_shape = tk.Label(master=frm_form, text="Shape:")
    ent_shape = tk.Entry(master=frm_form, width=20)
    lbl_shape.grid(row=1, column=0, sticky="e")
    ent_shape.grid(row=1, column=1)

    lbl_shapecolor = tk.Label(master=frm_form, text="Shape Color:")
    ent_shapecolor = tk.Entry(master=frm_form, width=20)
    lbl_shapecolor.grid(row=2, column=0, sticky="e")
    ent_shapecolor.grid(row=2, column=1)

    lbl_letter = tk.Label(master=frm_form, text="Letter:")
    ent_letter = tk.Entry(master=frm_form, width=20)
    lbl_letter.grid(row=3, column=0, sticky="e")
    ent_letter.grid(row=3, column=1)

    lbl_lettercolor = tk.Label(master=frm_form, text="Letter Color:")
    ent_lettercolor = tk.Entry(master=frm_form, width=20)
    lbl_lettercolor.grid(row=4, column=0, sticky="e")
    ent_lettercolor.grid(row=4, column=1)

    frm_buttons = tk.Frame()
    frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

    btn_save = tk.Button(master=frm_buttons, text="Save", command=save_file)
    btn_save.pack(side=tk.RIGHT, padx=10, ipadx=10)

    btn_next = tk.Button()

    # btn_clear = tk.Button(master=frm_buttons, text="Clear")
    # btn_clear.pack(side=tk.RIGHT, ipadx=10)
    # btn_clear.bind("<Button-1>", )

    window.mainloop()
