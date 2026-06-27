import os
import sys
import urllib.request
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline

def download_sample_image(url, save_path):
    print(f"Downloading sample image from: {url}")
    try:
        # User-agent header to avoid blocking from some hosts
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded sample image successfully to {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading sample image: {e}")
        return False

def generate_depth_map(image_path, model_name="depth-anything/Depth-Anything-V2-Small-hf"):
    device = 0 if torch.cuda.is_available() else -1
    device_name = "GPU (CUDA)" if device == 0 else "CPU"
    print(f"Initializing Hugging Face depth-estimation pipeline...")
    print(f"Using model: {model_name}")
    print(f"Running inference on: {device_name}")
    
    # Load pipeline
    pipe = pipeline(task="depth-estimation", model=model_name, device=device)
    
    print(f"Opening input image: {image_path}")
    img = Image.open(image_path).convert("RGB")
    
    print("Running depth estimation model...")
    result = pipe(img)
    
    # The pipeline outputs the predicted depth map as a PIL grayscale Image
    depth_map = result["depth"]
    return img, depth_map

def backproject_to_ply(color_img, depth_img, output_ply_path):
    print("Beginning 3D back-projection to point cloud...")
    
    # Convert images to arrays
    color_arr = np.array(color_img)
    depth_arr = np.array(depth_img, dtype=np.float32)
    
    H, W = depth_arr.shape
    print(f"Image dimensions: {W}x{H} pixels")
    
    # 1. Define virtual pinhole camera intrinsics
    # Assuming Field of View (FOV) of approx 60 degrees:
    # fx = fy = W / (2 * tan(30 deg)) = W / 1.1547 ≈ W * 0.866
    fx = fy = W * 0.866
    cx = W / 2.0
    cy = H / 2.0
    
    # 2. Convert raw relative depth (0-255 grayscale disparity) to depth values (Z)
    # In Depth-Anything, larger pixel values mean closer objects (disparity).
    # Normalize disparity to [0, 1]
    disp_norm = depth_arr / 255.0
    
    # Map disparity to depth Z in a realistic visual range (e.g. 1.0m to 8.0m)
    # Z = min_z + (1.0 - disp_norm) * (max_z - min_z)
    min_z = 1.0
    max_z = 8.0
    Z = min_z + (1.0 - disp_norm) * (max_z - min_z)
    
    # 3. Create pixel grid coordinate mapping
    u, v = np.meshgrid(np.arange(W), np.arange(H))
    
    # 4. Apply backprojection formula:
    # X = (u - cx) * Z / fx
    # Y = (v - cy) * Z / fy
    X = (u - cx) * Z / fx
    Y = (v - cy) * Z / fy
    
    # 5. Stack into N x 3 arrays for points and colors
    points = np.stack((X, Y, Z), axis=-1).reshape(-1, 3)
    colors = color_arr.reshape(-1, 3)
    
    # 6. Export as ASCII PLY file
    print(f"Writing {len(points)} vertices to PLY file: {output_ply_path}")
    
    header = (
        "ply\n"
        "format ascii 1.0\n"
        f"element vertex {len(points)}\n"
        "property float x\n"
        "property float y\n"
        "property float z\n"
        "property uchar red\n"
        "property uchar green\n"
        "property uchar blue\n"
        "end_header\n"
    )
    
    try:
        with open(output_ply_path, "w") as f:
            f.write(header)
            # Write points and colors efficiently
            for i in range(len(points)):
                f.write(
                    f"{points[i, 0]:.4f} {points[i, 1]:.4f} {points[i, 2]:.4f} "
                    f"{int(colors[i, 0])} {int(colors[i, 1])} {int(colors[i, 2])}\n"
                )
        print(f"Successfully generated PLY file: {output_ply_path}")
    except Exception as e:
        print(f"Error saving PLY file: {e}")

def create_comparison_image(color_img, depth_img, output_path):
    print("Generating comparison visualization...")
    W, H = color_img.size
    
    # Normalize depth image to grayscale and construct RGB format
    depth_rgb = depth_img.convert("RGB")
    
    # Create combined canvas: left side input, right side depth, with extra height for text label
    label_height = 40
    canvas_w = W * 2 + 10
    canvas_h = H + label_height
    
    combined = Image.new("RGB", (canvas_w, canvas_h), "#060913")
    
    # Paste images
    combined.paste(color_img, (0, 0))
    combined.paste(depth_rgb, (W + 10, 0))
    
    # Draw text annotations
    draw = ImageDraw.Draw(combined)
    
    # Try using default font
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
        
    draw.text((15, H + 10), "Original Input Image", fill="#06b6d4", font=font)
    draw.text((W + 25, H + 10), "Depth Anything V2 (Predicted Disparity Map)", fill="#b55fe6", font=font)
    
    # Draw simple thin border dividing them
    draw.line([(W + 4, 0), (W + 4, H)], fill=(64, 64, 64), width=2)
    
    try:
        combined.save(output_path)
        print(f"Comparison visualization saved to {output_path}")
    except Exception as e:
        print(f"Error saving comparison image: {e}")

def main():
    # Set directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input/Output paths
    input_image_path = os.path.join(script_dir, "input.jpg")
    output_depth_path = os.path.join(script_dir, "output_depth.png")
    output_comparison_path = os.path.join(script_dir, "output_comparison.png")
    output_ply_path = os.path.join(script_dir, "output_pointcloud.ply")
    
    # Download sample image if not already present
    if not os.path.exists(input_image_path):
        sample_url = "https://raw.githubusercontent.com/pytorch/hub/master/images/dog.jpg"
        success = download_sample_image(sample_url, input_image_path)
        if not success:
            print("Failed to secure an input image. Please place 'input.jpg' in the directory and run again.")
            sys.exit(1)
            
    # Run pipeline
    try:
        color_img, depth_img = generate_depth_map(input_image_path)
        
        # Save raw predicted depth
        depth_img.save(output_depth_path)
        print(f"Raw depth map saved to {output_depth_path}")
        
        # Create and save side-by-side comparison
        create_comparison_image(color_img, depth_img, output_comparison_path)
        
        # Project and save as PLY Point Cloud
        backproject_to_ply(color_img, depth_img, output_ply_path)
        
        print("\n3D Reconstruction pipeline completed successfully!")
        print(f"Generated outputs:\n - Depth Map: {output_depth_path}\n - Comparison: {output_comparison_path}\n - Point Cloud: {output_ply_path}")
        
    except Exception as e:
        print(f"Error executing reconstruction pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
