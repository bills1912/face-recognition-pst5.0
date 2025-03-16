from datetime import datetime
from PIL import Image
from customtkinter import *
from pymongo import MongoClient
from io import BytesIO
import numpy as np
import sqlite3

# client = MongoClient('mongodb+srv://ricardozalukhu1925:kuran1925@cluster0.lhmox.mongodb.net/')
# frecog_mongo = client["face_recognition_mongo"]
# frecog_mongo_collect = frecog_mongo["frecog_data"]
# frecog_mongo_coll_img = frecog_mongo["image_recog_data"]

def new_guest_form(id, img_guest):
        sqliteConn = sqlite3.connect("face_recog_pst5_1200.db")
        cursor = sqliteConn.cursor()
        app = CTkToplevel()
        app.geometry("680x480")
        app.resizable(0,0)
        side_img_data = Image.open("side-img.png")

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))

        CTkLabel(master=app, image=side_img).pack(expand=True, side="left")

        frame = CTkScrollableFrame(master=app, width=350, height=480, fg_color="#ffffff")
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Selamat Datang di PST 5.0!", text_color="#601E88", anchor="w", justify="left", 
                font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Silahkan isi buku tamu berikut yah", text_color="#7E7E7E", anchor="w", justify="left", 
                font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="Nama:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14))\
                .pack(anchor="w", pady=(38, 0), padx=(25, 0))
        name = CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        name.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="Alamat:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14))\
                .pack(anchor="w", pady=(10, 0), padx=(25, 0))
        alamat = CTkTextbox(master=frame, width=300, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", height=80)
        alamat.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="Nomor Telepon:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14))\
                .pack(anchor="w", pady=(10, 0), padx=(25, 0))
        tel = CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        tel.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="Pekerjaan:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14))\
                .pack(anchor="w", pady=(10, 0), padx=(25, 0))
        kerja = CTkEntry(master=frame, width=300, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        kerja.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="Keperluan Mengunjungi PST:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14))\
                .pack(anchor="w", pady=(10, 0), padx=(25, 0))
        keperluan = CTkTextbox(master=frame, width=300, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", height=80)
        keperluan.pack(anchor="w", padx=(25, 0))

        # CTkScrollbar(app, command=frame.y)

        def form_submit():
                # guest_data = {
                #         "id":id,
                #         "name": f"{name.get()}",
                #         "job": f"{kerja.get()}",
                #         "phone_number": f"{tel.get()}",
                #         "address": f"{alamat.get('0.0', 'end')}",
                #         "total_attendance": 1,
                #         "purpose": f"{keperluan.get('0.0', 'end')}",
                #         "last_attendance_time": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                # }
                guest_data_sql = """INSERT INTO frecog_data(id, name, job, phone_number, address, total_attendance, purpose, last_attendance_time) 
                                        VALUES(?,?,?,?,?,?,?,?)"""
                
                guest_photo = """INSERT INTO image_recog_data(id, img_data) VALUES(?,?)"""
                                        
                # img_bytes = np.asanyarray(bytearray(BytesIO(img_guest).read()), np.uint8)
                # guest_photo = {"id":id, "img_data":",".join(str(arr) for arr in img_bytes)}
                
                # frecog_tinydb_collect.insert(guest_data)
                # frecog_tinydb_coll_img.insert(guest_photo)
                cursor.execute(guest_data_sql, (id, name.get(), kerja.get(), tel.get(), alamat.get('0.0', 'end'), 1, keperluan.get('0.0', 'end'), 
                                                datetime.now()))
                cursor.execute(guest_photo, (id, img_guest))
                
                sqliteConn.commit()
                
                app.quit()

        CTkButton(frame, text="Submit", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 13), 
                text_color="#ffffff", width=300, height=40, command=form_submit).pack(anchor="w", pady=(40, 20), padx=(25, 0))
        app.mainloop()
