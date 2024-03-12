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
from gui import gui as g


class app():
    def __init__(self):
        self.credentials={"Name":"", "Chapa":"", "UT":""}
        self.load_config()

    #se actualiza la configuracion 
    def load_config(self):
        with open('C:\\Users\\17940\\Python_Testing\\CAF_Sequencer\\config_file\\config_file.json', "r") as cfgfile:
            self.settings_obj=json.load(cfgfile)
        cfgfile.close()
        self.JSON_Templates=self.settings_obj["json_protocols"]
        self.JSON_Runs=self.settings_obj["json_runs"]
        
    #se obtiene el protocolo que se esta ejecutando (Modificar clase protocolo)
    def get_protocol(self): return self.protocol

    #ejecutar por idd TB DELETED revisar en 
    def execute_part(self,idd): self.protocol.execute_by_id(idd)
    


############# No van a hacer falta ##############################
    
    #se setea el lugar de ejecucion de las acciones (para acciones)
    def set_execution_loc(self,loc):self.loc=loc
    
    #se pasa una referencia al arbol del protocolo ejecutado. Eso vendrá de la clase pro   
    def set_tree(self,tree):self.tree=tree

    
    #se fija la accion a realizar cuando acaba la ejcución de la ultima accion de un step
    def set_action_execution_end(self,func): 
        self.exend=func

    #funcion a realizar cuando se acaba una ejecución
    def exend(self):a=1


############### Llamadas a pantallas ################################

    #se lanza pantalla principal
    def main_screen(self):
        self.gui=g(self.credentials)
        self.gui.get_botonera().config(load=self.load,config=self.config,create_json=self.create_json, help=self.help, info=self.info)
        self.gui.get_save_button().config(command=self.json_res)
        self.gui.main()

    #se lanza menu de inicio
    def sign_in_menu(self):
        s=sign_in_tab.sign_in()
        s.main()
        self.credentials=s.get_credentials()
        self.UT=self.credentials["UT"]
        return s.success()


############### Funciones llamda de botones ################################

    #tab de ayuda
    def help(self):
        os.system("C://Users//17940//Python_Testing//CAF_Sequencer//documentation//CAF_PRESENTACION_CORPORATIVA_CAST_2023_V_150PPP.pdf")

    #tab de configuracion
    def config(self):
        config_tab.config_tab().main()
        self.load_config()

    # SE abre la tab de info
    def info(self): 
        informative=info_tab.info_tab()
        informative.main()

    #para el import excel 
    def create_json(self):
        try:
            x_path=import_excel.load_file()
            objeto_protocolo=import_excel.parses_frame.protocol(import_excel.PARSER_VERSION,x_path)
            import_excel.parser(objeto_protocolo)
        except:
            messagebox.showerror("Error", "No se ha podido generar JSON!")
        else:
            messagebox.showinfo("Generado!", "Generado correctamente en Sandbox")
    
    #se hace cuando se carga un json de protocolo
    def load(self):
        filename=filedialog.askopenfilename(filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")), title="Select Excel File")
        self.json_file=json.load(open(filename))
        self.protocol=fwk.protocol(self.gui.get_execution_tab(),self.json_file,self.exend,UT=self.credentials["UT"],tester_name=self.credentials["Name"],tester_chapa=self.credentials["Chapa"])
        self.gui.get_mapa_contenido().update_title(self.protocol.get_name())
        self.protocol.tree_load(self.gui.get_mapa_contenido().get_tree())
        mapa=self.gui.get_mapa_contenido()
        mapa.bt_exe.config(command=lambda:self.protocol.execute_by_id(mapa.sel_iid()))

    #cuando se pulsa el boton save
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

    #se ejecuta para actualizar los resultados del arbol, lo mismo, TB DELETED
    def get_result_id(self,exe_idd):
        return self.protocol.get_result_byid(exe_idd)


if __name__ == "__main__":
    a=app()
    #if(a.sign_in_menu()):
    a.main_screen()
    #a.info()