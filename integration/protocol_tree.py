import tkinter as tk
from tkinter import ttk

class protocol_map():
    def __init__(self,frame_place,app, r=0, c=0):
        
        #marco del mapa de protocolo
        self.app=app
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

        #se crea el boton de ejecucion
        self.frame_buttons=ttk.Button()
        self.bt_exe = ttk.Button(self.frame, text="Execute",command=self.execute_iid)
        self.bt_exe.grid(column=0,row=2)

        # Estilos para los tags
        self.style = ttk.Style(self.frame)
        
        self.style.configure('ok_tag', foreground='green')
        self.style.configure('nok_tag', foreground='red')
        self.style.configure('ne_tag', foreground='black')

        self.tree.tag_configure("ok_tag", foreground="green")
        self.tree.tag_configure("nok_tag", foreground="red")
        self.tree.tag_configure("ne_tag", foreground="black")

        self.app.set_action_execution_end(self.eje)
        self.app.set_tree(self.tree)

    def eje(self):
        self.bt_exe.config(state='normal')
        self.app.get_protocol().update_result()
        res=self.app.get_result_id(self.exe_idd)
        self.tree.item(self.sel_id, values=(res))
        

    def update_content(self):
        # Actualizar protocolo
        self.app.get_protocol().tree_load(self.tree)
        self.titulo.configure(text=self.app.get_protocol().get_name())

    def execute_iid(self):
        self.sel_id=self.tree.selection()[0]
        self.exe_idd=[]
        for i in self.sel_id.split():
             self.exe_idd.append(int(i))
        self.app.execute_part(self.exe_idd)
        self.bt_exe.config(state='disable')

def exe():
    print("execute button")

 
if __name__ == "__main__":
    x=tk.Tk()
    s=protocol_map(x,exe)
    x.mainloop()

