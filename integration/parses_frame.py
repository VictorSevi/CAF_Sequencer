
import os

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
 



class test_action(test_struct):
    def __init__(self,text,type):
       super().__init__()
       self.content={
            "text": text,
            "type": type
       }

class test_step(test_struct):
    def __init__(self,step_id,test_actions=[]):
        super().__init__()
        self.items=test_actions
        self.content={
            "id": step_id,
            "result": "NE",
            "test_actions": self.items_array}

class test_case(test_struct):
    def __init__(self,case_name,case_id,description,test_steps=[],initial_conditions=[]):
        super().__init__()
        self.items=test_steps
        self.initial_conditions=initial_conditions
        self.content={
            "name": case_name,
            "id": case_id,
            "result": "NE",
            "description": description,
            "initial_conditions": self.initial_conditions,
            "test_steps": self.items_array
        }
    def update_initials(self,initial_conditions):
        self.content.update({"initial_conditions":initial_conditions})    


class test_suite(test_struct):
    def __init__(self,suite_id,name,test_cases=[]):
        super().__init__()
        self.items=test_cases
        self.content={
            "id": suite_id,
            "result": "NE",
            "name": name,
            "Test_Cases":self.items_array
        }

class protocol(test_struct):
    def __init__(self,parser_version,file_path,test_suites=[]):
        super().__init__()
        self.file_path=file_path
        self.items=test_suites
        self.content={
            "Protocol_edition":self.get_edition(),
            "Parser_Version":parser_version,
            "Protocol_name":self.get_title(),
            "result": "NE",
            "Test_Suites":self.items_array
        }

    def get_edition(self):
        file_name = os.path.basename( self.file_path)
        position=file_name.find("Ed.")
        return file_name[position+3]

    def get_title(self):
        file_name = os.path.basename( self.file_path)
        position=file_name.find("_Ed.")
        return file_name[0:position]
    
    def get_file_path(self):
        return self.file_path


        
