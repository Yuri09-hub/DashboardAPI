from fastapi import HTTPException
import pandas as pd
import matplotlib as mpl

def clean(df):
    df = df.dropna()
    return df

def file_dataframe(file):
    if file.endswith(".csv"):
        file_df = pd.read_csv(file)
        return file_df
    elif file.endswith(".xlsx"):
        file_df = pd.read_excel(file)
        return file_df
    else:
        return HTTPException(status_code=400,detail="File type not supported")