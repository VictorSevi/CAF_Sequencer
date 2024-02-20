import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class sign_in():
    def __init__(self,master,running_app):
        self.app=running_app
        self.correct=False
        self.master = master
        self.master.title("Secuenciador Sign in") 
        self.master.geometry("500x200")
        self.master.iconbitmap("caf_icon.ico")
        self.master.resizable(width=False, height=False)
        

        self.global_frame=ttk.Frame(self.master)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=3)
        self.global_frame.rowconfigure(1, weight=2)
        self.global_frame.rowconfigure(2, weight=2)
        self.global_frame.rowconfigure(3, weight=2)

        self.global_frame.columnconfigure(0, weight=1)
        self.global_frame.columnconfigure(1, weight=5)

        #crear boton de Carga
        self.bt_load = ttk.Button(self.global_frame, text="Sign in",command=self.sign_in)
        self.bt_load.grid(column=0,row=3,sticky="nsew")

        #Crear Text space Chapa
        self.entry_chapa = ttk.Entry(self.global_frame)
        self.entry_chapa.grid(column=1,row=1,sticky="nsew",pady=10, ipady=10, padx=10, ipadx=10)
        self.label_chapa = ttk.Label(self.global_frame, text="Chapa",anchor="center",font=("Arial", 14))
        self.label_chapa.grid(column=0,row=1,sticky="nsew")

        #Crear Text space Nombre
        self.entry_name = ttk.Entry(self.global_frame)
        self.entry_name.grid(column=1,row=2,sticky="nsew",pady=10, ipady=10, padx=10, ipadx=10)
        self.label_name = ttk.Label(self.global_frame, text="Name",anchor="center",font=("Arial", 14))
        self.label_name.grid(column=0,row=2,sticky="nsew")

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
            self.app.set_credentials(self.entry_name.get(), self.entry_chapa.get())
            self.correct=True
            self.master.destroy()
            
    def error_chapa(self):
        messagebox.showwarning("Error", "Chapa incorrecta!")
    def error_name(self):
        messagebox.showwarning("Error", "Nombre incorrecto!")
    def passed(self):
        return self.correct

        
    
if __name__ == "__main__":
    x=tk.Tk()
    s=sign_in(x)
    x.mainloop()
    print(s.get_name())
    print(s.get_chapa())