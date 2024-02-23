import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import CAFTestingFwk as fwk
import sign_in_menu
import import_excel
import protocol_tree
import botonera


prt=fwk.protocol("","")

class app():
    def __init__(self):
        self.credentials={"Name":"", "Chapa":""}
        self.protocol=fwk.protocol("","")

    def upload_json(self):
        
        self.protocol=fwk.protocol(self.json_file["Protocol_name"],self.json_file["Protocol_edition"],tester_name=self.credentials["Name"],tester_chapa=self.credentials["Chapa"])
        for suite in self.json_file["Test_Suites"]:
            test_suite=fwk.test_suite(suite["name"],suite["id"])
            for case in suite["Test_Cases"]:
                test_case = fwk.test_case(case["name"],case["initial_conditions"],case["description"],str(case["id"]))
                for step in case["test_steps"]:
                    test_step = fwk.test_step(step["id"],"xxx")   
                    for index,action in enumerate(step["test_actions"]):
                        test_action = fwk.test_action(step["id"],action["text"],action["type"],self.loc,cmd=False)
                        test_step.add_test_action(test_action)
                    test_case.add_test_step(test_step)
                test_suite.add_test_case(test_case)
            self.protocol.add_test_suite(test_suite)
    
    def execute_part(self,i,j,k):
        self.protocol.execute_by_id(i,j,k)

    def set_credentials(self,name, chapa):
        self.credentials={"Name":name, "Chapa":chapa}
    
    def get_credentials(self):
        return self.credentials
    
    def set_execution_loc(self,loc):
        self.loc=loc
    
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
            x_path=import_excel.load_file()
            objeto_protocolo=import_excel.parses_frame.protocol(import_excel.PARSER_VERSION,x_path)
            import_excel.parser(objeto_protocolo)
            import_excel.generating_screen(objeto_protocolo.get_file_path())
    
    def load(self,json_file):
        self.json_file=json_file
        self.upload_json()

    def json_res(self):
        with open("C://Users//17940//Python_Testing//CAF_Sequencer//results//DO_prueba.json", "w") as outfile:
            json.dump(self.protocol.get_result_json(), outfile, indent = 4)


class gui():
    def __init__(self,master, running_app):
        
        #Main Window create
        self.app=running_app
        self.master=master
        self.json_file=""
        self.master.title("CAF Secuenciador") 
        self.master.geometry("1100x550")
        self.master.iconbitmap("caf_icon.ico")

        #Global frame  structure definition
        self.global_frame=ttk.Frame(self.master)
        self.global_frame.pack(fill=tk.BOTH, expand=True)
        self.global_frame.rowconfigure(0, weight=1)
        self.global_frame.rowconfigure(1, weight=20, minsize=400)
        self.global_frame.rowconfigure(2, weight=1)
        self.global_frame.columnconfigure(0, weight=1)

        self.botonera = botonera.botonera_superior(self.global_frame,
                                                   load_func=self.load,
                                                   help_func=self.app.help,
                                                   config_func=self.app.config,
                                                   info_func=self.app.info,
                                                   json_func=self.app.create_json)


        # Frame principal
        self.frame = ttk.Frame(self.global_frame)
        self.frame.grid(row=1, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=10)

        self.mapa_contenido = protocol_tree.protocol_map(self.frame,self.execute_iid)

        # Crear un Notebook (pestañas)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=0,column=1, sticky="nsew")

        # Pestaña 1
        tab1 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab1, text="Execution")
        self.app.set_execution_loc(tab1)

        # Pestaña 2
        tab2 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab2, text="Status")
        conectlab=tk.Label(tab2,text="No connections active!!", fg="red", font=("Arial",48),pady=150)
        conectlab.pack()

        
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

        bt=ttk.Button(self.info_frame,text="json",command=self.app.json_res)
        bt.grid(row=0,column=3, sticky="nsew")

    
    def get_frame(self):
        return self.frame
    
    def execute_iid(self):
        id=self.mapa_contenido.get_selection()[0]
        self.app.execute_part(int(id[0]),int(id[2]),int(id[4]))

    def load(self):
        filename=filedialog.askopenfilename(filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")), title="Select Excel File")
        self.json_file=json.load(open(filename))
        self.app.load(self.json_file)
        self.mapa_contenido.update_content(self.json_file)
        

def main():
    #root1 = tk.Tk()
    a=app()
    #m=sign_in_menu.sign_in(root1,a)
    #root1.mainloop()

    #if(m.passed()):
    root2= tk.Tk()
    g=gui(root2,a)
    root2.mainloop()

if __name__ == "__main__":
    main()

