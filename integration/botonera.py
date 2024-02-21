import tkinter as tk
from tkinter import ttk

class botonera_superior():
    def __init__(self,frame_place,load_func,help_func,config_func,info_func,json_func,r=0, c=0):

        self.load=load_func
        self.help=help_func
        self.config=config_func
        self.info=info_func
        self.create_json=json_func

        #crear frame para botones
        self.bt_frame = ttk.Frame(frame_place)
        self.bt_frame.grid(row=r, sticky="nsew")

        #crear boton de Carga
        self.bt_load = ttk.Button(self.bt_frame, text="Load",command=self.load)
        self.bt_load.grid(column=0,row=0)

        #crear boton de ayuda
        self.bt_help = ttk.Button(self.bt_frame, text="Help",command=self.help)
        self.bt_help.grid(column=4,row=0)

        #crear boton de Configurasao
        self.bt_config = ttk.Button(self.bt_frame, text="Config",command=self.config)
        self.bt_config.grid(column=2,row=0)

        #crear boton de informacion
        self.bt_info = ttk.Button(self.bt_frame, text="Info",command=self.info)
        self.bt_info.grid(column=3,row=0)
    
        #crear boton de parser
        self.bt_info = ttk.Button(self.bt_frame, text="Create json",command=self.create_json)
        self.bt_info.grid(column=1,row=0)
        
    
if __name__ == "__main__":
    x=tk.Tk()
    s=botonera_superior(x)
    x.mainloop()