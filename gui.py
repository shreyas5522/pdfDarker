import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import PIL
from PIL import Image
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
        # self.progress_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.btn_open.grid(row=0, column=0, padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, padx=5, pady=5)
        self.btn_convert.grid(row=2, column=0, padx=5, pady=5)
        self.progress_bar.grid(row=3, column=0, padx=5, pady=5)

        self.window.mainloop()

    def handle_open(self):
        self.progress_bar.start()
        filetypes = (
            ("PDF files", "*.pdf"),
        )

        filename = fd.askopenfilename(
            title="Choose a pdf",
            initialdir=".",
            filetypes=filetypes
        )
        self.dark.open_file(filename)
        print(filename)
        self.progress_bar.stop()
        # viewer_original = pdf.ShowPdf()
        # frm_original = viewer_original.pdf_view(
        #     self.preview_frame,
        #     pdf_location=filename,
        #     width=100,
        #     height=100
        # )
        # frm_original.pack(side="left")

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
        self.dark.convert()
        # viewer_converted = pdf.ShowPdf()
        # frm_converted = viewer_converted.pdf_view(
        #     self.preview_frame,
        #     pdf_location=r"b.pdf",
        #     width=100,
        #     height=100
        # )
        # frm_converted.pack(side="left")


if __name__ == "__main__":
    gui = Gui()
