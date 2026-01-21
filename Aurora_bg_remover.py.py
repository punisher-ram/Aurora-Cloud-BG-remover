"""
Aurora Cloud BG Remover - Professional Background Removal Tool
By hash&ke

Fixed alignment version: Responsive to Maximize/Minimize.
Auto-installs all requirements automatically.
"""

import subprocess
import sys
import os
import io
import threading
import random
from pathlib import Path
from datetime import datetime

# Auto-install required packages
def install_requirements():
    packages = ['rembg[gpu]', 'pillow', 'numpy']
    print("🔧 Installing required packages (this may take a moment)...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
        except:
            pass
    print("✅ Packages installed!\n")

# Try to import, install if needed
try:
    from rembg import remove, new_session
    from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
    import tkinter as tk
    from tkinter import filedialog, ttk, messagebox
    import numpy as np
except ImportError:
    install_requirements()
    from rembg import remove, new_session
    from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
    import tkinter as tk
    from tkinter import filedialog, ttk, messagebox
    import numpy as np


class ModernButton(tk.Canvas):
    """Custom modern button with smooth animations"""
    def __init__(self, parent, text, command, bg_color, hover_color, text_color, 
                 width=200, height=50, icon="", **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], 
                        highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.icon = icon
        self.enabled = True
        self.is_hovered = False
        
        self.draw_button(bg_color)
        self.bind('<Enter>', lambda e: self.on_hover() if self.enabled else None)
        self.bind('<Leave>', lambda e: self.on_leave() if self.enabled else None)
        self.bind('<Button-1>', lambda e: self.on_click() if self.enabled else None)
        
    def draw_button(self, color):
        self.delete('all')
        if self.is_hovered and self.enabled:
            self.create_rounded_rect(2, 2, self.winfo_reqwidth()-2, 
                                    self.winfo_reqheight()-2, 
                                    radius=28, fill=color, outline=color, width=3)
        else:
            self.create_rounded_rect(5, 5, self.winfo_reqwidth()-5, 
                                    self.winfo_reqheight()-5, 
                                    radius=25, fill=color, outline='')
        
        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2, 
                        text=display_text, fill=self.text_color, 
                        font=('Segoe UI', 11, 'bold'))
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                 x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                 x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def on_hover(self):
        self.is_hovered = True
        self.draw_button(self.hover_color)
        self.config(cursor='hand2')
        
    def on_leave(self):
        self.is_hovered = False
        self.draw_button(self.bg_color)
        self.config(cursor='')
        
    def on_click(self):
        if self.enabled and self.command:
            self.after(50, lambda: self.draw_button(self.bg_color))
            self.command()
            
    def set_state(self, enabled):
        self.enabled = enabled
        if enabled:
            self.draw_button(self.bg_color)
        else:
            self.draw_button('#2a2a3e')
            self.config(cursor='')


class AuroraCloudBGRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("☁️ Aurora Cloud BG Remover")
        self.root.geometry("1300x800")
        
        # Set minimum size to prevent layout breakage on minimize
        self.root.minsize(1100, 750)
        
        # Beautiful gradient colors
        self.bg_start = "#0a0015"
        self.bg_end = "#1a0033"
        self.root.configure(bg=self.bg_start)
        
        self.input_path = None
        self.output_path = None
        self.selected_format = tk.StringVar(value="png")
        self.selected_model = tk.StringVar(value="u2net")
        self.original_image = None
        self.processed_image = None
        self.session = None
        self.processing_time = 0
        
        # Enhancement options
        self.enhance_edges = tk.BooleanVar(value=True)
        self.auto_crop = tk.BooleanVar(value=False)
        self.quality_level = tk.StringVar(value="Ultra")
        
        # Statistics
        self.images_processed = 0
        self.current_model = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Animated gradient background
        canvas = tk.Canvas(self.root, width=1300, height=800, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Create stunning gradient (Increased range for maximized windows)
        for i in range(2500): # Increased from 800 to cover 4K screens
            ratio = min(i / 1500, 1) # Smoother gradient spread
            r = int(10 + (30 - 10) * ratio)
            g = int(0 + (0 - 0) * ratio)
            b = int(21 + (70 - 21) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, 3840, i, fill=color) # Extended width
            
        # Add subtle stars/particles effect
        for _ in range(120):
            x = random.randint(0, 1920) # Increased range
            y = random.randint(0, 1080)
            size = random.randint(1, 3)
            opacity = random.choice(['#ffffff', '#aaaaff', '#ffaaff'])
            canvas.create_oval(x, y, x+size, y+size, fill=opacity, outline='')
        
        # --- FIXED ALIGNMENT SECTION ---
        # Main container using relative sizing for responsiveness
        main_container = tk.Frame(self.root, bg='#1a0033', highlightthickness=0)
        
        # Outer glow effect - Adjusted for relative scaling
        for i in range(3):
            glow = tk.Frame(self.root, bg=f'#330066')
            # Place glow slightly behind main container with relative sizing
            glow.place(relx=0.5, rely=0.5, anchor='center', 
                      relwidth=0.92 + (i*0.005), relheight=0.92 + (i*0.005))
            glow.lower()
        
        # Place main container with relative width/height (responsive)
        main_container.place(relx=0.5, rely=0.5, anchor='center', 
                           relwidth=0.92, relheight=0.92)
        main_container.lift()
        
        # ===== HEADER SECTION =====
        header_frame = tk.Frame(main_container, bg='#1a0033')
        header_frame.pack(pady=20, fill='x')
        
        # Logo/Title
        title_canvas = tk.Canvas(header_frame, width=700, height=90, 
                                bg='#1a0033', highlightthickness=0)
        title_canvas.pack()
        
        title_canvas.create_text(350, 28, text="☁️ AURORA CLOUD", 
                                font=("Segoe UI", 36, "bold"),
                                fill="#00ffff", anchor="center")
        title_canvas.create_text(350, 58, text="BG REMOVER", 
                                font=("Segoe UI", 32, "bold"),
                                fill="#ff00ff", anchor="center")
        
        credit = tk.Label(header_frame, text="by hash&ke",
                         font=("Segoe UI", 9, "italic"),
                         bg='#1a0033', fg='#6666aa')
        credit.pack(pady=3)
        
        tagline = tk.Label(header_frame, 
                          text="✨ Professional AI Background Removal • Ultra Accurate • Lightning Fast ✨",
                          font=("Segoe UI", 11),
                          bg='#1a0033', fg='#9999ff')
        tagline.pack(pady=5)
        
        # ===== PREVIEW SECTION (Responsive) =====
        preview_container = tk.Frame(main_container, bg='#1a0033')
        preview_container.pack(pady=10, padx=40, fill='both', expand=True)
        
        # Original Image Panel
        original_panel = tk.Frame(preview_container, bg='#2a1a4a', 
                                 highlightthickness=3, highlightbackground='#00ffff')
        original_panel.pack(side='left', fill='both', expand=True, padx=8)
        
        original_header = tk.Frame(original_panel, bg='#1a0a2a', height=40)
        original_header.pack(fill='x')
        original_header.pack_propagate(False)
        
        tk.Label(original_header, text="📸 ORIGINAL IMAGE", 
                font=('Segoe UI', 12, 'bold'),
                bg='#1a0a2a', fg='#00ffff').pack(pady=10)
        
        self.original_canvas = tk.Label(original_panel, bg='#0a0015',
                                       text="🖼️\n\nNo image loaded\n\nClick 'Upload Image' below",
                                       font=('Segoe UI', 13),
                                       fg='#666688')
        self.original_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.original_info = tk.Label(original_panel, text="",
                                     font=('Segoe UI', 9),
                                     bg='#2a1a4a', fg='#8888aa')
        self.original_info.pack(pady=5)
        
        # Processed Image Panel
        processed_panel = tk.Frame(preview_container, bg='#2a1a4a',
                                  highlightthickness=3, highlightbackground='#ff00ff')
        processed_panel.pack(side='right', fill='both', expand=True, padx=8)
        
        processed_header = tk.Frame(processed_panel, bg='#1a0a2a', height=40)
        processed_header.pack(fill='x')
        processed_header.pack_propagate(False)
        
        tk.Label(processed_header, text="✨ BACKGROUND REMOVED", 
                font=('Segoe UI', 12, 'bold'),
                bg='#1a0a2a', fg='#ff00ff').pack(pady=10)
        
        self.processed_canvas = tk.Label(processed_panel, bg='#0a0015',
                                        text="⚡\n\nProcessed image\nwill appear here",
                                        font=('Segoe UI', 13),
                                        fg='#666688')
        self.processed_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.processed_info = tk.Label(processed_panel, text="",
                                      font=('Segoe UI', 9),
                                      bg='#2a1a4a', fg='#8888aa')
        self.processed_info.pack(pady=5)
        
        # ===== CONTROLS SECTION =====
        controls_container = tk.Frame(main_container, bg='#2a1a4a',
                                     highlightthickness=2, highlightbackground='#6600ff')
        controls_container.pack(pady=12, padx=40, fill='x')
        
        # Settings Row - Centered
        settings_frame = tk.Frame(controls_container, bg='#2a1a4a')
        settings_frame.pack(pady=15, padx=20, fill='x')
        
        # Inner frame to hold settings centered
        settings_inner = tk.Frame(settings_frame, bg='#2a1a4a')
        settings_inner.pack(anchor='center')
        
        # AI Model Selection
        model_container = tk.Frame(settings_inner, bg='#1a0a2a', 
                                  highlightthickness=1, highlightbackground='#6600ff')
        model_container.pack(side='left', padx=10, pady=5)
        
        tk.Label(model_container, text="🤖 AI Model:", 
                font=('Segoe UI', 10, 'bold'),
                bg='#1a0a2a', fg='#00ffff').pack(side='left', padx=8, pady=8)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.TCombobox', 
                       fieldbackground='#0a0015',
                       background='#6600ff',
                       foreground='#ffffff',
                       arrowcolor='#00ffff',
                       borderwidth=0)
        
        models = [
            "u2net - Ultra Accurate (Recommended)",
            "u2netp - Fast & Efficient",
            "silueta - Optimized for People"
        ]
        
        self.model_combo = ttk.Combobox(model_container, 
                                       textvariable=self.selected_model,
                                       values=models, state='readonly',
                                       width=32, font=('Segoe UI', 9),
                                       style='Custom.TCombobox')
        self.model_combo.set(models[0])
        self.model_combo.pack(side='left', padx=8, pady=8)
        
        # Format Selection
        format_container = tk.Frame(settings_inner, bg='#1a0a2a',
                                   highlightthickness=1, highlightbackground='#6600ff')
        format_container.pack(side='left', padx=10, pady=5)
        
        tk.Label(format_container, text="💾 Format:", 
                font=('Segoe UI', 10, 'bold'),
                bg='#1a0a2a', fg='#ff00ff').pack(side='left', padx=8, pady=8)
        
        format_combo = ttk.Combobox(format_container,
                                   textvariable=self.selected_format,
                                   values=["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
                                   state='readonly', width=12,
                                   font=('Segoe UI', 9),
                                   style='Custom.TCombobox')
        format_combo.pack(side='left', padx=8, pady=8)
        
        # Quality Selection
        quality_container = tk.Frame(settings_inner, bg='#1a0a2a',
                                    highlightthickness=1, highlightbackground='#6600ff')
        quality_container.pack(side='left', padx=10, pady=5)
        
        tk.Label(quality_container, text="⚡ Quality:", 
                font=('Segoe UI', 10, 'bold'),
                bg='#1a0a2a', fg='#00ff88').pack(side='left', padx=8, pady=8)
        
        quality_combo = ttk.Combobox(quality_container,
                                    textvariable=self.quality_level,
                                    values=["Standard", "High", "Ultra"],
                                    state='readonly', width=10,
                                    font=('Segoe UI', 9),
                                    style='Custom.TCombobox')
        quality_combo.set("Ultra")
        quality_combo.pack(side='left', padx=8, pady=8)
        
        # Enhancement Options
        enhance_container = tk.Frame(settings_inner, bg='#1a0a2a',
                                    highlightthickness=1, highlightbackground='#6600ff')
        enhance_container.pack(side='left', padx=10, pady=5)
        
        tk.Label(enhance_container, text="🎨 Options:", 
                font=('Segoe UI', 10, 'bold'),
                bg='#1a0a2a', fg='#ffaa00').pack(side='left', padx=8, pady=8)
        
        enhance_check = tk.Checkbutton(enhance_container, text="Edge Enhancement",
                                      variable=self.enhance_edges,
                                      font=('Segoe UI', 9),
                                      bg='#1a0a2a', fg='#ffffff',
                                      selectcolor='#0a0015',
                                      activebackground='#1a0a2a',
                                      activeforeground='#00ff88')
        enhance_check.pack(side='left', padx=5)
        
        crop_check = tk.Checkbutton(enhance_container, text="Auto-Crop",
                                   variable=self.auto_crop,
                                   font=('Segoe UI', 9),
                                   bg='#1a0a2a', fg='#ffffff',
                                   selectcolor='#0a0015',
                                   activebackground='#1a0a2a',
                                   activeforeground='#00ff88')
        crop_check.pack(side='left', padx=5)
        
        # Action Buttons Row
        buttons_frame = tk.Frame(controls_container, bg='#2a1a4a')
        buttons_frame.pack(pady=15)
        
        # Upload Button
        self.upload_btn = ModernButton(buttons_frame, "UPLOAD IMAGE", 
                                      self.select_file,
                                      '#00ffff', '#00dddd', '#000000',
                                      width=200, height=50, icon="📁")
        self.upload_btn.pack(side='left', padx=8)
        
        # Process Button
        self.process_btn = ModernButton(buttons_frame, "REMOVE BG",
                                       self.process_image,
                                       '#ff00ff', '#dd00dd', '#ffffff',
                                       width=220, height=50, icon="⚡")
        self.process_btn.set_state(False)
        self.process_btn.pack(side='left', padx=8)
        
        # Batch Process Button
        self.batch_btn = ModernButton(buttons_frame, "BATCH MODE",
                                     self.batch_process,
                                     '#9900ff', '#7700dd', '#ffffff',
                                     width=200, height=50, icon="📦")
        self.batch_btn.pack(side='left', padx=8)
        
        # Download Button
        self.download_btn = ModernButton(buttons_frame, "DOWNLOAD",
                                        self.download_image,
                                        '#00ff88', '#00dd77', '#000000',
                                        width=180, height=50, icon="⬇️")
        self.download_btn.set_state(False)
        self.download_btn.pack(side='left', padx=8)
        
        # ===== STATUS BAR =====
        status_container = tk.Frame(main_container, bg='#1a0033')
        status_container.pack(pady=10, fill='x', padx=40)
        
        self.status_label = tk.Label(status_container, 
                                     text="💡 Ready to process images • Select an image to get started",
                                     font=('Segoe UI', 11, 'bold'),
                                     bg='#1a0033', fg='#9999ff')
        self.status_label.pack()
        
        # Progress bar
        style.configure('Aurora.Horizontal.TProgressbar',
                       background='#ff00ff',
                       troughcolor='#1a0a2a',
                       borderwidth=0,
                       thickness=12)
        
        self.progress = ttk.Progressbar(status_container,
                                       mode='indeterminate',
                                       length=700,
                                       style='Aurora.Horizontal.TProgressbar')
        
        # Stats display
        stats_frame = tk.Frame(status_container, bg='#1a0033')
        stats_frame.pack(pady=5)
        
        self.stats_label = tk.Label(stats_frame,
                                    text="📊 Images Processed: 0 | ⚡ Last Process Time: --",
                                    font=('Segoe UI', 9),
                                    bg='#1a0033', fg='#6666aa')
        self.stats_label.pack()
        
        # ===== FOOTER =====
        footer_frame = tk.Frame(self.root, bg=self.bg_start)
        footer_frame.pack(side='bottom', pady=10)
        
        tk.Label(footer_frame,
                text="🌟 Premium Quality • Lightning Fast Processing • Professional AI Results 🌟",
                font=('Segoe UI', 10, 'bold'),
                bg=self.bg_start, fg='#6666aa').pack()
        
        tk.Label(footer_frame,
                text="Powered by Hash&ke AI",
                font=('Segoe UI', 8),
                bg=self.bg_start, fg='#444466').pack()
        
    def create_checkered_bg(self, width, height):
        """Create checkered background for transparency"""
        img = Image.new('RGB', (width, height), '#0a0015')
        draw = ImageDraw.Draw(img)
        square_size = 15
        
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                if (x // square_size + y // square_size) % 2 == 0:
                    draw.rectangle([x, y, x + square_size, y + square_size],
                                 fill='#1a0a2a')
        return img
        
    def resize_image_for_preview(self, image, max_width=520, max_height=300):
        """Resize maintaining aspect ratio"""
        ratio = min(max_width / image.width, max_height / image.height)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
    def select_file(self):
        filetypes = (
            ("All Images", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Select an image - Aurora Cloud BG Remover",
            filetypes=filetypes
        )
        
        if filename:
            self.input_path = filename
            
            try:
                self.original_image = Image.open(filename)
                preview = self.resize_image_for_preview(self.original_image)
                photo = ImageTk.PhotoImage(preview)
                
                self.original_canvas.configure(image=photo, text='')
                self.original_canvas.image = photo
                
                # Show image info
                size_mb = os.path.getsize(filename) / (1024 * 1024)
                info_text = f"{self.original_image.width}x{self.original_image.height} • {size_mb:.2f}MB • {self.original_image.mode}"
                self.original_info.config(text=info_text)
                
                self.status_label.config(text=f"✅ Loaded: {Path(filename).name} • Ready to process!", 
                                       fg='#00ff88')
                self.process_btn.set_state(True)
                self.download_btn.set_state(False)
                
                # Clear processed preview
                self.processed_canvas.configure(image='', 
                                              text="⚡\n\nProcessed image\nwill appear here",
                                              fg='#666688')
                self.processed_info.config(text="")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image:\n{str(e)}")
                
    def process_image(self):
        if not self.input_path:
            messagebox.showwarning("No File", "Please upload an image first!")
            return
        
        # Disable all buttons
        self.process_btn.set_state(False)
        self.upload_btn.set_state(False)
        self.batch_btn.set_state(False)
        
        self.status_label.config(text="🚀 Initializing Aurora Cloud AI Processing...", fg='#ffff00')
        self.progress.pack(pady=8)
        self.progress.start(8)
        self.root.update()
        
        # Process in thread
        thread = threading.Thread(target=self._process_thread)
        thread.start()
        
    def _process_thread(self):
        start_time = datetime.now()
        
        try:
            model_name = self.selected_model.get().split(' - ')[0]
            
            # Load AI model
            if self.session is None or model_name != self.current_model:
                self.status_label.config(text=f"🧠 Loading {model_name} AI Neural Network...", 
                                       fg='#ffff00')
                self.root.update()
                self.session = new_session(model_name)
                self.current_model = model_name
            
            # Read image
            with open(self.input_path, 'rb') as f:
                input_data = f.read()
            
            self.status_label.config(text="✨ AI Analyzing Image & Removing Background...",
                                   fg='#ffff00')
            self.root.update()
            
            # Quality settings based on selection
            quality = self.quality_level.get()
            if quality == "Ultra":
                alpha_settings = {
                    'alpha_matting': True,
                    'alpha_matting_foreground_threshold': 240,
                    'alpha_matting_background_threshold': 10,
                    'alpha_matting_erode_size': 10
                }
            elif quality == "High":
                alpha_settings = {
                    'alpha_matting': True,
                    'alpha_matting_foreground_threshold': 230,
                    'alpha_matting_background_threshold': 15,
                    'alpha_matting_erode_size': 8
                }
            else:
                alpha_settings = {'alpha_matting': False}
            
            # Remove background
            output_data = remove(input_data, session=self.session, **alpha_settings)
            
            self.processed_image = Image.open(io.BytesIO(output_data))
            
            # Apply enhancements
            if self.enhance_edges.get():
                self.status_label.config(text="🎨 Enhancing Edges for Professional Quality...",
                                       fg='#ffff00')
                self.root.update()
                self.processed_image = self.processed_image.filter(
                    ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
                )
            
            if self.auto_crop.get():
                self.status_label.config(text="✂️ Auto-Cropping to Content...",
                                       fg='#ffff00')
                self.root.update()
                self.processed_image = self.auto_crop_image(self.processed_image)
            
            # Create preview
            preview = self.resize_image_for_preview(self.processed_image)
            checkered = self.create_checkered_bg(preview.width, preview.height)
            checkered.paste(preview, (0, 0), preview if preview.mode == 'RGBA' else None)
            
            photo = ImageTk.PhotoImage(checkered)
            self.processed_canvas.configure(image=photo, text='')
            self.processed_canvas.image = photo
            
            # Show processed image info
            info_text = f"{self.processed_image.width}x{self.processed_image.height} • Transparent Background"
            self.processed_info.config(text=info_text)
            
            # Calculate processing time
            end_time = datetime.now()
            self.processing_time = (end_time - start_time).total_seconds()
            self.images_processed += 1
            
            self.status_label.config(
                text=f"✨ Success! Background Removed Perfectly in {self.processing_time:.2f}s",
                fg='#00ff88'
            )
            
            self.stats_label.config(
                text=f"📊 Images Processed: {self.images_processed} | ⚡ Last Process Time: {self.processing_time:.2f}s"
            )
            
            self.download_btn.set_state(True)
                
        except Exception as e:
            self.status_label.config(text=f"❌ Processing Error: {str(e)}", fg='#ff0000')
            messagebox.showerror("Processing Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.process_btn.set_state(True)
            self.upload_btn.set_state(True)
            self.batch_btn.set_state(True)
            
    def auto_crop_image(self, img):
        """Auto-crop to content"""
        if img.mode != 'RGBA':
            return img
        
        bbox = img.getbbox()
        if bbox:
            return img.crop(bbox)
        return img
        
    def download_image(self):
        if not self.processed_image:
            messagebox.showwarning("No Image", "Please process an image first!")
            return
        
        output_format = self.selected_format.get()
        default_name = f"{Path(self.input_path).stem}_aurora_no_bg.{output_format}"
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{output_format}",
            initialfile=default_name,
            filetypes=[
                (f"{output_format.upper()} files", f"*.{output_format}"),
                ("All files", "*.*")
            ]
        )
        
        if save_path:
            try:
                if output_format.lower() in ['jpg', 'jpeg']:
                    if self.processed_image.mode == 'RGBA':
                        rgb_img = Image.new('RGB', self.processed_image.size, (255, 255, 255))
                        rgb_img.paste(self.processed_image, 
                                    mask=self.processed_image.split()[3])
                        rgb_img.save(save_path, quality=100, optimize=True)
                    else:
                        self.processed_image.save(save_path, quality=100, optimize=True)
                else:
                    self.processed_image.save(save_path, optimize=True)
                
                self.status_label.config(
                    text=f"💾 Image Saved: {Path(save_path).name}",
                    fg='#00ff88'
                )
                
                messagebox.showinfo("Success!", 
                    f"✨ Image saved successfully!\n\n"
                    f"📁 Location:\n{save_path}\n\n"
                    f"⚡ Processing time: {self.processing_time:.2f}s")
                    
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save image:\n{str(e)}")

    def batch_process(self):
        """Batch process multiple images"""
        filetypes = (
            ("All Images", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif"),
            ("All files", "*.*")
        )
        
        filenames = filedialog.askopenfilenames(
            title="Select multiple images for batch processing",
            filetypes=filetypes
        )
        
        if not filenames:
            return
        
        output_dir = filedialog.askdirectory(
            title="Select output folder for processed images"
        )
        
        if not output_dir:
            return
        
        # Show batch processing dialog
        result = messagebox.askyesno(
            "Batch Processing",
            f"Process {len(filenames)} images?\n\n"
            f"Quality: {self.quality_level.get()}\n"
            f"Output folder: {output_dir}"
        )
        
        if not result:
            return
            
        # Disable inputs
        self.process_btn.set_state(False)
        self.upload_btn.set_state(False)
        self.batch_btn.set_state(False)
        self.download_btn.set_state(False)
        
        # Setup progress
        self.status_label.config(text=f"📦 Batch processing {len(filenames)} images...", fg='#ffff00')
        self.progress.pack(pady=8)
        self.progress.configure(mode='determinate', maximum=len(filenames))
        self.progress['value'] = 0
        self.root.update()
        
        # Run batch in thread
        thread = threading.Thread(target=self._batch_thread, args=(filenames, output_dir))
        thread.start()

    def _batch_thread(self, filenames, output_dir):
        """Handle background processing for multiple files"""
        successful = 0
        errors = 0
        
        model_name = self.selected_model.get().split(' - ')[0]
        
        # Quality settings
        quality = self.quality_level.get()
        if quality == "Ultra":
            alpha_settings = {'alpha_matting': True, 'alpha_matting_foreground_threshold': 240}
        elif quality == "High":
            alpha_settings = {'alpha_matting': True, 'alpha_matting_foreground_threshold': 230}
        else:
            alpha_settings = {'alpha_matting': False}
        
        try:
            # Initialize session if needed
            if self.session is None or model_name != self.current_model:
                self.session = new_session(model_name)
                self.current_model = model_name
            
            for i, file_path in enumerate(filenames):
                try:
                    # Update status
                    current_name = Path(file_path).name
                    self.root.after(0, lambda t=f"📦 Processing ({i+1}/{len(filenames)}): {current_name}": 
                                  self.status_label.config(text=t, fg='#ffff00'))
                    
                    # Read and process
                    with open(file_path, 'rb') as f:
                        input_data = f.read()
                        
                    output_data = remove(
                        input_data,
                        session=self.session,
                        **alpha_settings
                    )
                    
                    # Convert to PIL for saving logic
                    img = Image.open(io.BytesIO(output_data))
                    
                    # Apply auto-crop if selected
                    if self.auto_crop.get():
                        img = self.auto_crop_image(img)
                    
                    # Save file
                    stem = Path(file_path).stem
                    output_format = self.selected_format.get()
                    out_name = f"{stem}_aurora_no_bg.{output_format}"
                    save_path = os.path.join(output_dir, out_name)
                    
                    if output_format.lower() in ['jpg', 'jpeg']:
                        # Handle JPEG transparency
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.split()[3] if 'A' in img.getbands() else None)
                        rgb_img.save(save_path, quality=100)
                    else:
                        img.save(save_path)
                        
                    successful += 1
                    self.images_processed += 1
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    errors += 1
                
                # Update progress bar
                self.root.after(0, lambda v=i+1: self.progress.configure(value=v))
                
                # Update stats
                self.root.after(0, lambda c=self.images_processed: 
                              self.stats_label.config(text=f"📊 Images Processed: {c}"))
            
            # Final Status
            status_msg = f"✅ Batch Complete! Success: {successful}, Errors: {errors}"
            self.root.after(0, lambda: self.status_label.config(text=status_msg, fg='#00ff88'))
            self.root.after(0, lambda: messagebox.showinfo("Batch Complete", 
                f"✨ Processing finished!\n\n"
                f"✅ Successful: {successful}\n"
                f"❌ Failed: {errors}\n\n"
                f"📂 Output: {output_dir}"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Batch Error", str(e)))
            
        finally:
            # Reset UI
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.progress.pack_forget())
            self.root.after(0, lambda: self.process_btn.set_state(True))
            self.root.after(0, lambda: self.upload_btn.set_state(True))
            self.root.after(0, lambda: self.batch_btn.set_state(True))
            self.root.after(0, lambda: self.progress.configure(mode='indeterminate'))


if __name__ == "__main__":
    try:
        # Enable high DPI awareness for Windows
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    root = tk.Tk()
    app = AuroraCloudBGRemover(root)
    root.mainloop()