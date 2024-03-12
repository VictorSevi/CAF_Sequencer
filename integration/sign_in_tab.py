import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import app

class sign_in():
    def __init__(self):
        self.credentials={"Name":"", "Chapa":"", "UT":""}
        self.correct=False
        self.master = tk.Tk()
        self.master.title("Secuenciador Sign in") 
        self.master.geometry("500x300")
        #self.master.iconbitmap("caf_icon.ico")
        self.master.resizable(width=False, height=False)
        

        self.global_frame=ttk.Frame(self.master)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=3)
        self.global_frame.rowconfigure(1, weight=2)
        self.global_frame.rowconfigure(2, weight=2)
        self.global_frame.rowconfigure(3, weight=2)
        self.global_frame.rowconfigure(4, weight=2)

        self.global_frame.columnconfigure(0, weight=1)
        self.global_frame.columnconfigure(1, weight=5)

        #crear boton de Carga
        self.bt_load = ttk.Button(self.global_frame, text="Sign in",command=self.sign_in)
        self.bt_load.grid(column=0,row=4,sticky="nsew")

        #Crear Text space Chapa
        self.entry_chapa = ttk.Entry(self.global_frame, font=('Arial',14))
        self.entry_chapa.grid(column=1,row=1,sticky="nsew",pady=10, ipady=10, padx=10, ipadx=10)
        self.label_chapa = ttk.Label(self.global_frame, text="Chapa",anchor="center",font=("Arial", 14))
        self.label_chapa.grid(column=0,row=1,sticky="nsew")

        #Crear Text space Nombre
        self.entry_name = ttk.Entry(self.global_frame,font=('Arial',14))
        self.entry_name.grid(column=1,row=2,sticky="nsew",pady=10, ipady=10, padx=10, ipadx=10)
        self.label_name = ttk.Label(self.global_frame, text="Name",anchor="center",font=("Arial", 14))
        self.label_name.grid(column=0,row=2,sticky="nsew")

        #Crear Text space UT
        self.entry_ut = ttk.Entry(self.global_frame,font=('Arial',14))
        self.entry_ut.grid(column=1,row=3,sticky="nsew",pady=10, ipady=10, padx=10, ipadx=10)
        self.label_ut = ttk.Label(self.global_frame, text="UT",anchor="center",font=("Arial", 14))
        self.label_ut.grid(column=0,row=3,sticky="nsew")

        #Crear Text label titulo
        self.label_name = ttk.Label(self.global_frame, text="Bienvenido! ", font=("Arial", 26))
        self.label_name.grid(column=0,row=0,sticky="nsew")
    
    def sign_in(self):
        try:
            num=int(self.entry_chapa.get())
        except:
            self.error_chapa()

        if not (len(self.entry_chapa.get()) == 5):
            self.error_chapa()
        
        elif len(self.entry_name.get()) == 0:
            self.error_name()
        
        else:
            self.credentials={"Name":self.entry_name.get(), "Chapa":self.entry_chapa.get(), "UT":self.entry_ut.get()}
            self.correct=True
            self.master.destroy()

    def get_credentials(self):
        return self.credentials
            
    def error_chapa(self):
        messagebox.showwarning("Error", "Chapa incorrecta!")
    def error_name(self):
        messagebox.showwarning("Error", "Nombre incorrecto!")
    def passed(self):
        return self.correct
    def success(self):
        return self.correct

    def main(self):
        self.master.mainloop()