import tkinter as tk
from tkinter import ttk
import protocol_tree
import botonera
import connection_tab


class gui():
    def __init__(self,credentials={"Name":"", "Chapa":"", "UT":""}):
        
        #Main Window create
        self.credentials=credentials
        self.master=tk.Tk()
        self.master.title("CAF Secuenciador") 
        self.master.geometry("1200x650")
        self.master.iconbitmap("caf_icon.ico")

        #Global frame  structure definition
        self.global_frame=ttk.Frame(self.master)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=1)
        self.global_frame.rowconfigure(1, weight=20, minsize=400)
        self.global_frame.rowconfigure(2, weight=1)
        self.global_frame.columnconfigure(0, weight=1)
        self.botonera = botonera.botonera_superior(self.global_frame)


        # Frame principal
        self.frame = ttk.Frame(self.global_frame)
        self.frame.grid(row=1, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=10)

        self.mapa_contenido = protocol_tree.protocol_map(self.frame)
        #self.app.set_mapa(self.mapa_contenido)

        # Crear un Notebook (pestañas)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=0,column=1, sticky="nsew")

        # Pestaña 1
        self.execution_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.execution_tab , text="Execution")
        #self.app.set_execution_loc(self.execution_tab )

        #scrollbar = ttk.Scrollbar(tab1, orient='vertical')

        # Pestaña 2
        self.connection_tab=connection_tab.connections_tab(self.notebook,'10.0.0.16')

        # Pestaña 3
        self.details_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.details_tab, text="Detail")


        #Frame informativo inferior
        self.info_frame = ttk.Frame(self.global_frame)
        self.info_frame.grid(row=2,column=0,sticky="nsew")
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=1)

        #etiquetas del frame informativo
        self.label_version = ttk.Label(self.info_frame,anchor="w", text="v1.0.0")
        self.label_version.grid(row=0,column=0, sticky="nsew")

        self.label_protocol = ttk.Label(self.info_frame,anchor="center", text="Chapa: "+self.credentials["Chapa"]+"  Name: "+self.credentials["Name"]+"  UT: "+self.credentials["UT"])
        self.label_protocol.grid(row=0,column=1, sticky="nsew")

        self.label_info= ttk.Label(self.info_frame,anchor="e", text="CAF-Testing")
        self.label_info.grid(row=0,column=2, sticky="nsew")

        self.save_bt=ttk.Button(self.info_frame,text="Save")
        self.save_bt.grid(row=0,column=3, sticky="nsew")

        

    def main(self): self.master.mainloop()

    def get_botonera(self): return self.botonera

    def get_mapa_contenido(self): return self.mapa_contenido
    
    def get_execution_tab(self): return self.execution_tab
    
    def get_connection_tab(self): return self.connection_tab
    
    def get_details_tab(self): return self.details_tab

    def get_label_protocol(self): return self.label_protocol

    def get_save_button(self): return self.save_bt

    

def main():
    g=gui()
    g.main()

if __name__ == "__main__":
    main()