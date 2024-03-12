import tkinter as tk
from tkinter import ttk

class botonera_superior():
    def __init__(self,frame_place,r=0, c=0):#frame_place,load_func,help_func,config_func,info_func,json_func,r=0, c=0):

        #crear frame para botones
        self.bt_frame = ttk.Frame(frame_place)
        self.bt_frame.grid(row=r, sticky="nsew")

        #crear boton de Carga
        self.bt_load = ttk.Button(self.bt_frame, text="Load")
        self.bt_load.grid(column=0,row=0)

        #crear boton de ayuda
        self.bt_help = ttk.Button(self.bt_frame, text="Help")
        self.bt_help.grid(column=4,row=0)

        #crear boton de Configurasao
        self.bt_config = ttk.Button(self.bt_frame, text="Config")
        self.bt_config.grid(column=2,row=0)

        #crear boton de informacion
        self.bt_info = ttk.Button(self.bt_frame, text="Info")
        self.bt_info.grid(column=3,row=0)
    
        #crear boton de parser
        self.bt_parser = ttk.Button(self.bt_frame, text="Create json")
        self.bt_parser.grid(column=1,row=0)
        
    def config(self, load, help, config, info, create_json):

        #mapeo de los botones a sus funciones
        self.bt_load.config(command=load)
        self.bt_help.config(command=help)
        self.bt_config.config(command=config)
        self.bt_info.config(command=info)
        self.bt_parser.config(command=create_json)


        

if __name__ == "__main__":
    x=tk.Tk()
    s=botonera_superior(x)
    x.mainloop()