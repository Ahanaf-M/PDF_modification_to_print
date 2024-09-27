import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import io  # For in-memory file handling

# Global variables for file path and number of pages
pdf_path_var = None
num_pages_var = None

# Open file dialog to select PDF file
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )
    if file_path:
        pdf_path_var.set(file_path)

# Define the series-making function
def make_series(n):
    series = []
    for i in range(n):
        if i % 4 == 0 or i % 4 == 3:
            series.append(i)
        elif i % 4 == 1:
            series.append(i + 1)
        else:
            series.append(i - 1)
    return series

# Function to reorder pages in-memory and rotate them, saving as 'rotated_output.pdf'
def reorder_and_rotate():
    try:
        
        num_pages = int(num_pages_var.get())
        filename = pdf_path_var.get()

        # Open input PDF file
        pdf_in = open(filename, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_in)
        total_pages = len(pdf_reader.pages)

        # Adjust the number of pages to be divisible by 4 by adding blank pages
        pages_to_add = (4 - (total_pages % 4)) % 4

        pdf_writer = PyPDF2.PdfWriter()

        # Reorder pages in-memory based on the same logic
        for page in make_series(total_pages):
            pdf_writer.add_page(pdf_reader.pages[page])

        # Add blank pages to make the total divisible by 4
        for _ in range(pages_to_add):
            pdf_writer.add_blank_page(width=210, height=297)  # A4 size in mm (210 x 297)

        # Store reordered PDF in-memory
        memory_buffer = io.BytesIO()
        pdf_writer.write(memory_buffer)
        memory_buffer.seek(0)

        # Read the in-memory reordered PDF
        pdf_reader_mem = PyPDF2.PdfReader(memory_buffer)
        pdf_writer_rotated = PyPDF2.PdfWriter()

        # Adjust num_pages for rotation if it exceeds total pages
        total_adjusted_pages = len(pdf_reader_mem.pages)

        if num_pages > total_adjusted_pages:
            num_pages = total_adjusted_pages

        for i in range(num_pages):
            page = pdf_reader_mem.pages[i]
            # Rotate pages 3 and 4 (180 degrees)
            if i % 4 == 2 or i % 4 == 3:
                page.rotate(180)
            pdf_writer_rotated.add_page(page)

        # Save the final rotated PDF to 'rotated_output.pdf'
        with open('rotated_output.pdf', 'wb') as output_file:
            pdf_writer_rotated.write(output_file)

        pdf_in.close()

        messagebox.showinfo("Success", f"Rotated PDF saved as 'rotated_output.pdf'.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("PDF Modifier for printing made by Ahanaf")

# Initialize the variables
pdf_path_var = tk.StringVar()
num_pages_var = tk.StringVar()

# Layout for file selection
tk.Label(root, text="Select PDF File").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=pdf_path_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=open_file).grid(row=0, column=2, padx=10, pady=10)

# Input field for number of pages for rotation
tk.Label(root, text="Number of Pages for Rotation").grid(row=3, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=num_pages_var, width=40).grid(row=3, column=1, padx=10, pady=10)

# Button to reorder and rotate pages in-memory
tk.Button(root, text="Reorder and Rotate Pages", command=reorder_and_rotate).grid(row=4, column=1, padx=10, pady=10)

# Start the GUI loop
root.mainloop()
