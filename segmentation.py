"""
segmentation.py
Handles data loading, processing, mask file management, and the segmentation algorithm.
"""
import os
import glob
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

def load_image(filepath):
    """Loads a NIfTI (.nii/.nii.gz) or Numpy (.npy) array based on the file extension."""
    if filepath.endswith('.npy'):
        return np.load(filepath)
    return nib.load(filepath).get_fdata()

def normalize_intensity(image):
    """Scales image pixel values to a 0.0 - 1.0 range for consistent algorithm processing."""
    min_val = np.min(image)
    max_val = np.max(image)
    if max_val == min_val:
        return image
    return (image - min_val) / (max_val - min_val)

def save_mask(mask, filepath):
    """Saves a binary mask array to disk. Supports both .npy and .nii formats."""
    # Ensure the target directory exists before saving
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if filepath.endswith('.npy'):
        np.save(filepath, mask.astype(np.uint8))
    else:
        # affine=np.eye(4) maps array coordinates to physical space (required for NIfTI)
        nifti_img = nib.Nifti1Image(mask.astype(np.uint8), affine=np.eye(4))
        nib.save(nifti_img, filepath)

def delete_mask(filepath):
    """Deletes a mask file from disk if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted: {filepath}")
    else:
        print(f"File not found: {filepath}")

def segment(image):
    """
    TODO: Implement the segmentation algorithm here. This function should take a 2D numpy array (image) as input and return a binary mask of the same shape, where 1 indicates lesion presence and 0 indicates background.
    
    Input : 2D numpy array (values between 0.0 and 1.0).
    Output: 2D numpy array (same shape), 1 = lesion, 0 = background.
    """
    # Starter mask: threshold by pixel intensity. Pixels > 0.5 become 1 (True), others 0 (False)
    # how can you improve this? think about image properties, noise, and lesion characteristics.
    mask = (image > 0.5) 
    return mask.astype(np.uint8)

if __name__ == "__main__":
    # Batch processing execution
    input_dir = "students/dev/images"
    output_dir = "predictions"
    
    files = sorted(glob.glob(f"{input_dir}/*.npy"))
    if not files:
        print(f"No images found in {input_dir}")
        exit(1)

    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    
    for ax, filepath in zip(axes.ravel(), files):
        name = os.path.basename(filepath)
        
        # 1. Load and normalize
        img = load_image(filepath)
        img = normalize_intensity(img)
        
        # 2. Segment
        pred = segment(img)
        
        # 3. Save mask output
        out_path = os.path.join(output_dir, name)
        save_mask(pred, out_path)
        
        # 4. Visualize
        ax.imshow(img, cmap="gray")
        if np.any(pred):
            ax.contour(pred, levels=[0.5], colors="red")   
        ax.set_title(name.replace('.npy', ''))
        ax.axis("off")
        
    plt.tight_layout()
    plt.show()