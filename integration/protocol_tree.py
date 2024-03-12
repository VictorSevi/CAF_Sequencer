##########################################################################################################################
#
#   Código para la clase de la vista lateral de árbol donde se incluye la estructura del protocolo así como, titulo 
#   del protocolo edición y Botones de control de ejecución. Debe instanciar un protocolo ya que toda esta sección 
#   controla y monitorizael objeto protocolo que se haya cargado en la app.
#
#   Created by: Víctor Sevillano Gamarra a 01/03/2024 v1.0.0
#
#########################################################################################################################


import tkinter as tk
from tkinter import ttk

class protocol_map():
    def __init__(self,frame_place, r=0, c=0):
        
        #marco del mapa de protocolo
        self.frame = ttk.Frame(frame_place)
        self.frame.grid(row=r, column=c, sticky="nsew")
        self.frame.rowconfigure(0,weight=1)
        self.frame.rowconfigure(1,weight=30)
        self.frame.rowconfigure(2,weight=1)

        #se crea el arbol
        self.tree = ttk.Treeview(self.frame)
        self.tree.grid(row=1, column=0, sticky="nsew")

        self.tree["columns"] = ("Estado")
        self.tree.column("#0", width=150)
        self.tree.column("Estado", width=100)
        self.tree.heading("#0", text="Elemento")
        self.tree.heading("Estado", text="Estado")

        #se crea el titulo del arbol
        self.titulo=ttk.Label(self.frame,text="No item selected")
        self.titulo.grid(row=0, column=0, sticky="nsew")

        #se crea el marco de botones de ejecucion
        self.frame_buttons=ttk.Frame(self.frame)
        self.frame_buttons.grid(column=0,row=2)

        #se crea boton de ejecucion
        self.bt_exe = ttk.Button(self.frame_buttons, text="Execute")
        self.bt_exe.grid(column=0,row=0)

        #se crea boton de stop ejecucion
        self.bt_stop = ttk.Button(self.frame_buttons, text="Stop")
        self.bt_stop.grid(column=1,row=0)
        
    def set_protocol(self,protocol):
        self.protocol=protocol
        self.protocol.set_action_execution_end(self.eje)     #TBD
        self.protocol.set_tree(self.tree)                    #TBD


    def eje(self):
        self.protocol.update_result()
        self.protocol.update_tree_items(self.tree)
        
        
    def update_title(self, title): self.titulo.configure(text=title)

    def sel_iid(self): return [int(i) for i in self.tree.selection()[0].split()]
        
    def Exe_bt_disable(self):self.bt_exe.config(state='disable')

    def Exe_bt_enable(self):self.bt_exe.config(state='normal')

    def Stop_bt_disable(self):self.bt_stop.config(state='disable')

    def Stop_bt_enable(self):self.bt_stop.config(state='normal')

    def get_tree(self): return self.tree
    
if __name__ == "__main__":
    x=tk.Tk()
   # s=protocol_map(x)
    x.mainloop()