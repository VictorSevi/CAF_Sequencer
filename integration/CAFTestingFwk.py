
#import logging
#from settings import *
#from glaciation.helper import mainTest
#import glaciation.testing.generic as tgf
#from glaciation.cdu.api import CduAPIWrapper
#from glaciation.cdu.vardb import VardbVarWrapper

######################################################## Test Frame definition ####################################
#class test_frame:
#   def __init__(self,protocol_codes):
#      log=""
#      self.protocol_codes=protocol_codes
#      self.protocol_list=[]
#
#   def execute(self):
#      for c in self.protocol_codes:
#         for x in self.protocol_list:
#            if c==x.get_code():
#                  x.execute()
############################################################# Test frame definition ############################################################################
import tkinter as tk
from tkinter import messagebox

from time import time
from time import strftime
from time import localtime

class protocol:
   def __init__(self,protocol_name,test_global,tester_name="",tester_chapa=""):
      self.protocol_name = protocol_name
      self.protocol_version = test_global
      self.test_suites = []
      self.log = ""
      self.tester_name =tester_name
      self.tester_chapa =tester_chapa
      self.start_time=time()
      self.end_time=time()

   def add_test_suite(self, test_suite):
      self.test_suites.append(test_suite)

   def title(self):
      log=("""*******************************************************************************************************,
      ***                                                                                                 ***,
      ***                           """+self.protocol_name+"""                                            ***,
      ***                           """+self.protocol_code+"""                                            ***,
      ***                                                                                                 ***,
      *******************************************************************************************************,
      """)
      print(log)

   def execute(self):
      
      while self.tester_name=="":
         self.tester_name=input("Name :")
      while self.tester_chapa=="":
         self.tester_chapa=input("Chapa : ")
      for ts in self.test_suites:
         ts.title()
         ts.execute()
         self.log=self.log+ts.get_log()
      self.end_time=time()

   def get_log(self):
      return self.log
   
   def write_log(self,out_file="Test_Suite.txt",makefile=True):
         with open(out_file,'w') as file:
            file.write(self.log)
            file.close()
   
   def get_result_json(self):
      protocol_struct={
         "Run":1,
         "Protocol_edition":self.protocol_version,
         "Sequencer Version":"1.0.0",
         "Protocol_name":self.protocol_name,
         "Performer_name":self.tester_name,
         "Performer_chapa":self.tester_chapa,
         "Execution":strftime("%a, %d %b %Y %H:%M:%S",localtime(time())),
         "Time_spent":self.execution_time(),
         "Used Items":"NS 1234567890, Calibration date: 10/01/2022, Fluke Model 31-B, Code: C10.1.2.3.4",
         "Test_Suites":[ts.get_result_json() for ts in self.test_suites]
      }
      return protocol_struct
   
   def execution_time(self):
      time_secs=self.end_time-self.start_time
      h=int(time_secs/36000)
      m=int(time_secs/60)-h*60
      s=int(time_secs)-h*3600-m*60
      return str(h)+"h "+str(m)+"mins "+str(s)+"s"

   def execute_by_id(self,suite_index,case_index=-1,step_index=-1):
      if(case_index==-1):
         self.test_suites[suite_index].execute()
      else:
         self.test_suites[suite_index].execute_by_id(case_index,step_index)

   def x(self):
      print("xnmn")




################################################################### Test Suite definitions ##################################################################

class test_suite:
   def __init__(self,suite_name,suite_id):
      self.id=suite_id
      self.name=suite_name
      self.log_content=""
      self.test_cases=[]
      self.start_time=time()
      self.end_time=time()
      self.result_list=[]
      self.global_result="NE"

   def title(self):
      
      log=( "\n========================================= Test Suite "+ self.id +"=========================================="
      +"\n=="
      +"\n==      Title : "+ self.name.splitlines()[0]+"\n==")
   
      print(log)
      self.log_content=self.log_content+log

   def execute(self,makefile=0):
      self.start_time=time()
      log=""
      for tc in self.test_cases:
         tc.title()
         tc.initial_conditions()
         tc.execute()
         log=log+tc.get_log()
         self.result_list.append(tc.get_result())
      self.log_content=log
      self.end_time=time()
      self.global_result="NOK" if "NOK" in self.result_list else "OK"
   
   def get_log(self):
      return self.log_content
   
   def add_test_case(self,test_case):
      self.test_cases.append(test_case)

   def write_log(self,out_file="Test_Suite.txt"):
      with open(out_file,'w') as file:
         file.write(self.log_content)
         file.close()

   def get_log(self):
      return self.log_content
   
   def get_result(self):
      return self.global_result
   
   def get_result_json(self):
      suite_struct={
         "Suite_id":self.id,
         "result":self.global_result,
         "Test_Cases":[tc.get_result_json() for tc in self.test_cases]
      }
      return suite_struct

   def execute_by_id(self,case_index,step_index):
      if(step_index==-1):
         self.test_cases[case_index].execute()
      else:
         self.test_cases[case_index].execute_by_id(step_index)


################################################################### Test Cases definitions ##################################################################

class test_case:
   def __init__(self,Case_name, Initial_conditions, case_description,case_id):
    self.log_content=""
    self.test_steps=[]
    self.name=Case_name
    self.id=case_id
    self.description=case_description
    self.Initial_Conditions=Initial_conditions
    self.start_time=time()
    self.end_time=time()
    self.csv_results_path=""
    self.result_list=[]
    self.global_result="NE"


   def get_name(self):
       return self.name
   
   def execute(self):
      self.start_time=time()
      for ts in self.test_steps:
         ts.execute()
         self.log_content=self.log_content+ts.get_log()
         self.result_list.append(ts.get_result())
      self.end_time=time()
      self.global_result="NOK" if "NOK" in self.result_list else "OK"

   
   def title(self):
      log=( "==================================== Test Case "+self.id+" ===================================="
            +"\n=="
            +"\n==       Title : "+self.name
            +"\n==       Description : """+self.description.splitlines()[0])
      
      for lines in self.description.splitlines()[1:]:
         log=log+"\n==                     "+lines

      log=log+"\n==       Time : "+strftime("%a, %d %b %Y %H:%M:%S", localtime(time()))
      log=log+"\n=="
      
      print(log)
      self.log_content=self.log_content+log
   
   def initial_conditions(self):
      log="==  Asegurar las siguientes condiciones: \n=="

      for x in self.Initial_Conditions:
         log=log+"\n==        >"+x

      log=log+"\n=="
      print(log)
      input("== Pulse enter una vez comprobadas estas condiciones...\n==")
      print("====== Comenzamos el Test:========================================================")
      log=log+"\n ==== Comenzamos el Test: =========================================================="
      return log
   
   def add_test_step(self,test_step):
      self.test_steps.append(test_step)

   def write_log(self,out_file="Test_Case.txt"):
      with open(out_file,'w') as file:
         file.write(self.log)
         file.close()
   
   def get_log(self):
      return self.log_content
   
   def get_result(self):
      return self.global_result
   
   def get_result_json(self): 
      case_struct={ 
         "Case_id":self.id,
         "result":self.global_result,
         "Test_Steps":[ts.get_result_json() for ts in self.test_steps]
      }
      return case_struct

   def execute_by_id(self,step_index):
      self.test_steps[step_index].execute()
################################################################### Test Steps definitions ##################################################################

class test_step:
   def __init__(self,step_id,name):
      self.id=step_id
      self.name=name
      self.log=""
      self.test_actions=[]
      self.start_time=time()
      self.end_time=time()
      self.result_list=[]
      self.global_result="NE"

   def execute(self):
      self.start_time=time()
      for action in self.test_actions:
         action.visualice()
      for action in self.test_actions:
         action.execute()
         if(action.action_type=="ACA" or action.action_type=="MCA"):
            self.result_list.append(action.get_result())
      self.end_time=time()
      self.global_result="NOK" if "NOK" in self.result_list else "OK"

   def get_log(self):
      return self.log  
    
   def add_test_action(self,test_action):
      self.test_actions.append(test_action)

   def get_result_list(self):
      return self.result_list
   
   def get_result(self):
      return self.global_result

   def get_result_json(self):

      step_struct={ 
         "Step_id":self.id,
         "result":self.global_result,
         "Test_Actions":self.result_list
      }
      return step_struct


################################################################### Test Action definitions ##################################################################

class test_action:
   def __init__(self,action_id,action_text,action_type,tkinter_o,cmd=True): #,vdb_object
      self.frame_loc=tkinter_o
      self.log=""
      self.id=action_id
      self.action_text=action_text
      self.action_type=action_type
      self.variables=[{"variable":"","value":0,"max":0,"min":0,"device_name":""}]
      self.global_result="NE"
      self.cmd=cmd
      #self.frame_loc=frame_place
      self.row=0
      self.executed=False
      #self.vdb=vdb_object
   def visualice(self):
      # Crear etiquetas y cuadros de entrada
      if(self.action_type=="MFA"):
         self.frame_place=tk.Frame(self.frame_loc, borderwidth=2, relief="solid", pady=5,padx=5, bg="white")
         self.frame_place.pack(fill=tk.BOTH, expand=True)
         self.frame_place.columnconfigure(0, weight=10)
         self.frame_place.columnconfigure(1, weight=1)
         self.frame_place.rowconfigure(0, weight=1 )
         order_text = tk.Label(self.frame_place, text=self.action_text,pady=50, font=("Arial",15))
         order_text.grid(row=self.row, column=0)
         #order_text.pack( 
         self.boton_OK = tk.Button(self.frame_place, text="Done",width=8,height=2,pady=50,command=self.next_act)
         self.boton_OK.grid(row=self.row, column=1)
         self.boton_OK.config(state="disabled")
         #boton_OK.pack(   
      elif(self.action_type=="MCA"):
         self.frame_place=tk.Frame(self.frame_loc,borderwidth=2, relief="solid", pady=5,padx=5, bg="white")
         self.frame_place.pack(fill=tk.BOTH, expand=True)
         self.frame_place.columnconfigure(0, weight=8)
         self.frame_place.columnconfigure(1, weight=1)
         self.frame_place.columnconfigure(2, weight=1)
         self.frame_place.rowconfigure(0, weight=1 )
         order_text = tk.Label(self.frame_place, text=self.action_text,pady=50,font=("Arial",15))
         order_text.grid(row=self.row, column=0)
         #order_text.pack( 
         self.boton_OK = tk.Button(self.frame_place, text="OK",width=8,height=2,pady=50,command=self.set_ok,bg="green")
         self.boton_OK.grid(row=self.row, column=1)
         self.boton_OK.config(state="disabled")
         #boton_OK.pack(   
         self.boton_NOK = tk.Button(self.frame_place, text="NOK",width=8,height=2,pady=50,command=self.set_nok,bg="red")
         self.boton_NOK.grid(row=self.row, column=2)
         self.boton_OK.config(state="disabled")
         #boton_OK.pack()



   def execute(self):
      if self.cmd:
         log="\n"
         if(self.action_type=="MFA"):
            log=log+"\n"+self.action_text
            #self.log=log
            print(log)
            input("Press enter when done...")
         elif(self.action_type=="MCA"):
            validation=""
            log="\n"+self.action_text
            print(log)
            while(validation!="si" and validation!="no"):
               validation=input("\n¿Está OK? (Si/No)")
               validation=validation.lower()


            if(validation=="no"):
                  log=log+"--------> NOK    Revise step "+str(self.id)+" "+strftime("%a, %d %b %Y %H:%M:%S", localtime(time()))+"\n"
                  self.global_result="NOK"
            else:
                  log=log+"--------> OK "+str(self.id)+" "+strftime("%a, %d %b %Y %H:%M:%S", localtime(time()))+"\n"
                  self.global_result="OK"

            print(log)
            self.log=self.log+log
      else:
         self.button_not_pressed=True
         if(self.action_type=="MFA"):
            self.boton_OK.config(state="normal")
            while(self.button_not_pressed):
               pass

         elif(self.action_type=="MCA"):
            self.boton_OK(state="normal")
            self.boton_NOK.config(state="normal")
            while(self.button_not_pressed):
               pass


            
   def get_end(self):
      return self.executed

   def set_ok(self):
      self.global_result="OK"
      self.frame_place.destroy()
      self.executed=True
      self.button_not_pressed=False

   def set_nok(self):
      self.global_result="NOK"
      self.frame_place.destroy()
      self.executed=True
      self.button_not_pressed=False

   def next_act(self):
      self.frame_place.destroy()
      self.executed=True
      self.button_not_pressed=False
   
   def get_log(self):
      return self.log
   
   def add_variables(self, variable, value, tolerance):
      var_data={"variable":variable,"value":value ,"min":variable-tolerance,"max":variable+tolerance,"device_name":"CCU"}
      self.variables.append(var_data)
      
   def get_result(self):
      return self.global_result
   



         #elif(self.action_type=="ACA"):
      #   self.log="\n"+self.action_text
      #   print()
      #   for var in self.variables:
      #      try:
      #         var_read=self.vdb.readVar(var["device_name"], var["variable"])
      #      except:
      #         log=log+"\n could not read variable: "+var["variable"]+" from "+var["device_name"]
      #      
      #      if((var_read<var["min"] or var_read>var["max"]) and var_read!=var["value"]):
      #         log=log+"\n"+var["variable"]+"--------> NOK    Revise step "+str(self.id)
      #      else:
      #         log=log+"\n"+var["variable"]+"--------> OK "+str(self.id)



#
#   print(log)
#   self.log=self.log+"\n"+log
#
#
#elif(self.action_type=="AFA"):
#   
#   self.log="\n"+self.action_text
#   print(self.action_text)
#   for var in self.variables:
#      try:
#         self.vdb.forceVar(var["device_name"], var["variable"])
#         log=log+"Variable forced succesfully: "+var["variable"]+" to "+var["device_name"]
#      except:
#         log=log+"\n could not force variable: "+var["variable"]+" in "+var["device_name"]
#   
#   print(log)
#   self.log=self.log+"\n"+log
   