from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os

# Create the app instance
app = FastAPI()

# Directory to mount data
#DATA_DIR = r"D:\Tutorial\DevOps Workshop\azure-file-mount\data"  # Use raw string for Windows paths
DATA_DIR = '/mnt/data'  # Azure File Share mount path
os.makedirs(DATA_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file and save it to the mounted data directory.
    """
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "path": file_path}

@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a file from the mounted data directory.
    """
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

@app.get("/files/")
async def list_files():
    """
    List all files in the mounted data directory.
    """
    files = os.listdir(DATA_DIR)
    return {"files": files}
