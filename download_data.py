import os
import requests
import zipfile
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
from tqdm import tqdm

def download_file(url, filename):
    """Download a file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

def process_image(image_path, target_size=(224, 224)):
    """Process and compress an image"""
    try:
        # Open and convert to grayscale
        img = Image.open(image_path).convert('L')
        # Resize
        img = img.resize(target_size, Image.LANCZOS)
        # Save with compression
        img.save(image_path, 'JPEG', quality=85, optimize=True)
        return True
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return False

def download_and_organize_dataset():
    # Create directories
    os.makedirs("data/train", exist_ok=True)
    os.makedirs("data/val", exist_ok=True)
    os.makedirs("data/test", exist_ok=True)
    
    # Download the dataset
    print("Downloading dataset...")
    url = "https://data.mendeley.com/public-files/datasets/rscbjbr9sj/files/f12eaf6d-6023-432f-acc9-80c9d7393433/file_downloaded"
    zip_path = "data/chest_xray.zip"
    
    download_file(url, zip_path)
    
    # Extract the dataset
    print("Extracting files...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("data")
    
    # Process and organize files
    print("Organizing and compressing files...")
    base_path = Path("data/chest_xray")
    train_path = Path("data/train")
    val_path = Path("data/val")
    test_path = Path("data/test")
    
    for split in ["train", "val", "test"]:
        src_dir = base_path / split
        if split == "train":
            dst_dir = train_path
        elif split == "val":
            dst_dir = val_path
        else:
            dst_dir = test_path
            
        if src_dir.exists():
            for item in src_dir.iterdir():
                if item.is_dir():
                    dst_subdir = dst_dir / item.name
                    dst_subdir.mkdir(parents=True, exist_ok=True)
                    for file in item.iterdir():
                        if file.suffix.lower() in ['.jpeg', '.jpg', '.png']:
                            # Process and compress each image
                            process_image(file)
                            shutil.copy2(file, dst_subdir)
    
    # Clean up
    print("Cleaning up...")
    shutil.rmtree(base_path)
    os.remove(zip_path)
    print("Dataset download, compression, and organization complete!")

if __name__ == "__main__":
    download_and_organize_dataset() 