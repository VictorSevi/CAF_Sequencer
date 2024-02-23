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
        self.bt_exe = ttk.Button(self.frame, text="Execute",command=self.execute)
        self.bt_exe.grid(column=0,row=2)

        # Estilos para los tags
        self.style = ttk.Style(self.frame)
        
        self.style.configure('ok_tag', foreground='green')
        self.style.configure('nok_tag', foreground='red')

        self.tree.tag_configure("ok_tag", foreground="green")
        self.tree.tag_configure("nok_tag", foreground="red")
        self.tree.tag_configure("ne_tag", foreground="black")


    def update_content(self,protocol_object):

        for i,suite in enumerate(protocol_object["Test_Suites"]):
            suite_tag=('ok_tag' if suite["result"]=="OK" else ('nok_tag' if suite["result"]=="NOK" else 'ne_tag'))
            item = self.tree.insert("", tk.END, text=suite["name"],iid=(i,-1,-1),values=(suite["result"]),tags=(suite_tag,))
            for j,case in enumerate(suite["Test_Cases"]):
                case_tag=('ok_tag' if case["result"]=="OK" else ('nok_tag' if case["result"]=="NOK" else 'ne_tag'))
                subitem = self.tree.insert(item, tk.END, text=case["id"],iid=(i,j,-1),values=(case["result"]),tags=(case_tag,))
                for k,step in enumerate(case["test_steps"]):
                    step_tag=('ok_tag' if step["result"]=="OK" else ('nok_tag' if step["result"]=="NOK" else 'ne_tag'))
                    self.tree.insert(subitem, tk.END, text=step["id"],iid=(i,j,k),values=(step["result"]),tags=(step_tag,)) 
        
        # Actualizar protocolo
        self.titulo.configure(text=protocol_object["Protocol_name"])

    def get_selection(self):
        return self.tree.selection()
    
    def update_item_status(self,idd,estado):
        self.tree.item(idd, values=(estado))

def exe():
    print("execute button")

 
if __name__ == "__main__":
    x=tk.Tk()
    s=protocol_map(x,exe)
    x.mainloop()

