# Product Image Organizer with WebP Conversion

A **complete Python desktop application** for organizing product images and automatically converting them to WebP format. Built with Tkinter, featuring thumbnail previews, drag-to-reorder, and everything in ONE file.

## 🎯 Key Features

✨ **WebP Conversion (Main Feature)**
- Automatically converts all images to WebP format
- High-quality compression with quality=85
- Reduces file sizes significantly
- Supports: JPG, JPEG, PNG, WEBP input formats
- All output files are .webp

🖼️ **Image Management**
- **Drag-to-reorder images** - rearrange by dragging
- **Thumbnail previews** - visual preview of each image
- Highlighted MAIN image with green badge
- Gallery images clearly labeled by position
- Add via file picker or drag-and-drop

🎨 **Smart Organization**
- First image = MAIN image (highlighted with ★ badge)
- Other images = GALLERY images (auto-numbered)
- Automatic folder creation with duplicate handling
- Image renaming based on prefix

⚙️ **Folder Management**
- Select custom output directory
- Auto-create product folders
- Handle duplicate folder names (Folder, Folder (1), Folder (2), etc.)

---

## 📋 System Requirements

- **Python 3.7+**
- **Pillow (PIL)** - for image processing and WebP conversion
  ```bash
  pip install Pillow
  ```

---

## ⚡ Quick Start

### Option 1: Run with Python

```bash
# Install Pillow if not already installed
pip install Pillow

# Run the application
python product_image_organizer.py
```

### Option 2: Build Standalone EXE

```bash
# Install PyInstaller
pip install pyinstaller

# Build the EXE
pyinstaller --onefile --noconsole product_image_organizer.py

# Run from dist/product_image_organizer.exe
```

---

## 📖 How to Use

### Step 1: Enter Product Name
Example: `iPhone 15 Pro`

### Step 2: Enter Image Prefix
Example: `iphone15pro` (no spaces, used for file naming)

### Step 3: Select Output Folder
Click **📂 Browse...** to choose where product folders will be created

### Step 4: Add Images
- Click **➕ Add Images** to select files (JPG, JPEG, PNG, WEBP)
- Or **drag and drop** images into the list
- Images appear with thumbnails

### Step 5: Reorder Images (Optional)
- **Drag images by the ☰ handle** to reorder
- First image becomes MAIN image ⭐
- Others become GALLERY images

### Step 6: Review & Convert
- Check that MAIN image shows green ★ badge
- Click **✅ Convert to WebP & Organize**
- Wait for conversion to complete
- Done! Success message shows created files

---

## 📁 Output Structure

**Input:**
- Product: `iPhone 15 Pro`
- Prefix: `iphone15pro`
- Images: `photo1.jpg`, `photo2.png`, `photo3.webp`

**Output (All WebP):**
```
iPhone 15 Pro/
├── iphone15pro_Main.webp          ← 1st image (converted)
├── iphone15pro_Gallery01.webp     ← 2nd image (converted)
└── iphone15pro_Gallery02.webp     ← 3rd image (converted)
```

**If folder exists, creates:**
```
iPhone 15 Pro (1)/
iPhone 15 Pro (2)/
```

---

## 🎨 UI Sections

### 1. 📦 Product Information
- **Product Name** - Name of the product folder
- **Image Prefix** - Prefix used for image files

### 2. 📁 Output Folder
- Choose where to create product folders
- Click **Browse...** to select directory

### 3. 🖼️ Image Manager & WebP Converter
- **Thumbnail previews** - see each image
- **File info** - filename and full path
- **Status badges** - MAIN image (green) or Gallery number
- **Drag reorder** - change image order
- **Remove button** - delete individual images
- **Conversion notice** - "All will convert to WebP with quality=85"

### 4. Action Buttons
- **🔄 Reset** - clear all fields and images
- **❌ Clear Images** - remove all images only
- **✅ Convert to WebP & Organize** - convert and organize images

---

## 🚀 WebP Conversion Details

### What is WebP?

**WebP** is a modern image format that provides:
- ✅ Smaller file sizes than JPG/PNG (25-35% smaller)
- ✅ Better quality at lower file sizes
- ✅ Supports transparency (like PNG)
- ✅ Widely supported (browsers, apps, devices)

### Conversion Process

1. **Input Images**
   - Accepts: JPG, JPEG, PNG, WEBP formats
   - Any size or color mode

2. **Conversion Steps**
   - Opens image with Pillow
   - Converts to RGB (handles PNG transparency)
   - Applies WebP compression with quality=85
   - Saves with .webp extension

3. **Quality Settings**
   - Quality: 85 (high quality, good compression)
   - Method: 6 (slowest, best compression)
   - Perfect balance of quality and file size

### File Size Comparison

Example with iPhone images:
```
Original: photo1.jpg (2.5 MB)
Converted: iphone15pro_Main.webp (800 KB) - 68% smaller

Original: photo2.png (3.2 MB)
Converted: iphone15pro_Gallery01.webp (900 KB) - 72% smaller
```

---

## 🌐 Browser/App Support for WebP

| Platform | Support |
|----------|---------|
| Chrome | ✅ Full support |
| Firefox | ✅ Full support (57+) |
| Safari | ✅ Full support (16+) |
| Edge | ✅ Full support |
| Mobile Apps | ✅ Most support |
| Legacy Browsers | ⚠️ May not support |

---

## 🛠️ Advanced Features

### Thumbnail Caching
Thumbnails are cached for faster performance when viewing the same images multiple times.

### Drag-to-Reorder
Grab the ☰ handle and drag images up or down to change their order. First image automatically becomes MAIN.

### Background Processing
Image processing runs in a separate thread, so the UI never freezes.

### Input Validation
- Product name required
- Prefix required
- At least one image required
- Friendly error messages

### PNG Transparency Handling
- PNG images with alpha channel are converted to RGB
- White background automatically applied where transparent

---

## 📦 Single File Architecture

Everything is contained in **product_image_organizer.py**:
- ✅ Complete Tkinter UI
- ✅ Image preview with PIL/Pillow
- ✅ WebP conversion with Pillow
- ✅ Drag-to-reorder logic
- ✅ File operations
- ✅ Error handling
- ✅ Threading for background processing

**~600 lines of clean, well-commented code**

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named 'PIL'" | Install Pillow: `pip install Pillow` |
| Conversion is slow | Normal for large images; patience required |
| WebP file looks different | PNG transparency converted to white background |
| Placeholder image instead of thumbnail | Image file may be corrupted; try another image |
| UI looks blurry on Windows | This is normal DPI scaling; will work fine |
| EXE is 100+ MB | Normal - includes Python runtime; can't be reduced much |
| Permissions error when creating folder | Choose different output directory |

---

## 📝 Code Overview

### Main Class: `ProductImageOrganizer`

**UI Methods:**
- `setup_styles()` - Configure theme
- `create_product_section()` - Top section
- `create_output_section()` - Output folder selector
- `create_image_manager_section()` - Image list with thumbnails
- `create_action_panel()` - Action buttons

**Image Methods:**
- `add_images()` - File picker
- `get_thumbnail()` - Generate thumbnail
- `update_image_display()` - Render image list
- `create_image_item()` - Individual image widget

**WebP Conversion (Key Methods):**
- `rename_and_copy_images()` - Convert to WebP and save
  - Opens image with PIL
  - Converts to RGB (handles transparency)
  - Saves as WebP with quality=85
  - Uses zero-padded numbering

**Processing Methods:**
- `validate_input()` - Check inputs
- `create_product_folder()` - Create with duplicate handling
- `process_images()` - Main workflow
- `_process_images_thread()` - Background processing

---

## 🎓 Learning Resources

The code includes detailed comments explaining:
- Class structure and methods
- UI layout and components
- Image handling with Pillow
- WebP conversion techniques
- Drag-to-reorder implementation
- Threading for responsive UI
- Error handling and validation

Perfect for learning Tkinter and image processing!

---

## 📄 License

Free to use and modify for personal or commercial purposes.

---

**Version:** 2.1 (WebP Edition)  
**Created:** March 2026  
**Language:** Python 3.7+  
**Dependencies:** Tkinter (built-in), Pillow (pip install Pillow)

## 🎯 Key Features

✨ **Modern User Interface**
- Clean, sectioned layout (Product Info, Image Manager, Action Panel)
- Thumbnail previews with file information
- Responsive design with scrollable image list

🖼️ **Image Management**
- **Drag-to-reorder images** - rearrange by dragging
- **Thumbnail previews** - visual preview of each image
- Highlighted MAIN image with green badge
- Gallery images clearly labeled by position
- Add via file picker or drag-and-drop

🎨 **Smart Organization**
- First image = MAIN image (highlighted with ★ badge)
- Other images = GALLERY images (auto-numbered)
- Automatic folder creation with duplicate handling
- Image renaming based on prefix

⚙️ **Folder Management**
- Select custom output directory
- Auto-create product folders
- Handle duplicate folder names (Folder, Folder (1), Folder (2), etc.)

🔧 **Supported Formats**
- JPG, JPEG, PNG, WEBP

---

## 📋 System Requirements

- **Python 3.7+**
- **Pillow (PIL)** - for thumbnail generation
  ```bash
  pip install Pillow
  ```

---

## ⚡ Quick Start

### Option 1: Run with Python

```bash
# Install Pillow if not already installed
pip install Pillow

# Run the application
python product_image_organizer.py
```

### Option 2: Build Standalone EXE

```bash
# Install PyInstaller
pip install pyinstaller

# Build the EXE
pyinstaller --onefile --noconsole product_image_organizer.py

# Run from dist/product_image_organizer.exe
```

---

## 📖 How to Use

### Step 1: Enter Product Name
Example: `iPhone 15 Pro`

### Step 2: Enter Image Prefix
Example: `iphone15pro` (no spaces, used for file naming)

### Step 3: Select Output Folder
Click **📂 Browse...** to choose where product folders will be created

### Step 4: Add Images
- Click **➕ Add Images** to select files
- Or **drag and drop** images into the list
- Images appear with thumbnails

### Step 5: Reorder Images (Optional)
- **Drag images by the ☰ handle** to reorder
- First image becomes MAIN image ⭐
- Others become GALLERY images

### Step 6: Review & Process
- Check that MAIN image shows green ★ badge
- Click **✅ Generate Folder & Process**
- Done! Success message shows created files

---

## 📁 Output Structure

**Input:**
- Product: `iPhone 15 Pro`
- Prefix: `iphone15pro`
- Images: `photo1.jpg`, `photo2.jpg`, `photo3.jpg`

**Output:**
```
iPhone 15 Pro/
├── iphone15pro_Main.jpg          ← 1st image (MAIN)
├── iphone15pro_Gallery01.jpg     ← 2nd image
└── iphone15pro_Gallery02.jpg     ← 3rd image
```

**If folder exists, creates:**
```
iPhone 15 Pro (1)/
iPhone 15 Pro (2)/
```

---

## 🎮 UI Sections

### 1. 📦 Product Information
- **Product Name** - Name of the product folder
- **Image Prefix** - Prefix used for image files

### 2. 📁 Output Folder
- Choose where to create product folders
- Click **Browse...** to select directory

### 3. 🖼️ Image Manager
- **Thumbnail previews** - see each image
- **File info** - filename and full path
- **Status badges** - MAIN image (green) or Gallery number
- **Drag reorder** - change image order
- **Remove button** - delete individual images

### 4. Action Buttons
- **🔄 Reset** - clear all fields and images
- **❌ Clear Images** - remove all images only
- **✅ Generate Folder & Process** - create folder and process images

---

## 🚀 Advanced Features

### Thumbnail Caching
Thumbnails are cached for faster performance when viewing the same images multiple times.

### Drag-to-Reorder
Grab the ☰ handle and drag images up or down to change their order. First image automatically becomes MAIN.

### Background Processing
Image processing runs in a separate thread, so the UI never freezes.

### Input Validation
- Product name required
- Prefix required
- At least one image required
- Friendly error messages

---

## 🛠️ Building Executable

### For Windows Users

```bash
# Install required packages
pip install PyInstaller Pillow

# Create single EXE file
pyinstaller --onefile --noconsole product_image_organizer.py

# Result: dist/product_image_organizer.exe
```

### For macOS Users

```bash
pyinstaller --onefile --windowed product_image_organizer.py
# Result: dist/product_image_organizer.app
```

### For Linux Users

```bash
pyinstaller --onefile product_image_organizer.py
# Result: dist/product_image_organizer
```

### With Custom Icon (Windows)

```bash
pyinstaller --onefile --noconsole --icon=icon.ico product_image_organizer.py
```

---

## 📦 Single File Architecture

Everything is contained in **product_image_organizer.py**:
- ✅ Complete Tkinter UI
- ✅ Image preview with PIL/Pillow
- ✅ Drag-to-reorder logic
- ✅ File operations
- ✅ Error handling
- ✅ Threading for background processing

**~550 lines of clean, well-commented code**

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named 'PIL'" | Install Pillow: `pip install Pillow` |
| Placeholder image instead of thumbnail | Image file may be corrupted; try another image |
| Drag-reorder not working smoothly | Reduce number of images or restart app |
| UI looks blurry on Windows | This is normal DPI scaling; will work fine |
| EXE is 100+ MB | Normal - includes Python runtime; can't be reduced much |
| Permissions error when creating folder | Choose different output directory |

---

## 📝 Code Overview

### Main Class: `ProductImageOrganizer`

**UI Methods:**
- `setup_styles()` - Configure theme
- `create_product_section()` - Top section
- `create_output_section()` - Output folder selector
- `create_image_manager_section()` - Image list with thumbnails
- `create_action_panel()` - Action buttons

**Image Methods:**
- `add_images()` - File picker
- `get_thumbnail()` - Generate thumbnail
- `update_image_display()` - Render image list
- `create_image_item()` - Individual image widget

**Reorder Methods:**
- `start_drag()` - Begin dragging
- `on_drag()` - Drag in progress
- `end_drag()` - Drop and reorder

**Processing Methods:**
- `validate_input()` - Check inputs
- `create_product_folder()` - Create with duplicate handling
- `rename_and_copy_images()` - Process images
- `_process_images_thread()` - Background processing

---

## 🎓 Learning Resources

The code includes detailed comments explaining:
- Class structure and methods
- UI layout and components
- Image handling with Pillow
- Drag-to-reorder implementation
- Threading for responsive UI
- Error handling and validation

Perfect for learning Tkinter development!

---

## 📄 License

Free to use and modify for personal or commercial purposes.

---

**Version:** 2.0 (Advanced Edition)  
**Created:** March 2026  
**Language:** Python 3.7+  
**Dependencies:** Tkinter (built-in), Pillow (pip install Pillow)

