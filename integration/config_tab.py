import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

class config_tab:
    def __init__(self):
        self.file_cfg_path='C:\\Users\\17940\\Python_Testing\\CAF_Sequencer\\config_file\\config_file.json'
        
        with open(self.file_cfg_path,'r') as jsonfile:
            self.config_json=json.load(jsonfile)
            jsonfile.close()
        self.correct=False
        self.master = tk.Tk()
        self.master.title("Configuración de Secuenciador") 
        self.master.geometry("600x320")
        self.master.iconbitmap("caf_icon.ico")
        self.master.resizable(width=False, height=False)

        self.notebook = ttk.Notebook(self.master)
        #self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.notebook.pack()

        close_bt=tk.Button(self.master, text='Update', font=("Arial",12), command=self.update_json)
        close_bt.pack(pady=10,ipady=10,padx=250,ipadx=200)
        
        global_frame=tk.Frame(self.notebook)
        global_frame.rowconfigure(0, weight=1)
        global_frame.rowconfigure(1, weight=1)
        global_frame.rowconfigure(2, weight=1)
        global_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(global_frame, text="General")
        
        #Entradas de general
        self.templates=cuadro_sel(global_frame,'Protocol JSON Templates',initialdir=self.config_json["json_protocols"])
        #self.sandbox.grid(column=0,row=0,sticky="nsew")
        self.ejecuciones=cuadro_sel(global_frame,'Executions JSON',initialdir=self.config_json["json_runs"])
        #self.ejecuciones.grid(column=0,row=1,sticky="nsew")
        self.excel_export=cuadro_sel(global_frame,'Excel export',initialdir=self.config_json["excel_runs"])
        #self.excel_export.grid(column=0,row=2,sticky="nsew")


        con_frame=tk.Frame(self.notebook)
        con_frame.rowconfigure(0, weight=1)
        con_frame.rowconfigure(1, weight=1)
        con_frame.rowconfigure(2, weight=1)
        con_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(con_frame, text="Connections")

        #Entradas de connections
        self.ip=connection_entry(con_frame,'IP',ini=self.config_json["IP"])
        #self.sandbox.grid(column=0,row=0,sticky="nsew")
        self.password=connection_entry(con_frame,'Password',ini=self.config_json["Key"])
        #self.ejecuciones.grid(column=0,row=1,sticky="nsew")
        self.Connection_name=connection_entry(con_frame,'Connection Name',ini=self.config_json["Connection"])
        #self.excel_export.grid(column=0,row=2,sticky="nsew")


    def main(self):
        self.master.mainloop()

    def update_json(self):
        self.config_json.update({"json_protocols":self.templates.get_entry()})
        self.config_json.update({"json_runs":self.ejecuciones.get_entry()})
        self.config_json.update({"excel_runs":self.excel_export.get_entry()})
        self.config_json.update({"IP":self.ip.get_entry()})
        self.config_json.update({"Key":self.password.get_entry()})
        self.config_json.update({"Connection":self.Connection_name.get_entry()}) 

        jsonfile=open(self.file_cfg_path,'w')
        print(self.config_json)     
        json.dump(self.config_json, jsonfile, indent = 4)
        jsonfile.close()
        self.master.destroy()
        

class cuadro_sel:
    def __init__(self,frame_place,field_name, initialdir=''):
        #se crea el marco
        self.ini=initialdir
        self.global_frame=ttk.Frame(frame_place)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=2)
        self.global_frame.rowconfigure(1, weight=3)
        self.global_frame.columnconfigure(0, weight=10)
        self.global_frame.columnconfigure(1, weight=1)

        # Etiqueta para la entrada de texto
        etiqueta = tk.Label(self.global_frame, text=field_name, anchor='sw')
        etiqueta.grid(column=0,row=0,sticky="nsew", padx=5, ipadx=5)

        # Entrada de texto para mostrar el directorio seleccionado
        valor_por_defecto = tk.StringVar()
        valor_por_defecto.set(self.ini)
        self.entrada_directorio = tk.Entry(self.global_frame, width=100,textvariable=valor_por_defecto)
        self.entrada_directorio.grid(column=0,row=1,sticky="nsew",pady=10, ipady=5, padx=10, ipadx=10)

        # Botón para abrir el cuadro de diálogo
        boton = tk.Button(self.global_frame, text="Browse", command=self.seleccionar_directorio)
        boton.grid(column=1,row=1,sticky="nsew",pady=10, ipady=5, padx=10, ipadx=10)


    def seleccionar_directorio(self):
        directorio = filedialog.askdirectory(initialdir=self.ini)
        if directorio:
            self.entrada_directorio.delete(0, tk.END)  # Limpiar la entrada de texto
            self.entrada_directorio.insert(0, directorio)  # Mostrar el directorio seleccionado en la entrada de texto
        
    def get_entry(self): return self.entrada_directorio.get()
    

class connection_entry:
    def __init__(self,frame_place,field_name,ini=''):
        self.global_frame=ttk.Frame(frame_place)
        self.global_frame.rowconfigure(0, weight=2)
        self.global_frame.rowconfigure(1, weight=3)
        self.global_frame.pack()

        # Etiqueta para la entrada de texto
        valor_por_defecto = tk.StringVar()
        valor_por_defecto.set(ini)
        etiqueta = tk.Label(self.global_frame, text=field_name, anchor='sw')
        etiqueta.grid(column=0,row=0,sticky="nsew", padx=5, ipadx=5)

        # Entrada de texto para mostrar el directorio seleccionado
        self.entrada= tk.Entry(self.global_frame, width=100, textvariable=valor_por_defecto)
        self.entrada.grid(column=0,row=1,sticky="nsew",pady=10, ipady=5, padx=10, ipadx=10)

    def get_entry(self): return self.entrada.get()


if __name__ == "__main__":
    c=config_tab()
    c.main()