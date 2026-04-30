from fastapi import APIRouter, UploadFile, File, HTTPException
from dependencies import get_session, verify_token
from pathlib import Path
file_save = Path('file_saves')

form_route = APIRouter(tags=["form"], prefix="/form")

@form_route.post("/uploadfile")
async def upload_file(file: UploadFile):
    try:
        file_path = file_save / file.filename

        content = await file.read()

        file_path.write_bytes(content)
        return {"filename": file.filename,
                "location": f"{file_save}/{file.filename}"
                }

    except OSError as e:
        print(e)
        return HTTPException(status_code=400, detail="Error")


