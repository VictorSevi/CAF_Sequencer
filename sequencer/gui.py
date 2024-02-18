import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class TreeViewWithTextWindow:
    def __init__(self, master):
        self.master = master
        self.json_file=""
        self.master.title("CAF Secuenciador") 
        self.master.geometry("1100x550")
        self.master.iconbitmap("caf_icon.ico")

        self.global_frame=ttk.Frame(self.master)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=1)
        self.global_frame.rowconfigure(1, weight=20, minsize=400)
        self.global_frame.rowconfigure(2, weight=1)
        self.global_frame.columnconfigure(0, weight=1)

        #Frame de botones
        self.bt_frame = ttk.Frame(self.global_frame)
        self.bt_frame.grid(row=0, sticky="nsew")
        self.bt_load = ttk.Button(self.bt_frame, text="Load",command=self.load)
        self.bt_load.grid(column=0,row=0)
        self.bt_help = ttk.Button(self.bt_frame, text="Help",command=self.help)
        self.bt_help.grid(column=3,row=0)
        self.bt_config = ttk.Button(self.bt_frame, text="Config",command=self.config)
        self.bt_config.grid(column=1,row=0)
        self.bt_info = ttk.Button(self.bt_frame, text="Info",command=self.info)
        self.bt_info.grid(column=2,row=0)


        # Frame principal
        self.frame = ttk.Frame(self.global_frame)
        self.frame.grid(row=1, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=10)

        with open('D0000006245_Propulsion Management Functional Factory Type Test.json') as test_json:
            protocol_object=json.load(test_json)
        test_json.close()

        
        self.tree = ttk.Treeview(self.frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        for suite in protocol_object["Test_Suites"]:
            item = self.tree.insert("", tk.END, text=suite["name"])
            for case in suite["Test_Cases"]:
                subitem = self.tree.insert(item, tk.END, text=case["name"])
                for step in case["test_steps"]:
                    self.tree.insert(subitem, tk.END, text=step["id"]) 
        # Crear el área de texto
        self.descripcion = tk.Label(self.frame,text="Texto de ejemplo", bg="white")
        self.descripcion.grid(row=0, column=1, sticky="nsew")



        #Frame informativo inferior
        self.info_frame = ttk.Frame(self.global_frame)
        self.info_frame.grid(row=2,column=0,sticky="nsew")
        self.info_frame.columnconfigure(0, minsize=100)
        self.info_frame.columnconfigure(1, minsize=400)
        self.info_frame.columnconfigure(2, minsize=100)


        #etiquetas del frame informativo

        self.label_version = ttk.Label(self.info_frame, text="v0.0.0")
        self.label_version.grid(row=0,column=0, sticky="nsew")

        self.label_protocol = ttk.Label(self.info_frame, text="D0000006245_Propulsion Management Functional Factory Type Test")
        self.label_protocol.grid(row=0,column=1, sticky="nsew")

        self.label_info= ttk.Label(self.info_frame, text="CAF-2024")
        self.label_info.grid(row=0,column=2, sticky="nsew")
    def load(self):
        self.json_file=filedialog.askopenfilename(filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")), title="Select Excel File")
    
    def help(self):
        a=tk.Tk()
        message=tk.Message(a, text="la ayuda se encuentra a tomar viento")
        message.pack()
    def config(self):
        b=tk.Tk()
        message=tk.Message(b, text="la configurasao")
        message.pack()
    def info(self):
        c=tk.Tk()
        message=tk.Message(c, text="Hecho por el vity")
        message.pack()



def main():
    root = tk.Tk()
    app = TreeViewWithTextWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()