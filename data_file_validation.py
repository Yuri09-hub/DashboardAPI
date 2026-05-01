from fastapi import HTTPException
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from enum import Enum
import openpyxl

class charType(str, Enum):
    plot = "plot"
    bar = "bar"
    scatter = "scatter"
    line = "line"
    hist = "hist"

class columnType(str, Enum):
    integer = "int"
    float = "float"
    boolean = "boolean"
    string = "string"
    datetime = "datetime"

def column_converter(df,y,x, y_type:Enum, x_type:Enum):
    if y_type == x_type == "String":
        raise HTTPException(status_code=400,detail="You cannot have two columns of type string.")
    


def clean(df):
    df = df.dropna()
    df.columns = df.columns.str.strip()
    return df

def file_dataframe(file,y,x):
    if file.filename.endswith(".csv"):
        file_df = pd.read_csv(file.file,low_memory=False)
        file_df = file_df[[y, x]]
        return clean(file_df)
    elif file.filename.endswith(".xlsx"):
        file_df = pd.read_excel(file.file)
        file_df = file_df[[y, x]]
        return clean(file_df)
    else:
        raise HTTPException(status_code=400,detail="File type not supported")


def chart_generator(file_df,chart_type,y,x):

    if x not in file_df.columns and y not in file_df.columns:
        raise HTTPException(status_code=400,detail="Column not found")

    fig, ax = plt.subplots()
    file_df.plot(kind=chart_type, y=y, x=x)

    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf