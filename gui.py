import tkinter as tk
from tkinter import filedialog as fd

import pdfDarkererer
import pdfDarkererer as dark
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

    pdfDarkererer.out_filename
    print(filename)

    #viewer_original = pdf.ShowPdf()
    #frm_original = viewer_original.pdf_view(
     #   preview_frame,
      #  pdf_location=r"b.pdf",
       # width=100,
        #height=100
    #)
    #frm_original.pack(side="left")


def handle_save():
    print("SAVE")


def handle_convert():
    print("CONVERT")
    viewer_converted = pdf.ShowPdf()
    frm_converted = viewer_converted.pdf_view(
        preview_frame,
        pdf_location=r"a.pdf",
        width=100,
        height=100
    )
    frm_converted.pack(side="left")


window = tk.Tk()

button_frame = tk.Frame(master=window, width=200, height=100, bg="red")
preview_frame = tk.Frame(master=window, width=200, height=100, bg="yellow")

button_frame.columnconfigure(0, weight=1, minsize=200)
button_frame.rowconfigure([0, 1, 2], weight=1, minsize=75)

btn_open = tk.Button(
    master=button_frame,
    text="Open",
    width=8,
    bg="black",
    fg="white",
    borderwidth=2,
    relief=tk.RAISED,
    command=handle_open
)

btn_save = tk.Button(
    master=button_frame,
    text="Save",
    width=8,
    bg="black",
    fg="white",
    borderwidth=2,
    relief=tk.RAISED,
    command=handle_save
)

btn_convert = tk.Button(
    master=button_frame,
    text="Convert",
    width=8,
    bg="black",
    fg="white",
    borderwidth=2,
    relief=tk.RAISED,
    command=handle_convert
)
# btn_open.bind("<ButtonRelease-1>", handle_click)

button_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
preview_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

btn_open.grid(row=0, column=0, padx=5, pady=5)
btn_save.grid(row=1, column=0, padx=5, pady=5)
btn_convert.grid(row=2, column=0, padx=5, pady=5)

window.mainloop()
