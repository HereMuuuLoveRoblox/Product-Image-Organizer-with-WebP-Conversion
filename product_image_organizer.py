"""
Product Image Organizer with WebP Conversion - Advanced Desktop Application
A complete Tkinter-based application for organizing product images and converting them to WebP.
Features: Drag-to-reorder, thumbnail previews, automatic WebP conversion, all in ONE file.

Key Features:
- Thumbnail previews for all images
- Drag-to-reorder images
- Automatic WebP conversion with quality=85
- Smart folder creation with duplicate handling
- Modern UI with clear sections
- Background processing

Requirements:
- Python 3.7+
- Pillow (PIL): pip install Pillow
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
from PIL import Image, ImageTk
import threading


class ProductImageOrganizer:
    """
    Advanced Product Image Organizer with drag-to-reorder and thumbnail previews.
    """

    # Supported image formats
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.webp')
    THUMBNAIL_SIZE = (120, 120)

    def __init__(self, root):
        """Initialize the application window and UI components."""
        self.root = root
        self.root.title("Product Image Organizer")
        self.root.geometry("950x750")
        self.root.resizable(True, True)

        # Application state
        self.selected_images = []  # List of image file paths
        self.output_directory = os.path.dirname(os.path.abspath(__file__))
        self.dragging_index = None  # Track dragging image
        self.thumbnail_cache = {}  # Cache for thumbnails

        # Configure styles
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        """Configure ttk and custom styles for modern look."""
        style = ttk.Style()
        style.theme_use('clam')

        # Define custom colors
        bg_color = '#f0f0f0'
        fg_color = '#333333'
        accent_color = '#0078d4'

        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'), background=bg_color)
        style.configure('TLabel', font=('Segoe UI', 10), background=bg_color)
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TFrame', background=bg_color)

    def setup_ui(self):
        """Create the complete UI with all sections."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)

        # ============== SECTION 1: PRODUCT INFORMATION ==============
        self.create_product_section(main_frame)

        # ============== SECTION 2: OUTPUT FOLDER ==============
        self.create_output_section(main_frame)

        # ============== SECTION 3: IMAGE MANAGER ==============
        self.create_image_manager_section(main_frame)

        # ============== SECTION 4: ACTION PANEL ==============
        self.create_action_panel(main_frame)

    def create_product_section(self, parent):
        """
        TOP SECTION: Product Information
        Fields for product name and image prefix
        """
        section_frame = ttk.LabelFrame(parent, text="📦 Product Information", padding="12")
        section_frame.grid(row=0, column=0, sticky=tk.EW, pady=(0, 15))
        section_frame.columnconfigure(1, weight=1)

        # Product Name
        ttk.Label(section_frame, text="Product Name:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=8
        )
        self.product_name_var = tk.StringVar()
        product_entry = ttk.Entry(section_frame, textvariable=self.product_name_var, font=('Segoe UI', 10))
        product_entry.grid(row=0, column=1, sticky=tk.EW, pady=8)
        product_entry.insert(0, "")

        # Image Prefix
        ttk.Label(section_frame, text="Image Prefix:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=8
        )
        self.prefix_var = tk.StringVar()
        prefix_entry = ttk.Entry(section_frame, textvariable=self.prefix_var, font=('Segoe UI', 10))
        prefix_entry.grid(row=1, column=1, sticky=tk.EW, pady=8)
        prefix_entry.insert(0, "")

    def create_output_section(self, parent):
        """
        OUTPUT FOLDER: Allow users to select where to create folders
        """
        section_frame = ttk.LabelFrame(parent, text="📁 Output Folder", padding="12")
        section_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 15))
        section_frame.columnconfigure(1, weight=1)

        # Display current output directory
        self.output_dir_var = tk.StringVar(value=self.output_directory)
        dir_entry = ttk.Entry(section_frame, textvariable=self.output_dir_var, state=tk.DISABLED, font=('Segoe UI', 10))
        dir_entry.grid(row=0, column=0, sticky=tk.EW, columnspan=2, pady=8)

        # Browse button
        ttk.Button(section_frame, text="📂 Browse...", command=self.browse_output_directory, width=20).grid(
            row=0, column=2, padx=(10, 0), pady=8
        )

    def create_image_manager_section(self, parent):
        """
        MIDDLE SECTION: Image Manager with thumbnails and drag-to-reorder
        """
        section_frame = ttk.LabelFrame(parent, text="🖼️ Image Manager & WebP Converter", padding="12")
        section_frame.grid(row=2, column=0, sticky=tk.NSEW, pady=(0, 15))
        section_frame.columnconfigure(0, weight=1)
        section_frame.rowconfigure(2, weight=1)
        parent.rowconfigure(2, weight=1)

        # Add Images button
        button_frame = ttk.Frame(section_frame)
        button_frame.grid(row=0, column=0, sticky=tk.EW, pady=(0, 10))

        ttk.Button(button_frame, text="➕ Add Images", command=self.add_images, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(button_frame, text="or drag and drop images below", foreground="#666666").pack(side=tk.LEFT)

        # Instructions
        instructions_frame = ttk.Frame(section_frame)
        instructions_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))
        ttk.Label(
            instructions_frame,
            text="💡 Drag to reorder | First = MAIN image | All will convert to WebP with quality=85",
            foreground="#0078d4",
            font=('Segoe UI', 9, 'italic')
        ).pack(side=tk.LEFT)

        # Image list with scrollbar
        list_frame = ttk.Frame(section_frame)
        list_frame.grid(row=2, column=0, sticky=tk.NSEW)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Canvas for scrolling
        self.canvas = tk.Canvas(list_frame, bg='white', highlightthickness=1, highlightbackground='#cccccc')
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Frame inside canvas for images
        self.images_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.images_frame, anchor=tk.NW)

        # Bind canvas events
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.images_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind_all('<Button-4>', self._on_mousewheel)
        self.canvas.bind_all('<Button-5>', self._on_mousewheel)

        # Enable drag and drop to canvas
        self.setup_drag_drop()

    def _on_canvas_configure(self, event):
        """Update scroll region on canvas resize."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_frame_configure(self, event):
        """Update canvas window width."""
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width() - 20)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, 'units')
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, 'units')

    def create_action_panel(self, parent):
        """
        BOTTOM SECTION: Action buttons (Reset and Process)
        """
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=3, column=0, sticky=tk.EW, pady=(10, 0))

        # Control buttons
        ttk.Button(action_frame, text="🔄 Reset", command=self.reset_all, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="❌ Clear Images", command=self.clear_images, width=20).pack(side=tk.LEFT, padx=(0, 10))

        # Spacer
        spacer = ttk.Frame(action_frame)
        spacer.pack(side=tk.LEFT, expand=True)

        # Main action button
        ttk.Button(action_frame, text="✅ Convert to WebP & Organize", command=self.process_images, width=30).pack(side=tk.RIGHT)

    def setup_drag_drop(self):
        """Enable drag and drop support."""
        try:
            import tkinterdnd2 as tkdnd
            self.canvas.drop_target_register(tkdnd.DND_FILES)
            self.canvas.dnd_bind('<<Drop>>', lambda event: self.drop_files(event.data))
        except ImportError:
            # Fallback without drag-drop support
            pass

    def drop_files(self, data):
        """Handle dropped files."""
        try:
            files = self.parse_dropped_files(data)
            for file_path in files:
                self.add_image(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add files: {str(e)}")

    def parse_dropped_files(self, data):
        """Parse dropped file paths."""
        if isinstance(data, str):
            data = data.strip('{}')
            import re
            files = re.findall(r'"[^"]*"|\S+', data)
            return [f.strip('"') for f in files]
        return []

    def browse_output_directory(self):
        """Open folder dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Folder")
        if directory:
            self.output_directory = directory
            self.output_dir_var.set(directory)

    def add_images(self):
        """Open file dialog to select images."""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp"), ("All Files", "*.*")],
        )
        for file_path in files:
            self.add_image(file_path)

    def add_image(self, file_path):
        """Add image to list if valid format."""
        file_path = str(file_path).strip('"')

        # Validate file
        if not os.path.isfile(file_path):
            return

        if not any(file_path.lower().endswith(fmt) for fmt in self.SUPPORTED_FORMATS):
            messagebox.showwarning("Unsupported Format", f"'{os.path.basename(file_path)}' is not supported.\nSupported: {', '.join(self.SUPPORTED_FORMATS)}")
            return

        if file_path not in self.selected_images:
            self.selected_images.append(file_path)
            self.update_image_display()

    def get_thumbnail(self, image_path):
        """
        Get or create a thumbnail for an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            PhotoImage object for the thumbnail
        """
        if image_path in self.thumbnail_cache:
            return self.thumbnail_cache[image_path]

        try:
            img = Image.open(image_path)
            img.thumbnail(self.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            self.thumbnail_cache[image_path] = photo
            return photo
        except Exception as e:
            print(f"Error loading thumbnail for {image_path}: {e}")
            return None

    def update_image_display(self):
        """Update the image list display with thumbnails."""
        # Clear existing widgets
        for widget in self.images_frame.winfo_children():
            widget.destroy()

        # Create image items
        for index, image_path in enumerate(self.selected_images):
            self.create_image_item(index, image_path)

    def create_image_item(self, index, image_path):
        """
        Create a visual item for an image in the list.
        
        Args:
            index: Position in the list
            image_path: Path to the image file
        """
        # Item frame
        item_frame = tk.Frame(self.images_frame, bg='white', relief=tk.RAISED, borderwidth=1)
        item_frame.pack(fill=tk.X, padx=5, pady=5)

        # Left: Thumbnail and drag handle
        left_frame = tk.Frame(item_frame, bg='white')
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Drag handle indicator
        drag_label = tk.Label(left_frame, text="☰", font=('Arial', 16), bg='white', fg='#999999', cursor='hand2')
        drag_label.pack()

        # Thumbnail
        thumbnail = self.get_thumbnail(image_path)
        if thumbnail:
            thumb_label = tk.Label(left_frame, image=thumbnail, bg='white')
            thumb_label.image = thumbnail  # Keep a reference
            thumb_label.pack(pady=(5, 0))

        # Middle: File info
        middle_frame = tk.Frame(item_frame, bg='white')
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File name
        filename = os.path.basename(image_path)
        ttk.Label(middle_frame, text=filename, font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)

        # File path
        ttk.Label(middle_frame, text=image_path, font=('Segoe UI', 9), foreground='#666666').pack(anchor=tk.W)

        # Image type badge
        if index == 0:
            badge_frame = tk.Frame(middle_frame, bg='#2ecc71')
            badge_frame.pack(anchor=tk.W, pady=(5, 0))
            tk.Label(badge_frame, text="★ MAIN IMAGE ★", font=('Segoe UI', 9, 'bold'), bg='#2ecc71', fg='white', padx=8, pady=3).pack()
        else:
            ttk.Label(middle_frame, text=f"Gallery Image #{index}", font=('Segoe UI', 9, 'italic'), foreground='#0078d4').pack(anchor=tk.W, pady=(5, 0))

        # Right: Buttons
        right_frame = tk.Frame(item_frame, bg='white')
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        ttk.Button(right_frame, text="✕ Remove", command=lambda: self.remove_image(index), width=12).pack()

        # Bind drag events
        for widget in [item_frame, left_frame, drag_label, middle_frame]:
            widget.bind('<Button-1>', lambda e: self.start_drag(e, index))
            widget.bind('<B1-Motion>', lambda e: self.on_drag(e, index))
            widget.bind('<ButtonRelease-1>', lambda e: self.end_drag(e))

    def start_drag(self, event, index):
        """Start dragging an image."""
        self.dragging_index = index

    def on_drag(self, event, index):
        """Handle dragging motion (can be extended for visual feedback)."""
        pass

    def end_drag(self, event):
        """End dragging an image."""
        if self.dragging_index is not None and event.widget.master:
            # Get the widget under cursor
            x = self.root.winfo_pointerx() - self.root.winfo_rootx()
            y = self.root.winfo_pointery() - self.root.winfo_rooty()

            # Find which image frame is under cursor
            target_frame = self.root.winfo_containing(x, y)
            if target_frame:
                for i, image_path in enumerate(self.selected_images):
                    if target_frame.winfo_parent() == str(self.images_frame.winfo_id()):
                        if i != self.dragging_index and i is not None:
                            # Swap images
                            self.selected_images[self.dragging_index], self.selected_images[i] = (
                                self.selected_images[i],
                                self.selected_images[self.dragging_index],
                            )
                            self.update_image_display()
                            break

        self.dragging_index = None

    def remove_image(self, index):
        """Remove an image from the list."""
        if 0 <= index < len(self.selected_images):
            del self.selected_images[index]
            self.update_image_display()

    def clear_images(self):
        """Clear all images."""
        if self.selected_images:
            if messagebox.askyesno("Clear Images", "Remove all images?"):
                self.selected_images.clear()
                self.update_image_display()

    def reset_all(self):
        """Reset all fields and images."""
        if messagebox.askyesno("Reset All", "Reset all fields and images?"):
            self.product_name_var.set("")
            self.prefix_var.set("")
            self.selected_images.clear()
            self.update_image_display()

    def create_product_folder(self, base_path, product_name):
        """
        Create product folder, handling duplicates.
        
        Args:
            base_path: Base directory
            product_name: Product folder name
            
        Returns:
            Path to created folder
        """
        folder_path = os.path.join(base_path, product_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return folder_path

        # Handle duplicates
        counter = 1
        while True:
            new_folder_name = f"{product_name} ({counter})"
            new_folder_path = os.path.join(base_path, new_folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                return new_folder_path
            counter += 1

    def get_file_extension(self, file_path):
        """Get file extension."""
        return os.path.splitext(file_path)[1]

    def rename_and_copy_images(self, folder_path, prefix):
        """
        Convert images to WebP and save to folder.
        
        Args:
            folder_path: Destination folder
            prefix: Image prefix for renaming
            
        Returns:
            List of created files
        """
        created_files = []

        for index, image_path in enumerate(self.selected_images):
            try:
                # Open image with PIL
                img = Image.open(image_path)
                
                # Convert RGBA to RGB (for PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    # Handle palette mode
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    # Paste image onto background
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    # Convert other modes to RGB
                    img = img.convert('RGB')
                
                # Determine the filename with .webp extension
                if index == 0:
                    # Main image
                    filename = f"{prefix}_Main.webp"
                else:
                    # Gallery images
                    gallery_num = str(index).zfill(2)
                    filename = f"{prefix}_Gallery{gallery_num}.webp"

                # Create the destination path
                dest_path = os.path.join(folder_path, filename)

                # Save as WebP with quality=85
                img.save(dest_path, 'WEBP', quality=85, method=6)
                created_files.append(filename)

            except Exception as e:
                messagebox.showerror("Conversion Error", f"Failed to convert '{os.path.basename(image_path)}': {str(e)}")
                return created_files

        return created_files

    def process_images(self):
        """Main processing function."""
        if not self.validate_input():
            return

        product_name = self.product_name_var.get().strip()
        prefix = self.prefix_var.get().strip()

        # Run processing in a separate thread to prevent UI freezing
        thread = threading.Thread(target=self._process_images_thread, args=(product_name, prefix))
        thread.daemon = True
        thread.start()

    def _process_images_thread(self, product_name, prefix):
        """Process images in a background thread."""
        try:
            output_dir = self.output_directory
            product_folder = self.create_product_folder(output_dir, product_name)
            created_files = self.rename_and_copy_images(product_folder, prefix)

            if created_files:
                # Show success message on main thread
                self.root.after(0, lambda: self._show_success(product_folder, created_files))
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No images were processed"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Processing Error", f"An error occurred: {str(e)}"))

    def _show_success(self, folder_path, files):
        """Show success message and reset UI."""
        message = f"✅ Images converted to WebP and organized successfully!\n\n"
        message += f"📁 Folder: {folder_path}\n\n"
        message += f"📄 WebP Files created:\n"
        for filename in files:
            message += f"  • {filename}\n"

        messagebox.showinfo("✓ WebP Conversion Complete", message)

        # Reset form
        self.product_name_var.set("")
        self.prefix_var.set("")
        self.selected_images.clear()
        self.update_image_display()

    def validate_input(self):
        """
        Validate user input before processing.
        
        Returns:
            Boolean indicating if input is valid
        """
        product_name = self.product_name_var.get().strip()
        prefix = self.prefix_var.get().strip()

        if not product_name:
            messagebox.showerror("✗ Validation Error", "Please enter a Product Name")
            return False

        if not prefix:
            messagebox.showerror("✗ Validation Error", "Please enter an Image Prefix")
            return False

        if not self.selected_images:
            messagebox.showerror("✗ Validation Error", "Please select at least one image")
            return False

        return True


def main():
    """Create and run the main application window."""
    root = tk.Tk()
    app = ProductImageOrganizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
