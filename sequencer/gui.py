import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import CAFTestingFwk as fwk


prt=fwk.protocol("","")



class gui():
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

        #self.botonera = botonera_superior(self.global_frame)

        #botonera
        self.bt_frame = ttk.Frame(self.global_frame)
        self.bt_frame.grid(row=0, sticky="nsew")

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



        # Frame principal
        self.frame = ttk.Frame(self.global_frame)
        self.frame.grid(row=1, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=10)

        self.mapa_contenido = protocol_map(self.frame)
        self.frme_pruebaaaa=ttk.Frame(self.frame)
        self.frme_pruebaaaa.grid(row=0,column=1)
        #self.vista_general = general_view(self.frame)

        
        #self.descripcion = tk.Label(self.frame,text="Texto de ejemplo", bg="white")
        #self.descripcion.grid(row=0, column=1, sticky="nsew")

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

    def help(self):
        os.system("C://Users//17940//Python_Testing//CAF_Sequencer//documentation//CAF_PRESENTACION_CORPORATIVA_CAST_2023_V_150PPP.pdf")
    #TBD
    def config(self):
        b=tk.Tk()
        message=tk.Message(b, text="la configurasao")
        b.geometry("300x200")
        message.pack(pady=50)
        message.config(aspect=10,width=200)
    #TBD
    def info(self):
        c=tk.Tk()
        message=tk.Message(c, text="Hecho por el vity")
        message.config(aspect=10)
        c.geometry("300x200")
        message.pack()
    #TBD
    def create_json(self):
        c=tk.Tk()
        message=tk.Message(c, text="Aqui va la wea de crear jsons")
        message.config(aspect=1)
        c.geometry("300x200")
        message.pack()
    def load(self):
        filename=filedialog.askopenfilename(filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")), title="Select Excel File")
        self.json_file=json.load(open(filename))
        self.mapa_contenido.update_content(self.json_file)

        protocol=fwk.protocol(self.json_file["Protocol_name"],self.json_file["Protocol_edition"])

        for suite in self.json_file["Test_Suites"]:
            test_suite=fwk.test_suite(suite["name"],suite["id"])
            for case in suite["Test_Cases"]:
                test_case = fwk.test_case(case["name"],case["initial_conditions"],case["description"],str(case["id"]))
                for step in case["test_steps"]:
                    test_step = fwk.test_step(step["id"],"xxx")   
                    for index,action in enumerate(step["test_actions"]):
                        test_action = fwk.test_action(step["id"],action["text"],action["type"],self.frme_pruebaaaa,cmd=False,row=index)
                        test_step.add_test_action(test_action)
                    test_case.add_test_step(test_step)
                test_suite.add_test_case(test_case)
            protocol.add_test_suite(test_suite)
        prt=protocol
        


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

        #se crea el titulo del arbol
        self.titulo=ttk.Label(self.frame,text="No item selected")
        self.titulo.grid(row=0, column=0, sticky="nsew")

        #se crea el boton de ejecucion
        self.bt_exe = ttk.Button(self.frame, text="Execute",command=self.execute)
        self.bt_exe.grid(column=0,row=2)


    def update_content(self,protocol_object):
        #with open('D0000006245_Propulsion Management Functional Factory Type Test.json') as test_json:
        #    protocol_object=json.load(test_json)
        #test_json.close()

        # Actualizar arbol
        
        for i,suite in enumerate(protocol_object["Test_Suites"]):
            item = self.tree.insert("", tk.END, text=suite["name"],iid=(i,-1,-1))
            for j,case in enumerate(suite["Test_Cases"]):
                subitem = self.tree.insert(item, tk.END, text=case["name"],iid=(i,j,-1))
                for k,step in enumerate(case["test_steps"]):
                    self.tree.insert(subitem, tk.END, text=step["id"],iid=(i,j,k)) 
        
        # Actualizar protocolo
        self.titulo.configure(text=protocol_object["Protocol_name"])

    
    def execute(self):
        id=self.tree.selection()[0]
        print(len(id))
        protocol.execute_by_id(int(id[0]),int(id[2]),int(id[4]))
        


#class general_view:
#    def __init__(self, frame_place, r=0, c=1):
#        #se crea el titulo del arbol
#        self.titulo=ttk.Frame(frame_place)
#        self.titulo.grid(row=r, column=c, sticky="nsew")
#        #protocol.execute()

class botonera_superior():
    def __init__(self,frame_place, r=0, c=0):
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

def main():
    #root = tk.Tk()
    #app = gui(root)
    #root.mainloop()
    m=tk.Tk()
    s=sing_in(m)
    m.mainloop()

if __name__ == "__main__":
    main()