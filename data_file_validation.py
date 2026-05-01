from fastapi import HTTPException
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from enum import Enum


class charType(str, Enum):
    bar = "bar"
    scatter = "scatter"
    line = "line"
    hist = "hist"


class columnType(str, Enum):
    integer = "integer"
    float = "float"
    boolean = "boolean"
    string = "String"
    datetime = "datetime"


def column_converter(df, y, y_type):
    if y not in df.columns:
        raise HTTPException(status_code=400, detail="Column not found")

    if y_type == "integer":
        df[y] = pd.to_numeric(df[y], errors="coerce", downcast="integer")
    elif y_type == "float":
        df[y] = pd.to_numeric(df[y], errors="coerce", downcast="float")
    elif y_type == "boolean":
        df[y] = df[y].astype(bool)
    elif y_type == "Datetime":
        df[y] = pd.to_datetime(df[y], format="%Y-%m-%d")
    elif y_type == "String":
        df[y] = df[y].str[:4] + "..."
        df[y] = df[y].str.strip()
        df[y] = df[y].str.title()

    return df


def data_set_clean(df):
    df.columns = df.columns.str.strip()
    df = df.dropna()
    df = df.head(15)

    return df


def file_dataframe(file, y, x, y_type, x_type):
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(status_code=400, detail="File type not supported")

    if len(df.columns) > 2:
        df = df[[y,x]]

    df = data_set_clean(df)
    df = column_converter(df, y, y_type)
    df = column_converter(df, x, x_type)

    return df


def chart_generator(file_df, chart_type, y, x):
    if x not in file_df.columns or y not in file_df.columns:
        raise HTTPException(status_code=400, detail="Column not found")

    fig, ax = plt.subplots()

    if pd.api.types.is_string_dtype(file_df[y]):
        file_df.plot(color='blue', kind=chart_type, y=x, x=y, ax=ax)
        plt.ylabel(x)
        plt.xlabel(y)
    else:
        file_df.plot(color='blue', kind=chart_type, y=y, x=x, ax=ax)
        plt.ylabel(y)
        plt.xlabel(x)

    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf
