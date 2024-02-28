import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class info_tab():
    def __init__(self):
        self.correct=False
        self.master = tk.Tk()
        self.master.title("Secuenciador information") 
        self.master.geometry("400x200")
        self.master.iconbitmap("caf_icon.ico")
        self.master.resizable(width=False, height=False)
        

        self.global_frame=ttk.Frame(self.master)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=3)
        self.global_frame.rowconfigure(1, weight=2)
        self.global_frame.rowconfigure(2, weight=2)
        self.global_frame.rowconfigure(3, weight=2)

        #Crear Text label titulo
        self.label_name = ttk.Label(self.global_frame, text="Baseline info", font=("Arial", 20))
        self.label_name.grid(column=0,row=0,sticky="nsew", ipady=15)

        self.label_name = ttk.Label(self.global_frame, text="Secuenciador version: v1.0.0", font=("Arial", 12))
        self.label_name.grid(column=0,row=1,sticky="nsew", ipady=10)

        self.label_name = ttk.Label(self.global_frame, text="Parser version: v1.0.0", font=("Arial", 12))
        self.label_name.grid(column=0,row=2,sticky="nsew", ipady=10)

        self.label_name = ttk.Label(self.global_frame, text="Release By: Víctor Sevillano G. CAF on 28/02/2024", font=("Arial", 12))
        self.label_name.grid(column=0,row=3,sticky="nsew", ipady=10)

    def main(self):
        self.master.mainloop()
      
    
if __name__ == "__main__":
    i=info_tab()
    i.main()
