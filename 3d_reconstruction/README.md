# Monocular 3D Reconstruction Pipeline

This directory contains a self-contained, lightweight Python pipeline and Jupyter Notebook for generating a **dense 3D point cloud** from a single 2D image.

The pipeline utilizes **Depth Anything V2** (via Hugging Face `transformers`) to estimate pixel-wise relative depth and performs **inverse camera projection (backprojection)** to generate the 3D geometry.

---

## 📂 Folder Architecture

- **`reconstruct_3d.py`**: Standalone Python execution script.
- **`reconstruct_3d_notebook.ipynb`**: Interactive Jupyter Notebook walkthrough.
- **`notes.md`**: In-depth research notes on 3D reconstruction methods (SfM, MVS, NeRF, 3DGS) and mathematical proofs.
- **`input.jpg`**: The input image (automatically downloaded if missing).
- **`output_depth.png`**: Predicted grayscale depth map.
- **`output_comparison.png`**: Side-by-side visualization of input vs. depth map.
- **`output_pointcloud.ply`**: Resulting colorized dense 3D point cloud file.

---

## 🛠️ Setup & Execution

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install numpy torch torchvision transformers pillow
```

### 2. Run the Script
To download the sample image, run inference on the GPU (or CPU if no CUDA is available), and output the 3D files:
```bash
python reconstruct_3d.py
```

### 3. Output Point Cloud Scale
The point cloud is exported to a Stanford PLY file (`output_pointcloud.ply`). 
- Relative disparity values from the model are mapped to a visual depth range (between $1.0\text{m}$ and $8.0\text{m}$).
- Camera focal lengths ($f_x, f_y$) are automatically estimated using a virtual pinhole camera with a 60-degree Field of View (FOV).

---

## 🖥️ How to Visualize the 3D Model

The generated `output_pointcloud.ply` file is saved with color information for each point. You can view it in 3D space using the following tools:

1. **MeshLab** (Recommended, Free, Open-Source):
   - Download and install MeshLab.
   - Go to `File -> Import Mesh...` and select `output_pointcloud.ply`.
   - Left-click and drag to rotate the camera around the 3D point cloud.
2. **Blender**:
   - Go to `File -> Import -> Stanford (.ply)`.
3. **Web Viewer**:
   - Drag and drop `output_pointcloud.ply` into [creators3d.com/online-viewer](https://www.creators3d.com/online-viewer).

---

## 🧠 Behind the Scenes & Mathematics

For the full comparison of modern 3D reconstruction methods and the detailed equations of the camera projection model, read the [notes.md](file:///d:/VS_Code_Projects/PMW-Day1/3d_reconstruction/notes.md) file.
