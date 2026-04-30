from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from models import User, form
from pathlib import Path
from data_file_validation import file_dataframe

file_save = Path('file_saves')

form_route = APIRouter(tags=["form"], prefix="/form")

@form_route.post("/uploadfile")
async def upload_file(file: UploadFile, user: User = Depends(verify_token),
                      session:Session = Depends(get_session)):
    try:
        file_path = file_save / file.filename

        content = await file.read()

        file_path.write_bytes(content)

        #locale = form(file=str(file_path),user_id=user.id)

        return {"filename": file.filename,
                "location": f"{file_save}/{file.filename}"
        }
    except OSError as e:
        print(e)
        return HTTPException(status_code=400, detail="Error")


