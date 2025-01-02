from pymongo import MongoClient

client = MongoClient('path/of/mongodb/connection')
frecog_mongo = client["face_recognition_mongo"]
frecog_mongo_collect = frecog_mongo["frecog_data"]

data = [
     {
            "id":"321654",
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
     {
            "id":"852741",
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
     {
            "id":"963852",
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
]

frecog_mongo_insert = frecog_mongo_collect.insert_many(data)