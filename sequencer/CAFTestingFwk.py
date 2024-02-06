
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

class test_global:
   def __init__(self,protocol_name,protocol_code):
      self.protocol_name = protocol_name
      self.protocol_code = protocol_code
      self.test_suites = []
      self.log = ""

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
   
      for ts in self.test_suites:
         ts.title()
         ts.execute()
         self.log=self.log+ts.get_log()
      
   def get_log(self):
      return self.log
   
   def write_log(self,out_file="Test_Suite.txt",makefile=True):
         with open(out_file,'w') as file:
            file.write(self.log)
            file.close()


################################################################### Test Suite definitions ##################################################################

class test_suite:
   def __init__(self,suite_name,suite_id):
      self.id=suite_id
      self.name=suite_name
      self.log_content=""
      self.test_cases=[]


   def title(self):
      
      log=( "\n========================================= Test Suite "+ self.id +"=========================================="
      +"\n=="
      +"\n==      Title : "+ self.name 
      +"\n==")

      print(log)
      self.log_content=self.log_content+log

   def execute(self):
      log=""
      for tc in self.test_cases:
         tc.title()
         tc.initial_conditions()
         tc.execute()
         log=log+tc.get_log()
      self.log_content=log
   
   def get_log(self):
      return self.log_content
   
   def add_test_case(self,test_case):
      self.test_cases.append(test_case)

   def write_log(self,out_file="Test_Suite.txt",makefile=True):
      with open(out_file,'w') as file:
         file.write(self.log_content)
         file.close()



################################################################### Test Cases definitions ##################################################################

class test_case:
   def __init__(self,Case_name, Initial_conditions, case_description,case_id):
    self.log_content=""
    self.test_steps=[]
    self.name=Case_name
    self.id=case_id
    self.description=case_description
    self.Initial_Conditions=Initial_conditions

   def get_name(self):
       return self.name
   
   def execute(self):
      for ts in self.test_steps:
         ts.execute()
         self.log_content+ts.get_log()
   
   def title(self):
      log=( "==================================== Test Case "+self.id+" ===================================="
            +"\n=="
            +"\n==       Title : "+self.name
            +"\n==       Description : """+self.description
            +"\n==")
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

   def write_log(self,out_file="Test_Case.txt",makefile=True):
      with open(out_file,'w') as file:
         file.write(self.log)
         file.close()
   
   def get_log(self):
      return self.log_content
   

################################################################### Test Steps definitions ##################################################################

class test_step:
   def __init__(self,step_id,name):
      self.id=step_id
      self.name=name
      self.log=""
      self.test_actions=[]

   def execute(self):
      for action in self.test_actions:
         action.execute()

   def get_log(self):
      return self.log  
    
   def add_test_action(self,test_action):
      self.test_actions.append(test_action)




################################################################### Test Action definitions ##################################################################

class test_action:
   def __init__(self,action_id,action_text,action_type): #,vdb_object
      self.log=""
      self.id=action_id
      self.action_text=action_text
      self.action_type=action_type
      self.variables=[{"variable":"","value":0,"max":0,"min":0,"device_name":""}]
      #self.vdb=vdb_object
   
   def execute(self):
      log=""
      if(self.action_type=="MFA"):
         log="\n"+self.action_text
         self.log=log
         print(log)
         input("Press enter when done...")
         
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
         

      elif(self.action_type=="MCA"):
         validation=""
         self.log="\n"+self.action_text
         print(self.action_text)
         while(validation!="si" and validation!="no"):
            validation=input("¿Está OK? (Si/No)")
            validation=validation.lower()

         
         if(validation=="no"):
               log=log+"\n"+self.action_text+"--------> NOK    Revise step "+str(self.id)
         else:
               log=log+"\n"+self.action_text+"--------> OK "+str(self.id)

         print(log)
         self.log=self.log+"\n"+log
         
   def get_log(self):
      return self.log
   
   def add_variables(self, variable, value, tolerance):
      var_data={"variable":variable,"value":value ,"min":variable-tolerance,"max":variable+tolerance,"device_name":"CCU"}
      self.variables.append(var_data)
