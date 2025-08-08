from fastapi import UploadFile
from pathlib import Path
from PIL import Image
import io

class FileService:
  def __init__(self):
    self.upload_folder = "app/static"
  
  def save_avatar(self, input: UploadFile, user_id: str) -> str:
    file_directory = Path(f"{self.upload_folder}/avatars")
    file_directory.mkdir(parents=True, exist_ok=True)

    # Extract file contents
    contents = input.file.read()
    
    # Open image from bytes using pillow
    image = Image.open(io.BytesIO(contents))
    image = image.convert("RGBA")

    # Generate unique filename
    unique_filename = f"{user_id}_avatar.webp"
    file_path = f"{file_directory}/{unique_filename}"

    image.save(file_path, format="webp", quality=85)

    return f"/static/avatars/{unique_filename}"
