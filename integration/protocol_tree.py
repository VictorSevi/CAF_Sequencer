import tkinter as tk
from tkinter import ttk

class protocol_map():
    def __init__(self,frame_place,execute_func, r=0, c=0):
        
        #marco del mapa de protocolo
        self.execute=execute_func
        self.frame = ttk.Frame(frame_place)
        self.frame.grid(row=r, column=c, sticky="nsew")
        self.frame.rowconfigure(0,weight=1)
        self.frame.rowconfigure(1,weight=30)
        self.frame.rowconfigure(2,weight=1)

        #se crea el arbol
        self.tree = ttk.Treeview(self.frame)
        self.tree.grid(row=1, column=0, sticky="nsew")

        #se crea el titulo del arbol
        self.titulo=ttk.Label(self.frame,text="No item selected")
        self.titulo.grid(row=0, column=0, sticky="nsew")

        #se crea el boton de ejecucion
        self.bt_exe = ttk.Button(self.frame, text="Execute",command=self.execute)
        self.bt_exe.grid(column=0,row=2)


    def update_content(self,protocol_object):

        for i,suite in enumerate(protocol_object["Test_Suites"]):
            item = self.tree.insert("", tk.END, text=suite["name"],iid=(i,-1,-1))
            for j,case in enumerate(suite["Test_Cases"]):
                subitem = self.tree.insert(item, tk.END, text=case["name"],iid=(i,j,-1))
                for k,step in enumerate(case["test_steps"]):
                    self.tree.insert(subitem, tk.END, text=step["id"],iid=(i,j,k)) 
        
        # Actualizar protocolo
        self.titulo.configure(text=protocol_object["Protocol_name"])

    def get_selection(self):
        return self.tree.selection()
    

def exe():
    print("execute button")

 
if __name__ == "__main__":
    x=tk.Tk()
    s=protocol_map(x,exe)
    x.mainloop()

