import tkinter as tk
from tkinter import ttk
import import_excel
import protocol_tree
import botonera
import app


class gui():
    def __init__(self,master, running_app):
        
        #Main Window create
        self.app=running_app
        self.master=master
        self.master.title("CAF Secuenciador") 
        self.master.geometry("1100x550")
        self.master.iconbitmap("caf_icon.ico")

        #Global frame  structure definition
        self.global_frame=ttk.Frame(self.master)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=1)
        self.global_frame.rowconfigure(1, weight=20, minsize=400)
        self.global_frame.rowconfigure(2, weight=1)
        self.global_frame.columnconfigure(0, weight=1)

        self.botonera = botonera.botonera_superior(self.global_frame,self.app)


        # Frame principal
        self.frame = ttk.Frame(self.global_frame)
        self.frame.grid(row=1, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=10)

        self.mapa_contenido = protocol_tree.protocol_map(self.frame,self.app)
        #self.app.set_mapa(self.mapa_contenido)

        # Crear un Notebook (pestañas)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=0,column=1, sticky="nsew")

        # Pestaña 1
        tab1 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab1, text="Execution")
        self.app.set_execution_loc(tab1)
        #scrollbar = ttk.Scrollbar(tab1, orient='vertical')

        # Pestaña 2
        tab2 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab2, text="Status")
        conectlab=tk.Label(tab2,text="No connections active!!", fg="red", font=("Arial",48),pady=150)
        conectlab.pack()

        #Frame informativo inferior
        self.info_frame = ttk.Frame(self.global_frame)
        self.info_frame.grid(row=2,column=0,sticky="nsew")
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=1)

        #etiquetas del frame informativo

        self.label_version = ttk.Label(self.info_frame,anchor="w", text="v1.0.0")
        self.label_version.grid(row=0,column=0, sticky="nsew")

        self.label_protocol = ttk.Label(self.info_frame,anchor="center", text="Chapa: "+str(self.app.get_credentials().get("Chapa"))+"  Name: "+str(self.app.get_credentials().get("Name"))+"  UT: "+str(self.app.get_credentials().get("UT")))
        self.label_protocol.grid(row=0,column=1, sticky="nsew")

        self.label_info= ttk.Label(self.info_frame,anchor="e", text="CAF-Testing")
        self.label_info.grid(row=0,column=2, sticky="nsew")

        bt=ttk.Button(self.info_frame,text="Save",command=self.app.json_res)
        bt.grid(row=0,column=3, sticky="nsew")
    

def main():
    #root1 = tk.Tk()
    a=app.app()
    if(a.sign_in_menu()):
        root2= tk.Tk()
        g=gui(root2,a)
        root2.mainloop()

if __name__ == "__main__":
    main()

