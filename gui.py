import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import PIL
from PIL import Image, ImageTk
from tkPDFViewer import tkPDFViewer as pdf

import pdfDarkererer
import ipyplot


class Gui:
    def __init__(self):
        self.dark = pdfDarkererer.pdfDark()
        self.window = tk.Tk()

        self.button_frame = tk.Frame(master=self.window, width=200, height=100, bg="red")
        self.preview_frame = tk.Frame(master=self.window, width=200, height=100, bg="yellow")

        self.button_frame.columnconfigure(0, weight=1, minsize=200)
        self.button_frame.rowconfigure([0, 1, 2], weight=1, minsize=75)
        self.progress_bar = ttk.Progressbar(self.button_frame, orient="horizontal", mode="indeterminate")

        self.scroll_bar = tk.Scrollbar(self.preview_frame, orient=tk.VERTICAL)
        self.pdf = tk.Text(self.preview_frame, yscrollcommand=self.scroll_bar.set, bg="grey")
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_bar.config(command=self.pdf.yview)

        self.btn_open = tk.Button(
            master=self.button_frame,
            text="Open",
            width=8,
            bg="black",
            fg="white",
            borderwidth=2,
            relief=tk.RAISED,
            command=self.handle_open
        )

        self.btn_save = tk.Button(
            master=self.button_frame,
            text="Save",
            width=8,
            bg="black",
            fg="white",
            borderwidth=2,
            relief=tk.RAISED,
            command=self.handle_save
        )

        self.btn_convert = tk.Button(
            master=self.button_frame,
            text="Convert",
            width=8,
            bg="black",
            fg="white",
            borderwidth=2,
            relief=tk.RAISED,
            command=self.handle_convert
        )

        self.button_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.preview_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.pdf.pack(fill=tk.BOTH, expand=True)

        self.btn_open.grid(row=0, column=0, padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, padx=5, pady=5)
        self.btn_convert.grid(row=2, column=0, padx=5, pady=5)
        self.progress_bar.grid(row=3, column=0, padx=5, pady=5)

        self.pics = []
        self.window.mainloop()

    def progress(self):
        self.progress_bar.start()

    def handle_open(self):
        filetypes = (
            ("PDF files", "*.pdf"),
        )

        filename = fd.askopenfilename(
            title="Choose a pdf",
            initialdir=".",
            filetypes=filetypes
        )

        self.progress_bar.start()
        self.dark.open_file(filename)
        self.progress_bar.stop()

        for i in range(len(self.dark.images)):
            temp_pic = self.dark.images[i].resize((200, 200))
            #temp_pic = temp_pic.resize((200, 200))
            self.pics.append(ImageTk.PhotoImage(temp_pic))

        for pic in self.pics:
            self.pdf.image_create(tk.END, image=pic)
            self.pdf.insert(tk.END, "\n\n")

    def handle_save(self):
        print("SAVE")
        filetypes = (
            ("PDF files", "*.pdf"),
        )

        filename = fd.asksaveasfilename(
            title="Save as...",
            initialdir=".",
            filetypes=filetypes
        )
        self.dark.save(filename)

    def handle_convert(self):
        print("CONVERT")
        self.pics = []
        self.pdf.delete('1.0', tk.END)
        self.dark.convert()
        for i in range(len(self.dark.images_invert)):
            temp_pic = self.dark.images_invert[i].resize((200, 200))
            #temp_pic = temp_pic.resize((200, 200))
            self.pics.append(ImageTk.PhotoImage(temp_pic))

        for pic in self.pics:
            self.pdf.image_create(tk.END, image=pic)
            self.pdf.insert(tk.END, "\n\n")


if __name__ == "__main__":
    gui = Gui()
