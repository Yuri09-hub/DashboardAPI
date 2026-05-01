from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from models import User, form
from pathlib import Path
from data_file_validation import charType, chart_generator, file_dataframe


class PNGStreamingResponse(StreamingResponse):
    media_type = "image/png"


file_save = Path('file_saves')

form_route = APIRouter(tags=["form"], prefix="/form")


@form_route.post("/uploadfile")
async def upload_file( x:str, y:str, response:charType, user: User = Depends(verify_token),
                      session: Session = Depends(get_session),file: UploadFile = File(...)):

    if file.filename.endswith(".csv") or file.filename.endswith(".xlsx"):
        file_path = file_save / file.filename
        content = await file.read()
        file_path.write_bytes(content)

        # save relative path file
       # locale = form(file=str(file_path), user_id=user.id)
        #session.add(locale)
        #session.commit()

        file_df = file_dataframe(file, y.title(), x.title())
        buf = chart_generator(file_df, response.value,y,x)
        return StreamingResponse(buf, media_type="image/png")
    raise HTTPException(status_code=400, detail="Error3")


