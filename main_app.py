import customtkinter as ctk

import games.pin_ball as pb
import games.road_rash as rr
import games.motor_rider as mr
import games.chrome_dino as cd


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("Game Hub")
app.geometry("250x300")

def button_function():
    print("button pressed")
    
button1 = ctk.CTkButton(master=app, text="🚗 Road Rash", command=rr.main)
button1.place(relx=0.5, rely=0.30, anchor=ctk.CENTER)

button2 = ctk.CTkButton(master=app, text="🦖 Chrome Dino", command=cd.main)
button2.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

button3 = ctk.CTkButton(master=app, text="🚲 Motor Rider", command=mr.main)
button3.place(relx=0.5, rely=0.60, anchor=ctk.CENTER)

button4 = ctk.CTkButton(master=app, text="📌 Pin Ball", command=pb.main)
button4.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

app.mainloop()