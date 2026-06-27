# Sagar Mehmood - Academic & Technical Profile

A beautifully designed, premium single-page portfolio highlighting the academic, professional, and technical profile of **Sagar Mehmood**, a final-year Computer Science student at FAST School of Computing and an aspiring AI researcher.

Built with performance and aesthetics in mind, this project adheres to modern web standards, featuring responsive layout systems, smooth micro-animations, and rich visual styling.

## 🎨 Visual & Technical Design Choices

- **Modern Tech Palette**: Deep, dark space backgrounds (`#060913`) paired with custom neon-glow accents (cyan for engineering, purple for AI/computation, and emerald for algorithms).
- **Glassmorphism**: Cards use translucent panels with `backdrop-filter: blur(16px)` and subtle, thin borders to create high-contrast depth and visual structure.
- **Ambient Lighting**: Animated radial gradient background glowing circles (`.bg-glow-1`, `.bg-glow-2`) float and scale in the background, making the page feel alive.
- **Micro-interactions & Animations**:
  - A subtle **pulsing online status indicator** (`.pulse-dot`) signaling availability.
  - A rotating **avatar ring** (`.avatar-ring`) providing visual interest.
  - Hover states on social links, experience grids, and language tags which slightly translate upwards, glow, or expand to invite engagement.
- **Responsive Layout**: Designed mobile-first using CSS Grid and Flexbox, converting the dual-column layout smoothly into a single-column stack on smaller screens.
- **SEO & Semantics**: Built with full semantic HTML tags (`<header>`, `<main>`, `<section>`, `<footer>`), valid title metadata, descriptive headers, and unique interactive item IDs.

---

## 📂 Project Architecture

The updated project directory structure is organized as follows:

```text
PMW-Day1/
├── index.html                  # Single-file webpage containing profile styles and markup
├── README.md                   # Documentation and project overview
└── 3d_reconstruction/          # 3D Reconstruction Module
    ├── reconstruct_3d.py       # Standalone Python script for depth estimation & PLY export
    ├── reconstruct_3d_notebook.ipynb # Step-by-step Jupyter Notebook walkthrough
    ├── notes.md                # Research comparisons, camera equations, and setup guide
    ├── input.jpg               # Input image (downloaded automatically)
    ├── output_depth.png        # Generated grayscale depth map
    ├── output_comparison.png   # Combined side-by-side visualization
    └── output_pointcloud.ply   # Resulting dense colorized 3D point cloud (1.8M+ points)
```

---

## 🌀 3D Reconstruction Research & Pipeline

As part of the PMW-Day1 evaluation, we researched practical 3D reconstruction methods and implemented a complete pipeline to generate a 3D point cloud from a single image using **Depth Anything V2**.

- **Researched Methods**: Compares Structure from Motion (SfM), Multi-View Stereo (MVS), NeRF, 3D Gaussian Splatting, and Monocular Depth estimation. Detailed comparison notes can be found in the [3D Reconstruction Notes](file:///d:/VS_Code_Projects/PMW-Day1/3d_reconstruction/notes.md).
- **Backprojection Geometry**: Uses inverse camera projection equations (pinhole camera model) to map pixel coords $(u, v)$ and depth $Z$ to 3D coordinates $(X, Y, Z)$ in camera space.
- **Inference & Execution**: The script operates on GPU (via CUDA) if available, generating a high-density, color-mapped `.ply` model representing the visual scene.

To run the pipeline or view the notebook, navigate to the `3d_reconstruction/` folder and check the setup guide in [notes.md](file:///d:/VS_Code_Projects/PMW-Day1/3d_reconstruction/notes.md).

---


### Profile Content Breakdown

1. **Identity & Philosophy**
   - **Name**: Sagar Mehmood (Final-year CS student, FAST School of Computing)
   - **Mindset**: Investigative, deep-dive engineer interested in the "why," "when," and "how" of technical designs.
   - **Core Ambition**: Aspiring world-class AI researcher working on architectural and hardware efficiency.
2. **Technical Expertise**
   - **Systems & AI Optimization**: CUDA, OpenCL, GPU Kernel optimization, Parallel systems, and HBM memory bandwidth efficiency.
   - **Web Development**: MERN Stack, React, Next.js (App Router), Tailwind CSS, Framer Motion, and Server/Client execution boundaries.
   - **Competitive Programming**: Algorithmic speed implementation on HackerRank using C++ & Python (Binary Lifting for LCA, complex heap management, and data mapping).