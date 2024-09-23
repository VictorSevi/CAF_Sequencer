
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
    file_path=askopenfilename(filetypes=[("Excel Files", "*.xlsm")], title="Select Excel File")
    if file_path:
        return file_path
    else:
        print("No file selected.")
        return ""
    
def devolver_text(text):
    return str(text)

def parser(protocolo):
    # Load the selected Excel file
    df = pd.read_excel(protocolo.get_file_path(),sheet_name='Protocolo', converters={"Nº": devolver_text,"ACTION": devolver_text}, header=3)


    # Limpiar los nombres de las columnas (remover saltos de línea y espacios innecesarios)
    df.columns = df.columns.str.replace('\n', ' ').str.strip()

    print(df.columns)

    # Unmerge cells in column C, keeping values in the first row
    df['RES. from C1'] = df['RES. from C1'].ffill()
    df['Nº'] = df['Nº'].astype(str)
    df["Empty_Vars"] = df["AL Nº VARIABLE"].isna()
    df["Empty_Res"] = df["EXPECTED RESULT"].isna()
    df["Empty_Act"] = df["ACTION"].isna()

    flag_case_initials=False
    first_step=True
    first_case=True
    first_suite=True

    
    for index,line in df.iterrows():
        #Detectas si se define una suite
        if "." not in line['Nº'] and line['Empty_Res']:
            if not first_suite:
                case.add(step)
                suite.add(case)
                protocolo.add(suite) 
            suite = parses_frame.test_suite(line['Nº'],line['ACTION'])
            first_suite=False 
            first_case=True

        #Detectas si se define un case
        elif "." in line['Nº'] and len(line['Nº'])<7:
            if not first_case:
                case.add(step)
                suite.add(case)
            case = parses_frame.test_case(line['ACTION'],line['Nº'],line['ACTION'])
            flag_case_initials=True   
            first_case=False
            first_step=True        

        #Si la anterior linea es un case esta es una condición inicial del caso anterior
        elif flag_case_initials:
            initial_conditions=str(line['ACTION']).splitlines()[1:]
            case.update_initials(initial_conditions)
            flag_case_initials=False

        #Si es Manual Force Action
        elif not line['Empty_Act']: #and not line.item(7):
            if not first_step:case.add(step)
            step=parses_frame.test_step(line['Nº'])
            step.add(parses_frame.test_action(line['ACTION'],"MFA"))
            first_step=False

            if not line['Empty_Vars']:
                a=parses_frame.test_action(line['EXPECTED RESULT'],"ACA")
                
                step.add(a)
                

            elif line['Empty_Vars']:
                step.add(parses_frame.test_action(line['EXPECTED RESULT'],"MCA"))

        #Si es Automatic ceck Action
        elif line['Empty_Act']: # and not line.item(7):
            if not (line['Empty_Vars']):
                step.add(parses_frame.test_action(line['EXPECTED RESULT'],"ACA"))

            elif line['Empty_Vars']:
                step.add(parses_frame.test_action(line['EXPECTED RESULT'],"MCA"))
            
            #step.update_content()
            #case.update_content()
            #suite.update_content()   
    
    case.add(step)
    suite.add(case)
    print(suite.get_json_struct())  
    protocolo.add(suite)
    protocol_content=protocolo.get_json_struct()
    


    with open("C://Users//17940//Desktop//json_pruebas//"+ protocolo.get_title()+".json", "w") as outfile:
        json.dump(protocol_content, outfile, indent = 4)


if __name__ == "__main__":
    x_path=load_file()
    objeto_protocolo=parses_frame.protocol(PARSER_VERSION,x_path)
    parser(objeto_protocolo)