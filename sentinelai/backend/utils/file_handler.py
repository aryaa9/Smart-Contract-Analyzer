import os

def save_upload(file, folder="data/contracts"):
    os.makedirs(folder, exist_ok=True)
    path = f"{folder}/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path
