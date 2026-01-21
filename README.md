# Aurora-Cloud-BG-remover
Aurora Cloud BG Remover is a professional desktop application built with Python and Tkinter that uses advanced deep-learning models to remove image backgrounds with high precision. It features a modern UI, batch processing, multiple AI models, and a fully responsive layout that adapts correctly to window resize, minimize, and maximize actions.

☁️ Aurora Cloud BG Remover

Aurora Cloud BG Remover is a professional, AI-powered desktop application for high-quality image background removal. Built using Python and Tkinter, it runs fully offline and leverages deep-learning models via `rembg` to deliver accurate, fast, and privacy-friendly results.

This version includes a **fixed and responsive UI layout**, ensuring stable alignment during window resize, minimize, and maximize operations.

---

## ✨ Features

🧠 AI Background Removal
- Powered by `rembg` (U²-Net based models)
- Multiple model options:
  - **u2net** – Ultra accurate (recommended)
  - **u2netp** – Fast and lightweight
  - **silueta** – Optimized for human subjects

🖥️ Modern Desktop UI
- Premium gradient background with particle effects
- Glass-morphism inspired panels
- Custom animated buttons
- Side-by-side image preview (Original vs Processed)

📐 Responsive & Stable Layout
- Fixed alignment issues on resize
- Works smoothly on maximize / minimize
- DPI-aware on Windows systems
- Minimum window size enforced to prevent UI breakage

⚡ Quality & Enhancement Controls
- Quality modes: **Standard / High / Ultra**
- Alpha matting for clean edges
- Optional edge enhancement
- Auto-crop to detected subject

📦 Batch Processing
- Process multiple images in one run
- Automatic output naming
- Progress tracking and status updates

### 💾 Export Options
- Supported formats:
  - PNG
  - JPG / JPEG
  - WEBP
  - BMP
  - TIFF
- Smart handling of transparency when exporting to JPEG

🚀 Performance
- GPU acceleration supported (`rembg[gpu]`)
- Runs completely offline
- No API calls, no uploads, no data sharing

🔧 Auto Dependency Installation
- Automatically installs required Python packages on first run


🛠️ Tech Stack

- Language:Python 3
- UI Framework:Tkinter
- AI / ML:rembg (U²-Net)
- Image Processing:Pillow, NumPy
- Threading:Python threading (non-blocking UI)

