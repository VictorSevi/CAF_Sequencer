
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import tkinter as tk
import json
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")
import pandas as pd
import parses_frame

PARSER_VERSION="1.0.0"

def load_file():
    # Prompt the user to select an Excel file
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path=askopenfilename(filetypes=[("Excel Files", "*.xlsx")], title="Select Excel File")
    if file_path:
        return file_path
    else:
        print("No file selected.")
        return ""
    
def devolver_text(text):
    return str(text)

def parser(protocolo):
    # Load the selected Excel file
    df = pd.read_excel(protocolo.get_file_path(), converters={"Case identifier": devolver_text,"Action Description": devolver_text})
 
    # Unmerge cells in column C, keeping values in the first row
    df['Result Description'] = df['Result Description'].ffill()
    df['Case identifier'] = df['Case identifier'].astype(str)
    df["Empty_Vars"] = df["Variables"].isna()
    df["Empty_Res"] = df["Result Description"].isna()
    df["Empty_Act"] = df["Action Description"].isna()

    #5 empty vars
    #6 Empty Res
    #7 Empty Act

    print(df)
    arr=df.to_numpy()
    flag_case_initials=False
    first_step=True
    first_case=True
    first_suite=True


    
    for line in arr:

        #Detectas si se define una suite
        if not "." in line.item(1) and not 'nan'in line.item(1):
            if not first_suite:
                case.add(step)
                suite.add(case)
                protocolo.add(suite) 
            suite = parses_frame.test_suite(line.item(1),line.item(2))
            first_suite=False 
            first_case=True

        #Detectas si se define un case
        elif "." in line.item(1) and len(line.item(1))<7:
            if not first_case:
                case.add(step)
                suite.add(case)
            case = parses_frame.test_case(line.item(2),line.item(1),line.item(2))
            flag_case_initials=True   
            first_case=False
            first_step=True        

        #Si la anterior linea es un case esta es una condición inicial
        elif flag_case_initials:
            initial_conditions=line.item(2).splitlines()[1:]
            case.update_initials(initial_conditions)
            flag_case_initials=False

        elif not line.item(8): #and not line.item(7):
            if not first_step:case.add(step)
            step=parses_frame.test_step(line.item(1))
            step.add(parses_frame.test_action(line.item(2),"MFA"))
            first_step=False

            if not (line.item(6)):
                a=parses_frame.test_action(line.item(3),"ACA")
                
                step.add(a)
                

            elif not (line.item(7)=='True'):
                step.add(parses_frame.test_action(line.item(3),"MCA"))

        elif line.item(8): # and not line.item(7):
            if not (line.item(6)=='True'):
                step.add(parses_frame.test_action(line.item(3),"ACA"))

            elif not (line.item(7)=='True'):
                step.add(parses_frame.test_action(line.item(3),"MCA"))
            
            #step.update_content()
            #case.update_content()
            #suite.update_content()   
    
    case.add(step)
    suite.add(case)
    print(suite.get_json_struct())  
    protocolo.add(suite)
    protocol_content=protocolo.get_json_struct()
    


    with open("C://Users//17940//Python_Testing//CAF_Sequencer//json_protocols//"+ protocolo.get_title()+".json", "w") as outfile:
        json.dump(protocol_content, outfile, indent = 4)


if __name__ == "__main__":
    x_path=load_file()
    objeto_protocolo=parses_frame.protocol(PARSER_VERSION,x_path)
    parser(objeto_protocolo)