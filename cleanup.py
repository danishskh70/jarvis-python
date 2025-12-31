import os

# Path to HF cache on Windows
cache_dir = os.path.expanduser(r"C:\Users\Acer\.cache\huggingface\hub")

if not os.path.exists(cache_dir):
    print("Hugging Face cache folder not found!")
else:
    print(f"Checking cache in: {cache_dir}\n")
    for folder in os.listdir(cache_dir):
        folder_path = os.path.join(cache_dir, folder)
        if os.path.isdir(folder_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            size_gb = total_size / (1024**3)
            print(f"{folder}: {size_gb:.2f} GB")
