"""
Image-to-Image Filter Application
A simple GUI application for applying filters to images using Tkinter and Pillow
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os


class ImageFilterApp:
    """Main application class for the Image Filter App"""
    
    def __init__(self, root):
        """Initialize the application window and components"""
        self.root = root
        self.root.title("Image Filter Application")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables to store images
        self.original_image = None
        self.processed_image = None
        self.display_image = None
        
        # Create the GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        
        # Main title
        title_label = tk.Label(
            self.root, 
            text="Image Filter Application", 
            font=("Arial", 20, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Frame for buttons
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack()
        
        # Upload button
        upload_btn = tk.Button(
            button_frame,
            text="Upload Image",
            command=self.upload_image,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="Save Image",
            command=self.save_image,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2",
            state=tk.DISABLED
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        self.save_btn = save_btn
        
        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_image,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Filter selection frame
        filter_frame = tk.LabelFrame(
            self.root,
            text="Select Filter",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        filter_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Filter buttons
        filters = [
            ("Black & White", self.apply_black_white),
            ("Blur", self.apply_blur),
            ("Sharpen", self.apply_sharpen),
            ("Cartoon", self.apply_cartoon),
            ("Edge Detection", self.apply_edge_detection)
        ]
        
        for filter_name, filter_func in filters:
            btn = tk.Button(
                filter_frame,
                text=filter_name,
                command=filter_func,
                font=("Arial", 10),
                padx=15,
                pady=8,
                relief=tk.RAISED,
                cursor="hand2",
                state=tk.DISABLED
            )
            btn.pack(side=tk.LEFT, padx=5)
            # Store reference to enable/disable later
            if not hasattr(self, 'filter_buttons'):
                self.filter_buttons = []
            self.filter_buttons.append(btn)
        
        # Image display frame
        display_frame = tk.Frame(self.root, bg="lightgray", padx=10, pady=10)
        display_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Canvas for displaying images
        self.canvas = tk.Canvas(
            display_frame,
            bg="white",
            width=800,
            height=500
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Please upload an image to get started",
            font=("Arial", 10),
            fg="gray",
            pady=5
        )
        self.status_label.pack()
        
    def upload_image(self):
        """Open file dialog to select and load an image"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Open and store the original image
                self.original_image = Image.open(file_path)
                self.processed_image = self.original_image.copy()
                
                # Enable filter buttons
                for btn in self.filter_buttons:
                    btn.config(state=tk.NORMAL)
                self.save_btn.config(state=tk.NORMAL)
                
                # Display the image
                self.display_image_on_canvas(self.original_image)
                
                # Update status
                filename = os.path.basename(file_path)
                self.status_label.config(
                    text=f"Image loaded: {filename}",
                    fg="green"
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image_on_canvas(self, image):
        """Display the image on the canvas, resizing if necessary"""
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # If canvas not yet rendered, use default size
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500
        
        # Calculate scaling to fit image in canvas
        img_width, img_height = image.size
        scale_w = (canvas_width - 20) / img_width
        scale_h = (canvas_height - 20) / img_height
        scale = min(scale_w, scale_h, 1.0)  # Don't upscale
        
        # Resize image
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        display_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage and display
        self.display_image = ImageTk.PhotoImage(display_img)
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.display_image,
            anchor=tk.CENTER
        )
    
    def apply_black_white(self):
        """Convert image to black and white (grayscale)"""
        if self.original_image:
            try:
                self.processed_image = self.original_image.convert("L").convert("RGB")
                self.display_image_on_canvas(self.processed_image)
                self.status_label.config(text="Filter applied: Black & White", fg="blue")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    def apply_blur(self):
        """Apply blur filter to the image"""
        if self.original_image:
            try:
                self.processed_image = self.original_image.filter(ImageFilter.BLUR)
                self.display_image_on_canvas(self.processed_image)
                self.status_label.config(text="Filter applied: Blur", fg="blue")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    def apply_sharpen(self):
        """Apply sharpen filter to the image"""
        if self.original_image:
            try:
                self.processed_image = self.original_image.filter(ImageFilter.SHARPEN)
                self.display_image_on_canvas(self.processed_image)
                self.status_label.config(text="Filter applied: Sharpen", fg="blue")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    def apply_cartoon(self):
        """Apply cartoon-like effect to the image"""
        if self.original_image:
            try:
                # Create cartoon effect by:
                # 1. Reducing colors (quantization)
                # 2. Applying edge enhancement
                img = self.original_image.copy()
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Reduce colors for cartoon effect
                img = img.quantize(colors=64).convert('RGB')
                
                # Apply slight edge enhancement
                img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
                
                # Increase saturation slightly
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.2)
                
                self.processed_image = img
                self.display_image_on_canvas(self.processed_image)
                self.status_label.config(text="Filter applied: Cartoon", fg="blue")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    def apply_edge_detection(self):
        """Apply edge detection filter to the image"""
        if self.original_image:
            try:
                # Convert to grayscale first
                gray = self.original_image.convert("L")
                # Apply edge detection filter
                edges = gray.filter(ImageFilter.FIND_EDGES)
                # Convert back to RGB for display
                self.processed_image = edges.convert("RGB")
                self.display_image_on_canvas(self.processed_image)
                self.status_label.config(text="Filter applied: Edge Detection", fg="blue")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    def save_image(self):
        """Save the processed image to a file"""
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(
                title="Save Image As",
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                try:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Success", f"Image saved successfully to:\n{file_path}")
                    self.status_label.config(text=f"Image saved: {os.path.basename(file_path)}", fg="green")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No processed image to save!")
    
    def reset_image(self):
        """Reset to the original image"""
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.display_image_on_canvas(self.original_image)
            self.status_label.config(text="Image reset to original", fg="orange")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

