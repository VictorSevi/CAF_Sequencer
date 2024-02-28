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
import config_tab
import info_tab
import sign_in_tab
from tkinter import messagebox


class app():
    def __init__(self):
        self.credentials={"Name":"", "Chapa":"", "UT":""}
        self.load_config()

    def upload_json(self):
        self.protocol=fwk.protocol(self.loc,self.json_file,self.exend,UT=self.credentials["UT"])
        self.protocol.tree_load(self.tree)
    
    def load_config(self):
        with open('C:\\Users\\17940\\Python_Testing\\CAF_Sequencer\\config_file\\config_file.json', "r") as cfgfile:
            settings_obj=json.load(cfgfile)
        cfgfile.close()
        self.JSON_Templates=settings_obj["json_protocols"]
        self.JSON_Runs=settings_obj["json_runs"]
        

    def set_action_execution_end(self,func): self.exend=func

    def sign_in_menu(self):
        s=sign_in_tab.sign_in()
        s.main()
        self.credentials=s.get_credentials()
        self.UT=self.credentials["UT"]
        return s.success()

    def get_protocol(self): return self.protocol

    def execute_part(self,idd): self.protocol.execute_by_id(idd)
        
    def get_credentials(self):return self.credentials

    def set_execution_loc(self,loc):self.loc=loc
    
    def help(self):os.system("C://Users//17940//Python_Testing//CAF_Sequencer//documentation//CAF_PRESENTACION_CORPORATIVA_CAST_2023_V_150PPP.pdf")

    def config(self):
        cfg_tab = config_tab.config_tab()
        cfg_tab.main()
        self.load_config()

    def info(self):
        inf=info_tab.info_tab()
        inf.main()
        
    def create_json(self):
        try:
            x_path=import_excel.load_file()
            objeto_protocolo=import_excel.parses_frame.protocol(import_excel.PARSER_VERSION,x_path)
            import_excel.parser(objeto_protocolo)
        except:
            messagebox.showerror("Error", "No se ha podido generar JSON!")
        else:
            messagebox.showinfo("Generado!", "Generado correctamente en Sandbox")
    
    def load(self):
        filename=filedialog.askopenfilename(filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")), title="Select Excel File")
        self.json_file=json.load(open(filename))
        self.upload_json()

    def json_res(self):
        try:
            fecha=strftime("%a %d %b %Y %H-%M-%S",localtime(time()))
            folder_structure="UT"+str(self.credentials["UT"])+ "\\"+self.protocol.get_name().strip()

            folder_path=os.path.join(self.JSON_Runs,folder_structure)
            name_template='RUN_'+self.protocol.get_code()+fecha+'.json'

            if not os.path.exists(folder_path):os.makedirs(folder_path)

            with open(os.path.join(folder_path,name_template), "w") as outfile:
                json.dump(self.protocol.get_result_json(), outfile, indent = 4)
        except:
            messagebox.showerror("Error", "No se ha podido guardar!")
        else:
            messagebox.showinfo("Guardado!", "Guardado correcto en Sandbox")
        

    def set_tree(self,tree):self.tree=tree

    def get_result_id(self,exe_idd):return self.protocol.get_result_byid(exe_idd)


if __name__ == "__main__":
    a=app()
    a.sign_in_menu()