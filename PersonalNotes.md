# Sagar Mehmood - PMW-Day1 Submission & Personal Notes

This document details my implementation process, environment configuration, research notes, and reflections for the **PMW-Day1** 3D reconstruction assignment.

---

## 👤 GitHub & Student Identity
- **Student Name**: Sagar Mehmood
- **Academic Profile**: Final-year Computer Science Student, FAST School of Computing
- **GitHub Username**: [IoRagas](https://github.com/IoRagas)
- **Repository Link**: [PMW-Day1](https://github.com/IoRagas/PMW-Day1)

---

## 💻 Environment Readiness
My local development workspace is fully configured and ready:
- **Python**: Version `3.12.10` (installed on Windows)
- **Git**: Installed and configured for local version tracking
- **gh CLI**: Installed for command-line GitHub interactions and PR submissions
- **Editor**: VS Code (workspace directory: `d:\VS_Code_Projects\PMW-Day1`)
- **AI Coding Assistant**: Pair programmed with Antigravity (powered by Gemini) for rapid pipeline setup and geometric mathematics verification.
- **Hardware Acceleration**: PyTorch configured with **CUDA 12.8 (GPU)** for fast depth model inference.

---

## 📈 Tutorial-to-Code Links & Learning Sources
I studied several technical resources and documentation pages to implement this pipeline:
1. **Hugging Face Transformers - Monocular Depth Estimation**:
   - [HF Depth Estimation Pipeline](https://huggingface.co/docs/transformers/main/en/tasks/monocular_depth_estimation)
   - *Applied Learning*: Used this tutorial to load the `depth-anything/Depth-Anything-V2-Small-hf` model using the pipelines API, enabling rapid relative depth estimation.
2. **PyTorch Hub - Depth Models**:
   - [PyTorch Hub MiDaS Demo](https://pytorch.org/hub/intelisl_midas_v2/)
   - *Applied Learning*: Utilized PyTorch's test image repositories for stable, unauthenticated input assets (`dog.jpg`).
3. **Pinhole Camera Model & Intrinsic Calibration**:
   - [OpenCV Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
   - [Scratchapixel - Pinhole Camera Model](https://www.scratchapixel.com/lessons/3d-basic-rendering/3d-viewing-pinhole-camera)
   - *Applied Learning*: Applied the geometric backprojection equations to map 2D pixel coordinates $(u, v)$ and depth $Z$ back into 3D world space coordinates $(X, Y, Z)$.

---

## 🌀 3D Reconstruction Research Summary

In this project, I compared different practical 3D reconstruction methodologies:

1. **Structure from Motion (SfM)**: Reconstructs camera positions and sparse geometry by matching SIFT/ORB features across multiple offset photos. Excellent for geometric precision but slow and outputs sparse data.
2. **Multi-View Stereo (MVS)**: Creates dense point clouds and meshes using calibrated photos. Requires precise camera metrics.
3. **Neural Radiance Fields (NeRF)**: Represents scenes implicitly using MLPs. Excellent for photorealistic view synthesis, but slow to train and hard to extract explicit meshes.
4. **3D Gaussian Splatting (3DGS)**: Uses millions of explicit 3D Gaussians for real-time volumetric rendering. Training is fast, but splats are view-dependent and have large file sizes.
5. **Monocular Depth Backprojection (Selected)**: Uses a deep neural network (Depth Anything V2) to estimate depth map values from a **single image** and projects them back using a pinhole camera model. Highly practical, runs in real-time, and requires only one image.

---

## 🔬 Implementation Walkthrough

### Mathematical Backprojection
To project a 2D pixel coordinate $(u, v)$ to a 3D point $(X, Y, Z)$ in camera space, I implemented the following inverse projection equations in NumPy:

$$X = \frac{(u - c_x) \cdot Z}{f_x}$$
$$Y = \frac{(v - c_y) \cdot Z}{f_y}$$
$$Z = Z$$

Where:
- $f_x, f_y$ are approximated horizontal and vertical focal lengths using a 60-degree Field of View (FOV): $f = \text{Width} \cdot 0.866$.
- $c_x, c_y$ are the image center coordinates ($\frac{\text{Width}}{2}, \frac{\text{Height}}{2}$).
- Depth $Z$ is mapped from the normalized model disparity output: $Z = Z_{\text{min}} + (1.0 - d_{\text{norm}}) \cdot (Z_{\text{max}} - Z_{\text{min}})$ to obtain a visual depth field between $1.0\text{m}$ and $8.0\text{m}$.

### Execution Results
I successfully executed the standalone script `python 3d_reconstruction/reconstruct_3d.py`. The model completed depth estimation on my GPU and exported:
- A raw depth map (`output_depth.png`)
- A side-by-side comparison (`output_comparison.png`)
- A dense Stanford PLY point cloud model (`output_pointcloud.ply`) consisting of **1,875,298 colorized 3D points**.

---

## 🛠️ PR Workflow & AI Commit Details

### Pull Request (PR) Workflow
1. **Branch**: Isolated development of the 3D pipeline on the `main` branch (working locally).
2. **Commit**: Created logical, atomic commits documenting the additions.
3. **Push**: Will push local commits to GitHub upon final inspection.
4. **Pull Request**: Will open a pull request on the repository to merge the 3D module changes and invite review.

### Local Git Commit History
```text
commit 869c7a0d4cbb8f4300ee5c1e855b... (HEAD -> main)
Author: IoRagas <sagarmehmood1234@gmail.com>
Date:   Sat Jun 27 12:08:08 2026 +0500

    docs: add READMEs for 3D reconstruction pipeline

commit 9441927926cb24c3683cf11ab79f55994b1ee8c8 (origin/main)
Author: IoRagas <sagarmehmood1234@gmail.com>
Date:   Sat Jun 27 12:06:46 2026 +0500

    chore: delete obsolete project files and documentation

commit ff7dd0ec08f0f997b637afcb5295e94d4f299d8c
Author: IoRagas <sagarmehmood1234@gmail.com>
Date:   Sat Jun 27 11:54:47 2026 +0500

    Add monocular 3D reconstruction pipeline using Depth Anything V2
```

---

## 🧠 Reflection & Manual Verification

### What the AI Coding Assistant Did:
- Generated the boilerplate structure of `reconstruct_3d.py` and the Jupyter Notebook.
- Drafted the mathematical NumPy functions for pinhole projection.
- Formulated the research notes comparing the 3D reconstruction frameworks.

### What I Manually Verified:
- **Environment Checks**: Tested the imports and verified GPU/CUDA compatibility.
- **Debugged Image URLs**: The initial pipeline script attempted to load example images from a deleted GitHub raw directory (which returned a 404). I updated the pipeline to download a stable PyTorch Hub image (`dog.jpg`), which successfully executed.
- **Fixed Pillow Color Specifiers**: Remedied a Pillow crash during comparison map drawing where `rgba` string colors failed. I replaced the color string with a standard RGB tuple `(64, 64, 64)`.
- **Output Inspection**: Inspected the resulting grayscale depth map and checked that the exported `.ply` file had correct headers and non-zero coordinate geometry.
- **Repository Cleanup**: Executed git commits to clean up obsolete, pre-existing HTML profile page code so the repository only hosts this submission.
