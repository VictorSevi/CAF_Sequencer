#import app
import logging
from glaciation.helper import mainTest
import glaciation.testing.generic as tgf
from glaciation.cdu.api import CduAPIWrapper
from glaciation.cdu.vardb import VardbVarWrapper
import time
import tkinter as tk
import subprocess
from ping3 import ping


PROGNAME = "CCU_CP4"          # filled automaticaly if run from rqm
TESTER = "Victor Sevillano"     # filled automaticaly if run from rqm
LOG_FILE_PATH = "C://Users//17940//OneDrive - Construcciones y Auxiliar deFerrocarriles SA (CAF)//Escritorio//Monit_termicos//Reults//results.txt"      # filled automaticaly if run from rqm
DESCRIPTION = "Tests Zaragoza"                                                                                                                          #description_tests
JSON_FILE_NAME= "C://Users//17940//Python_Testing//CAF_Sequencer//config_file//variables.json"



class connections_tab:
    def __init__(self, notebook,ip):
        #self.app = app
        self.notebook=notebook
        self.ip=ip
        
        tab2 = tk.Frame(self.notebook,bg="#D3D3D3")
        tab2.pack(fill='both',anchor='nw',expand=True)
        
        tab2.rowconfigure(0, weight=1)
        tab2.rowconfigure(1, weight=3)
        tab2.rowconfigure(2, weight=3)
        tab2.columnconfigure(0, weight=1)

        conec_title=tk.Label(tab2,text="Connections", fg="black", font=("Arial",32),bg="#D3D3D3",pady=20, padx=20, anchor='w' )
        conec_title.grid(row=0, column=0,sticky="w")

        #Tabla Info #"#C42222"
        conect_content_fr=tk.Frame(tab2,bg="#D3D3D3", pady=10)
        conect_content_fr.grid(row=1, column=0,sticky="nwes")
        conect_content_fr.rowconfigure(0, weight=1)
        conect_content_fr.rowconfigure(1, weight=2)
        conect_content_fr.rowconfigure(2, weight=1)
        conect_content_fr.rowconfigure(3, weight=2)
        conect_content_fr.columnconfigure(0, weight=1)
        conect_content_fr.columnconfigure(1, weight=20)



        #primera fila
        data_label=tk.Label(conect_content_fr,text="Data:", fg="black", font=("Arial",16),bg="white", anchor='w',width=4, height=2,padx=10)
        data_label.grid(row=0, column=0,pady=2, ipady=10, padx=10,ipadx=10,sticky='nws')
        data_content=tk.Label(conect_content_fr,text="IP: 10.0.0.16     PORT: 10000         ", fg="black", font=("Arial",16),bg="white",height=2, anchor='w',padx=10)
        data_content.grid(row=0, column=1,pady=2, ipady=10,sticky='nw')

        #segunda fila
        device_label=tk.Label(conect_content_fr,text="Device:", fg="black", font=("Arial",16),bg="white", anchor='w',width=4, height=2,padx=10)
        device_label.grid(row=1, column=0,pady=2, ipady=10, padx=10,ipadx=10,sticky='nws')
        device_content=tk.Label(conect_content_fr,text="CCU_CP4         vars: variables_json", fg="black", font=("Arial",16),bg="white",height=2, anchor='w',padx=10)
        device_content.grid(row=1, column=1,pady=2, ipady=10,sticky='nw')


        conec_title=tk.Label(tab2,text="Controls", fg="black", font=("Arial",32),bg="#D3D3D3",pady=20, padx=20, anchor='w' )
        conec_title.grid(row=2, column=0,sticky="w")

        #vardb_but=tk.Button(conect_content_fr,text='Generate vardb')
        #vardb_but.grid(row=2, column=1,sticky='nsw')
        #connection_button and status
        conect_actions=tk.Frame(tab2,bg="#D3D3D3", pady=10)
        conect_actions.grid(row=3, column=0,sticky="nswe")
        conect_actions.rowconfigure(0, weight=1)
        conect_actions.rowconfigure(1, weight=1)
        conect_actions.columnconfigure(0, weight=1)
        conect_actions.columnconfigure(1, weight=1)

        boton_ping=tk.Button(conect_actions, text='Ping',font=("Arial",16),command=self.check_ping)
        boton_ping.grid(row=0,column=0,sticky='nswe', ipadx=20, ipady=20, pady=10,padx=40)
        boton_conex=tk.Button(conect_actions, text='Connection',font=("Arial",16), command=self.connect)
        boton_conex.grid(row=0,column=1,sticky='nswe', ipadx=20, ipady=20, pady=10,padx=40)
        self.pilot_conex=tk.Label(conect_actions, text='Status', bg='red', fg="black",font=("Arial",16))
        self.pilot_conex.grid(row=1,column=1,sticky='nswe', ipadx=20, ipady=20, pady=10,padx=40)
        self.pilot_ping=tk.Label(conect_actions, text='Ping', bg='red', fg="black",font=("Arial",16))
        self.pilot_ping.grid(row=1,column=0,sticky='nswe', ipadx=20, ipady=20, pady=10,padx=40)
        self.notebook.add(tab2, text="Connections")

    def check_ping(self):
        resp = ping(self.ip)
        if resp:    self.pilot_ping.config(bg="green")
        else:    self.pilot_ping.config(bg="red")

    def connect(self):
        try:
            cdu = CduAPIWrapper(JSON_FILE_NAME)
            cdu.runAll(retries=1)
            vdb = VardbVarWrapper(JSON_FILE_NAME)
            vdb.loadVars()
        
        except:
            self.pilot_conex.config(bg="red")

        else:
            self.pilot_conex.config(bg="green")



if __name__ == "__main__":
    wind=tk.Tk()
    connections_tab(wind,'10.0.0.16')
    wind.mainloop()







        
        




























@mainTest
def main():
    # Start all CDU sync and mon
    cdu = CduAPIWrapper(JSON_FILE_NAME)
    cdu.runAll(retries=1)

    # Connect to all vars using vardbvar
    vdb = VardbVarWrapper(JSON_FILE_NAME)
    vdb.loadVars()  
    # read vars
    #vdb.readVar("CCU_A","fwk_internal::TEMPERATURE")
    for i in range(10):
        x=vdb.readVar("CCU","PLC_TRAIN_LFW")
        print(x)
        time.sleep(2)
    #vdb.readVar("CCU_A","CduDiagnosis::CONF_Max_monitorization_sessions")
    # assert if 3 cdu sessions are available in CCU_P
    #tgf.checkParam(vdb, "CCU_CP4","CduDiagnosis::CONF_Max_monitorization_sessions",3)
    # wait until temperature is 32 in CCU_A
    #tgf.waitParam(vdb, "CCU_CP4", "fwk_internal::TEMPERATURE", 32)
    # force var HMI_PLC_CAB in HMI_MON
    #vdb.forceVar("HMI_MON","HMI_PLC_CAB",1)
    # Stop monitorizations and convert CompactReg file to csv

    #tgf.convertCompactRegToCsv("CompactReg_HMI", True)
    cdu.stopMon()


