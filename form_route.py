from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

file_save = Path('file_saves')

form_route = APIRouter(tags=["form"], prefix="/form")

@form_route.post("/uploadfile")
async def upload_file(file: UploadFile):
    try:

        file_path = file_save / file.filename


        content = await file.read()

    
        file_path.write_bytes(content)
        return {"filename": file.filename}

    except OSError as e:
        print(e)
        return HTTPException(status_code=400, detail="Error")


