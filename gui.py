import tkinter as tk
from tkinter import filedialog as fd

from tkPDFViewer import tkPDFViewer as pdf


def handle_open():
    filetypes = (
        ("PDF files", "*.pdf"),
    )

    filename = fd.askopenfilename(
        title="Choose a pdf",
        initialdir=".",
        filetypes=filetypes
    )

    print(filename)

    # viewer_original = pdf.ShowPdf()
    # frm_original = viewer_original.pdf_view(
    #   self.preview_frame,
    #  pdf_location=r"b.pdf",
    # width=100,
    # height=100
    # )
    # frm_original.pack(side="left")


def handle_save():
    print("SAVE")


def handle_convert(preview_frame):
    print("CONVERT")
    viewer_converted = pdf.ShowPdf()
    frm_converted = viewer_converted.pdf_view(
        preview_frame,
        pdf_location=r"a.pdf",
        width=100,
        height=100
    )
    frm_converted.pack(side="left")


class Gui:
    def __init__(self):
        self.window = tk.Tk()

        self.button_frame = tk.Frame(master=self.window, width=200, height=100, bg="red")
        self.preview_frame = tk.Frame(master=self.window, width=200, height=100, bg="yellow")

        self.button_frame.columnconfigure(0, weight=1, minsize=200)
        self.button_frame.rowconfigure([0, 1, 2], weight=1, minsize=75)

        self.btn_open = tk.Button(
            master=self.button_frame,
            text="Open",
            width=8,
            bg="black",
            fg="white",
            borderwidth=2,
            relief=tk.RAISED,
            command=handle_open
        )

        self.btn_save = tk.Button(
            master=self.button_frame,
            text="Save",
            width=8,
            bg="black",
            fg="white",
            borderwidth=2,
            relief=tk.RAISED,
            command=handle_save
        )

        self.btn_convert = tk.Button(
            master=self.button_frame,
            text="Convert",
            width=8,
            bg="black",
            fg="white",
            borderwidth=2,
            relief=tk.RAISED,
            command=handle_convert
        )
        # btn_open.bind("<ButtonRelease-1>", handle_click)

        self.button_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.preview_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.btn_open.grid(row=0, column=0, padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, padx=5, pady=5)
        self.btn_convert.grid(row=2, column=0, padx=5, pady=5)

        self.window.mainloop()


if __name__ == "__main__":
    gui = Gui()
