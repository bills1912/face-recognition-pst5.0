from customtkinter import *
from PIL import Image

app = CTk()
app.geometry("600x600")
app.resizable(0,0)

def new_guest_form():
        side_img_data = Image.open("side-img.png")

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))

        CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

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
                print(f"Name:{name.get()}\nKeperluan Mengunjungi PST: {keperluan.get('0.0', 'end')}")
                app.destroy()
                # print(keperluan.get("0.0", "end"))

        CTkButton(frame, text="Submit", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 13), 
                text_color="#ffffff", width=300, height=40, command=form_submit).pack(anchor="w", pady=(40, 20), padx=(25, 0))
        
        app.mainloop()
