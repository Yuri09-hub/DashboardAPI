# 📊 Dashboard API

## Overview
This project is a backend API built with FastAPI that allows users to upload datasets (CSV/Excel), process data dynamically, and generate charts automatically.

It is designed to simplify data visualization by handling data conversion, validation, and chart generation through a single API.

---

## Features

- Upload CSV and Excel files
- Automatic data parsing with pandas
- Dynamic column selection (X and Y)
- Data type conversion (int, float, datetime, boolean, string)
- Automatic chart generation (bar, line, etc.)
- Data validation and cleaning
- Error handling for invalid datasets

---

## Technologies Used

- Python
- FastAPI
- Pandas
- Matplotlib
- Uvicorn

---

## Project Structure


project/

│

├── form_route.py # API routes (upload & request handling)

├── data_file_validation.py # Data processing & validation logic

├── chart_generator.py # Chart creation logic

├── venv/ # Virtual environment

└── main.py # Application entry point


---


##Running the API

uvicorn main:app --reload


## API documentation:

http://127.0.0.1:8000/docs


##System Logic

User uploads a dataset (CSV or Excel)

API reads and validates the file

User selects X and Y columns

System converts data types if needed

A chart is generated and returned as output

##Author

Yuri Rodrigues

Angola 🇦🇴
