import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import CAFTestingFwk as fwk
import sign_in_menu
import parser_to_json
import protocol_tree


prt=fwk.protocol("","")

class app():
    def __init__(self):
        self.credentials={"Name":"", "Chapa":""}
        self.protocol=fwk.protocol("","")

    def upload_json(self,json_file):
        
        self.protocol=fwk.protocol(json_file["Protocol_name"],json_file["Protocol_edition"])
        for suite in json_file["Test_Suites"]:
            test_suite=fwk.test_suite(suite["name"],suite["id"])
            for case in suite["Test_Cases"]:
                test_case = fwk.test_case(case["name"],case["initial_conditions"],case["description"],str(case["id"]))
                for step in case["test_steps"]:
                    test_step = fwk.test_step(step["id"],"xxx")   
                    for index,action in enumerate(step["test_actions"]):
                        test_action = fwk.test_action(step["id"],action["text"],action["type"],cmd=True,row=index)
                        test_step.add_test_action(test_action)
                    test_case.add_test_step(test_step)
                test_suite.add_test_case(test_case)
            self.protocol.add_test_suite(test_suite)
    
    def execute_part(self,i,j,k):
        self.protocol.execute_by_id(0,0,0)

    def set_credentials(self,name, chapa):
        self.credentials={"Name":name, "Chapa":chapa}
    
    def get_credentials(self):
        return self.credentials


class gui():
    def __init__(self,master, running_app):
        
        self.app=running_app
        self.master=master
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

        self.mapa_contenido = protocol_tree.protocol_map(self.frame,self.execute_iid)
        #self.frme_note=ttk.Frame(self.frame)
        #self.frme_note.grid(row=0,column=1)
        #self.vista_general = general_view(self.frame)

        # Crear un Notebook (pestañas)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=0,column=1, sticky="nsew")

        # Pestaña 1
        tab1 = tk.Frame(self.notebook)
        self.notebook.add(tab1, text="Status")

        # Pestaña 2
        tab2 = tk.Frame(self.notebook)
        self.notebook.add(tab2, text="Execution")

        
        #self.descripcion = tk.Label(self.frame,text="Texto de ejemplo", bg="white")
        #self.descripcion.grid(row=0, column=1, sticky="nsew")

        #Frame informativo inferior
        self.info_frame = ttk.Frame(self.global_frame)
        self.info_frame.grid(row=2,column=0,sticky="nsew")
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=1)


        #etiquetas del frame informativo

        self.label_version = ttk.Label(self.info_frame,anchor="w", text="v0.0.0")
        self.label_version.grid(row=0,column=0, sticky="nsew")

        self.label_protocol = ttk.Label(self.info_frame,anchor="center", text="Chapa: "+str(self.app.get_credentials().get("Chapa"))+"  Name: "+str(self.app.get_credentials().get("Name")))
        self.label_protocol.grid(row=0,column=1, sticky="nsew")

        self.label_info= ttk.Label(self.info_frame,anchor="e", text="CAF-2024")
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
        parser_to_json.parser()
    def load(self):
        filename=filedialog.askopenfilename(filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")), title="Select Excel File")
        self.json_file=json.load(open(filename))
        self.mapa_contenido.update_content(self.json_file)
        self.app.upload_json(self.json_file)
    
    def get_frame(self):
        return self.frame
    
    def execute_iid(self):
        id=self.mapa_contenido.get_selection()[0]
        print(len(id))
        self.app.execute_part(int(id[0]),int(id[2]),int(id[4]))
        


        
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
    #app = gui(root)
    #root.mainloop()
    root1 = tk.Tk()
    a=app()
    m=sign_in_menu.sign_in(root1,a)
    root1.mainloop()

    if(m.passed()):
        root2= tk.Tk()
        g=gui(root2,a)
        root2.mainloop()

if __name__ == "__main__":
    main()