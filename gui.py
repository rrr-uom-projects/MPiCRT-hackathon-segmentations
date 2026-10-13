"""
gui.py
Provides a graphical interface to view medical images and segmentation overlays.
"""
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import helper functions from the local segmentation.py file
from segmentation import load_image, normalize_intensity

def launch_gui():
    """Tkinter GUI setup and execution."""
    root = tk.Tk()
    root.title("CT Slice & Mask Viewer")
    root.geometry("650x700")
    
    canvas_widget = None

    def open_and_display():
        nonlocal canvas_widget
        
        # File dialogs without extensions to prevent macOS crashes
        ct_path = filedialog.askopenfilename(title="Select CT Slice")
        if not ct_path: return
        mask_path = filedialog.askopenfilename(title="Select Mask")
        if not mask_path: return

        ct_img = normalize_intensity(load_image(ct_path))
        mask_img = load_image(mask_path)

        # Clear existing plot
        if canvas_widget:
            canvas_widget.destroy()

        # Build new plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(ct_img, cmap="gray")
        
        if np.any(mask_img):
            ax.contour(mask_img, levels=[0.5], colors="red", linewidths=1)
            
        ax.axis("off")
        ax.set_title(f"CT: {os.path.basename(ct_path)}\nMask: {os.path.basename(mask_path)}", fontsize=10)

        # Embed plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill=tk.BOTH)
        canvas.draw()
        
        plt.close(fig) # Prevent matplotlib memory leaks

    btn = tk.Button(root, text="Load CT & Mask", command=open_and_display, height=2)
    btn.pack(pady=10, fill=tk.X, padx=20)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()