from fastapi import HTTPException
import pandas as pd
import matplotlib as mpl
from fastapi.responses import StreamingResponse
from io import BytesIO

class PNGStreamingResponse(StreamingResponse):
    media_type = "image/png"

def clean(df):
    df = df.dropna()
    return df

def file_dataframe(file):
    if file.endswith(".csv"):
        file_df = pd.read_csv(file,low_memory=False)
        return clean(file_df)
    elif file.endswith(".xlsx"):
        file_df = pd.read_excel(file)
        return clean(file_df)
    else:
        return HTTPException(status_code=400,detail="File type not supported")

def