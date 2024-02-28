
############################################################# Test frame definition ############################################################################
import tkinter as tk
from time import time
from time import strftime
from time import localtime
import FwkActions as actions




class test_struct:
    def __init__(self):
        self.items=[]
        self.items_array=[]
        self.content={}      
    def add(self,item):
        self.items_array.append(item.get_json_struct())
        self.items.append(item)
    def get_json_struct(self):
        return self.content


class protocol:
   def __init__(self,loc,json_file,func_fin_exe,tester_name="",tester_chapa="",UT=""):
      self.exend = func_fin_exe
      self.json_file=json_file
      self.protocol_name = self.json_file["Protocol_name"]
      self.protocol_version = self.json_file["Protocol_edition"]
      self.test_suites = []
      self.items_array=[]
      self.tester_name =tester_name
      self.tester_chapa =tester_chapa
      self.start_time=time()
      self.end_time=time()
      self.result='NE'
      self.loc=loc
      self.protocol_struct={
         "UT":UT,
         "Protocol_edition":self.protocol_version,
         "Parser_Version":"1.0.0",
         "Sequencer Version":"1.0.0",
         "Protocol_name":self.protocol_name,
         "Performer_name":self.tester_name,
         "Performer_chapa":self.tester_chapa,
         "Execution":strftime("%a, %d %b %Y %H:%M:%S",localtime(time())),
         "Time_spent":self.execution_time(),
         "Used Items":"NS 1234567890, Calibration date: 10/01/2022, Fluke Model 31-B, Code: C10.1.2.3.4",
         "result":self.result,
         "Test_Suites":self.items_array
      }
      
      
      for suite in self.json_file["Test_Suites"]:
          tsu=test_suite(suite["name"],suite["id"])
          for case in suite["Test_Cases"]:
              tc = test_case(case["name"],case["initial_conditions"],case["description"],str(case["id"]))
              for step in case["test_steps"]:
                  ts = test_step(step["id"])   
                  for index,action in enumerate(step["test_actions"]):
                      if action["type"]=='MFA':
                          ac_new=test_action = actions.MFA_test_action(self.loc,action["text"], row=index)
                      
                      elif action["type"]=='MCA':
                          ac_new=test_action = actions.MCA_test_action(self.loc,action["text"], row=index)
                      if not index==0: ac.set_next_acion(ac_new)
                      
                      ac=ac_new
                      ts.add_test_action(test_action)
                  ac.set_end_func(self.exend)
                  tc.add_test_step(ts)
              tsu.add_test_case(tc)
          self.add_test_suite(tsu)

   def add_test_suite(self, test_suite):
      self.items_array.append(test_suite.get_result_json())
      self.test_suites.append(test_suite)
   
   def get_result_json(self):return self.protocol_struct
   
   def execution_time(self):
      time_secs=self.end_time-self.start_time
      h=int(time_secs/36000)
      m=int(time_secs/60)-h*60
      s=int(time_secs)-h*3600-m*60
      return str(h)+"h "+str(m)+"mins "+str(s)+"s"

   def execute_by_id(self,idd): self.get_test_items(idd).execute()

   def get_result(self): return self.result

   def get_name(self):return self.protocol_name

   def get_code(self):return self.protocol_name[:11]

   def tree_load(self,tree):
      for item in tree.get_children():
         tree.delete(item)

      for i,suite in enumerate(self.test_suites):
         suite.tree_load(tree,i)
        
   def get_test_items(self, idd):
      if idd[1]==-1: return self.test_suites[idd[0]]
      else: return self.test_suites[idd[0]].get_test_items(idd)

   def get_result_byid(self,exe_idd): return self.get_test_items(exe_idd).get_result()

   def update_result(self):
      for items in self.test_suites:
         items.update_result()
      self.result_list = [suites.get_result() for suites in self.test_suites]
      if 'NOK' in self.result_list: self.result='NOK'
      elif 'NE' in self.result_list: self.result='NE'
      else: self.result='OK'
         

################################################################### Test Suite definitions ##################################################################

class test_suite:
   def __init__(self,suite_name,suite_id):
      self.id=suite_id
      self.name=suite_name
      self.test_cases=[]
      self.start_time=time()
      self.end_time=time()
      self.result_list=[]
      self.items_array=[]
      self.result="NE"
      self.suite_struct={
         "id":self.id,
         "result":self.result,
         "name": self.name,
         "Test_Cases":self.items_array
      }


   def execute(self,makefile=0):
      a=0
   
   
   def add_test_case(self,test_case):
      self.items_array.append(test_case.get_result_json()) 
      self.test_cases.append(test_case)
  
   def get_result(self):return self.result
   
   def get_result_json(self):return self.suite_struct

   def execute_by_id(self,case_index,step_index):
      if(step_index==-1):
         self.test_cases[case_index].execute()
      else:
         self.test_cases[case_index].execute_by_id(step_index)
   
   def tree_load(self,tree,i):
      #suite_tag=('ok_tag' if self.result=="OK" else ('nok_tag' if self.result=="NOK" else 'ne_tag'))
      item = tree.insert("", tk.END, text=self.name,iid=(i,-1,-1),values=(self.result))#,tags=(suite_tag,))
      for j,case in enumerate(self.test_cases):
         case.tree_load(tree,item,i,j)
             
   def get_test_items(self, idd):
      if idd[2]==-1: return self.test_cases[idd[1]]
      else: return self.test_cases[idd[1]].get_test_items(idd)

   def update_result(self):
      for items in self.test_cases:
         items.update_result()
      self.result_list = [cases.get_result() for cases in self.test_cases]
      if 'NOK' in self.result_list: self.result='NOK'
      elif 'NE' in self.result_list: self.result='NE'
      else: self.result='OK'

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
      self.items_array=[]
      self.result="NE"
      self.case_struct={
            "name": self.name,
            "id": self.id,
            "result": "NE",
            "description": self.description,
            "initial_conditions": self.Initial_Conditions,
            "test_steps":  self.items_array
        }


   def get_name(self):
       return self.name
   
   def execute(self):
      self.start_time=time()
      for ts in self.test_steps:
         ts.execute()
         self.log_content=self.log_content+ts.get_log()
         self.result_list.append(ts.get_result())
      self.end_time=time()
      self.result="NOK" if "NOK" in self.result_list else "OK"

   def add_test_step(self,test_step):
      self.items_array.append(test_step.get_result_json()) 
      self.test_steps.append(test_step)

   def write_log(self,out_file="Test_Case.txt"):
      with open(out_file,'w') as file:
         file.write(self.log)
         file.close()
   
   def get_log(self):
      return self.log_content
   
   def get_result(self):
      return self.result
   
   def get_result_json(self): return  self.case_struct

   def execute_by_id(self,step_index):
      self.test_steps[step_index].execute()

   def tree_load(self,tree,item,i,j):
      #case_tag=('ok_tag' if self.result else ('nok_tag' if self.result=="NOK" else 'ne_tag'))
      subitem = tree.insert(item, tk.END, text=self.id,iid=(i,j,-1),values=(self.result))#,tags=(case_tag,))
      for k,step in enumerate(self.test_steps):
         step.tree_load(tree,subitem,k,i,j)

   def get_test_items(self, idd):
      return self.test_steps[idd[2]]
   
   
   def update_result(self):
      for items in self.test_steps:
         items.update_result()
      self.result_list = [steps.get_result() for steps in self.test_steps]
      if 'NOK' in self.result_list: self.result='NOK'
      elif 'NE' in self.result_list: self.result='NE'
      else: self.result='OK'
################################################################### Test Steps definitions ##################################################################

class test_step:
   def __init__(self,step_id,name=""):
      self.id=step_id
      self.name=name
      self.log=""
      self.test_actions=[]
      self.start_time=time()
      self.end_time=time()
      self.result_list=[]
      self.items_array=[]
      self.result="NE"
      self.content={ 
         "id": self.id,
         "result":self.result,
         "test_actions":self.items_array
      }


   def execute(self):
      self.start_time=time()
      for index,a in enumerate(self.test_actions):
         a.execute(index)
      self.test_actions[0].enable()
      self.end_time=time()

   def add_test_action(self,test_action):
      self.items_array.append(test_action.get_result_json()) 
      self.test_actions.append(test_action)

   def get_result_list(self):
      return self.result_list
   
   def get_result(self):
      return self.result

   def get_result_json(self): return self.content

   def tree_load(self,tree,subitem,k,i,j):
      #step_tag=('ok_tag' if self.result=="OK" else ('nok_tag' if self.result=="NOK" else 'ne_tag'))
      tree.insert(subitem, tk.END, text=self.id,iid=(i,j,k),values=(self.result))#,tags=(step_tag,)) 

   def update_result(self):
      self.result_list = []
      for action in self.test_actions:
         if action.is_CA():
               self.result_list.append(action.get_result())

      if 'NOK' in self.result_list: self.result='NOK'
      elif 'NE' in self.result_list: self.result='NE'
      else: self.result='OK'