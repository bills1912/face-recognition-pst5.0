# Face Recognition for Attendance to Build PST 5.0

## Getting Started
This is an application that is built base on machine learning model to recognize human face, especially for the visitor to PST of BPS - Statistics Sumatera Utara Province.

## How to Run
Step by step to run the application:
- Run `pip install -r requirements.txt` to install package that is required in this apps 
- Configure the database connection (for mongodb database) using connection string, and put it into the `MongoClient()` function in inside `add_data_to_database.py`, then run the file
- Run `encode_generator.py` to encode all figure dataset and put it in the database
- Finally, run `main.py` to run the application

> [!TIP]
> To make sure the application is running well, use `run.ipynb` file to make sure if all of the code is running well

> [!WARNING]
> At some moment, while you are installing `face_recognition` package, an error will be occured. So you must install `dlib` package manually from this [link](https://github.com/sachadee/Dlib), use the version that is compatible to your Python version.

