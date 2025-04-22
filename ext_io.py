import tkinter as tk
from tkinter import filedialog

def choose_tiff_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Choose your TIFF files",
        filetypes=[("TIFF files", "*.tif *.tiff")]
    )
    return list(file_paths)


# def choose_tiff_file():
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window
#     file_path = filedialog.askopenfilename(
#         title="Select a TIFF file",
#         filetypes=[("TIFF files", "*.tif *.tiff")]
#     )
#     print("Selected file:", file_path)
#     return file_path

# Example usage
# if __name__ == "__main__":
#     selected_file = choose_tiff_file()
