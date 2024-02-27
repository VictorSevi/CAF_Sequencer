import json
import tkinter as tk
from tkinter import filedialog
import os
import CAFTestingFwk as fwk
import import_excel
from time import localtime
from time import time
from time import strftime
import os


class app():
    def __init__(self):
        self.credentials={"Name":"", "Chapa":""}

    def upload_json(self):
        self.protocol=fwk.protocol(self.loc,self.json_file,self.exend)
        self.protocol.tree_load(self.tree)
        self.UT=2
    
    def set_action_execution_end(self,func): self.exend=func

    def get_protocol(self): return self.protocol

    def execute_part(self,idd): self.protocol.execute_by_id(idd)
        
    def set_credentials(self,name, chapa): self.credentials={"Name":name, "Chapa":chapa}
        
    def get_credentials(self):return self.credentials

    def set_execution_loc(self,loc):self.loc=loc
    
    def help(self):os.system("C://Users//17940//Python_Testing//CAF_Sequencer//documentation//CAF_PRESENTACION_CORPORATIVA_CAST_2023_V_150PPP.pdf")

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
    
    def load(self):
        filename=filedialog.askopenfilename(filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")), title="Select Excel File")
        self.json_file=json.load(open(filename))
        self.upload_json()

    def json_res(self):
        fecha=strftime("%a %d %b %Y %H-%M-%S",localtime(time()))
        self.sandbox="C:\\Users\\17940\\Python_Testing\\CAF_Sequencer\\Executions"
        self.folder_structure="UT"+str(self.UT)+ "\\"+self.protocol.get_name().strip()
        folder_path=os.path.join(self.sandbox,self.folder_structure)
        name_template='RUN_'+self.protocol.get_code()+fecha+'.json'
        
        if not os.path.exists(folder_path):os.makedirs(folder_path)
            
        with open(os.path.join(folder_path,name_template), "w") as outfile:
            json.dump(self.protocol.get_result_json(), outfile, indent = 4)
#"RUN_"+self.protocol.get_code()+ fecha
    def set_tree(self,tree):self.tree=tree

    def get_result_id(self,exe_idd):return self.protocol.get_result_byid(exe_idd)


