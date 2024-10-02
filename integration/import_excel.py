#####################################################################################################
#
#       LVR-Essen format protocol to json parser. Developed by Víctor Sevillano 01/nov/2024
#
#####################################################################################################

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import tkinter as tk
import json
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")
import pandas as pd
import parses_frame

#version del parser
PARSER_VERSION="1.0.0"

#funcion para seleccionar un archivo en el directorio. Devuelve ruta al archivo a cargar
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
    
#lee una celada de excel como texto
def devolver_text(text):return str(text)

#funcion general de ejecucion del parser
def parser(protocolo):

    # Load the selected Excel file
    df = pd.read_excel(protocolo.get_file_path(),sheet_name='Protocolo', converters={"Nº": devolver_text,"ACTION": devolver_text}, header=3)


    # Limpiar los nombres de las columnas (remover saltos de línea y espacios innecesarios)
    df.columns = df.columns.str.replace('\n', ' ').str.strip()

    # Desarmar filas para desglosar linea a linea
    df['RES. from C1'] = df['RES. from C1'].ffill()
    df['EXPECTED RESULT'] = df['EXPECTED RESULT']
    df['Nº'] = df['Nº'].astype(str)
    df["Empty_Vars"] = df["AL Nº VARIABLE"].isna()
    df["Empty_Res"] = df["EXPECTED RESULT"].isna()
    df["Empty_Act"] = df["ACTION"].isna()

    flag_case_initials=False
    first_step=True
    first_case=True
    first_suite=True

    #Recorrer toda la Tabla    
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
        elif "." in line['Nº'] and len(line['Nº'].strip())<7:
            if not first_case:
                case.add(step)
                suite.add(case)
            alarms_active=[]
            case = parses_frame.test_case(line['ACTION'],line['Nº'],line['ACTION'])
            flag_case_initials=True   
            first_case=False
            first_step=True
            print(line['Nº'])     

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

            print(line['EXPECTED RESULT'])
            if not line['Empty_Res']:
                if (not line['Empty_Vars']) or ("dissapears" in line['EXPECTED RESULT'] or "reset" in line['EXPECTED RESULT'] or "clear" in line['EXPECTED RESULT']):
                    vars=get_vars(line,alarms_active)
                    a=parses_frame.test_action(line['EXPECTED RESULT'],"ACA",variables=vars["varnames"],values=vars["varvalues"],checktypes=vars["checktypes"])   
                    step.add(a)
                    if vars["Alarm"]==2:
                        for var_ind in vars["varnames"]: alarms_active.append(var_ind)
                    if vars["Alarm"]==1:
                        alarms_active=[]

                elif line['Empty_Vars']:
                    step.add(parses_frame.test_action(line['EXPECTED RESULT'],"MCA"))

        #Si es Automatic ceck Action
        elif line['Empty_Act'] or ("dissapears" in line['EXPECTED RESULT'] or "reset" in line['EXPECTED RESULT'] or "clear" in line['EXPECTED RESULT']): # and not line.item(7):
            if not (line['Empty_Vars']):
                vars=get_vars(line,alarms_active)
                step.add(parses_frame.test_action(line['EXPECTED RESULT'],"ACA",variables=vars["varnames"],values=vars["varvalues"],checktypes=vars["checktypes"]))

            elif line['Empty_Vars']:
                step.add(parses_frame.test_action(line['EXPECTED RESULT'],"MCA"))
             
    
    case.add(step)
    suite.add(case)
    protocolo.add(suite)
    protocol_content=protocolo.get_json_struct()
    


    with open("C://Users//17940//Desktop//json_pruebas//"+ protocolo.get_title()+".json", "w") as outfile:
        json.dump(protocol_content, outfile, indent = 4)

#obtiene las variables, valor y tipo de comparacion para unan accion de tipo ACA
def get_vars(line, active_alarms):

    varnames = []
    varvalues = []
    checktypes = []
    interpreted_line = []
    alarm_flag = 0
    print(line['Nº'])
    if not line["Empty_Vars"]:
        for row in line['AL Nº VARIABLE'].splitlines()[0:]:
            row.strip()
            row=row.replace('<Cx>','C1')

            if '±' in row:
                values_array=row.split('=')
                values_range=values_array[1].split('±')
                varnames.append(values_array[0])
                varvalues.append({"max":numerize_value(values_range[0])+numerize_value(values_range[1]),"min":numerize_value(values_range[0])-numerize_value(values_range[1])})
                checktypes.append('RANGE')


            #lineas con formato IO2_<Cx>_xxx = 1
            elif '=' in row:
                values_array=row.split('=', 1)
                varnames.append(values_array[0])
                varvalues.append({"eq":numerize_value(values_array[1])})
                checktypes.append('EQUAL')

            #lineas con formato rango IO2_<Cx>_IA_xxx < 100
            elif '<' in row:
                values_array= row.split('<')
                if len(values_array)==3:
                    varnames.append(values_array[1])
                    varvalues.append({"max":numerize_value(values_array[2]),"min":numerize_value(values_array[0])})
                    checktypes.append('RANGE')


            #lineas con formato rango 4 < IO2_<Cx>_IA_xxx < 100
                if len(values_array)==2:
                    varnames.append(values_array[0])
                    varvalues.append({"min":numerize_value(values_array[1])})
                    checktypes.append('SMALLER')

            #lineas con formato rango IO2_<Cx>_IA_xxx > 100
            elif '>' in row: 
                varnames.append(values_array[0])
                varvalues.append({"max":numerize_value(values_array[1])})
                checktypes.append('GREATER')

            elif ("dissapears" in line['EXPECTED RESULT'] or "reset" in line['EXPECTED RESULT'] or "clear" in line['EXPECTED RESULT']):
                varnames = active_alarms
                for vars in varnames:
                    varvalues.append({"eq":0})
                    checktypes.append('EQUAL')
                alarm_flag = 1 #1 stands for alarm deactivation

            elif 'AL' in row and not("dissapears" in line['EXPECTED RESULT'] or "reset" in line['EXPECTED RESULT']):
                al_var=row.strip().replace('AL','PLC_M')
                varnames.append(al_var)
                varvalues.append({"eq":1})
                checktypes.append('EQUAL')
                alarm_flag = 2 #2 stands for alarm activation
    else:
        varnames = active_alarms
        for vars in varnames:
            varvalues.append({"eq":0})
            checktypes.append('EQUAL')
        alarm_flag = 1 #1 stands for alarm deactivation
    
    interpreted_line={"varnames":varnames,"varvalues":varvalues,"checktypes":checktypes,"Alarm":alarm_flag}  
    return interpreted_line
    
    #Si hay un '<' en la variable

#lee un string y devuelve un valor numético. Si no es posible lanza una excepcion de texto
def numerize_value(val):
    if ',' in val:
        val_point=val.replace(',','.')
        return float(val_point.strip())
    elif '.' in val:
        return float(val.strip())
    else:
        return int(val.strip())
    
if __name__ == "__main__":
    x_path=load_file()
    objeto_protocolo=parses_frame.protocol(PARSER_VERSION,x_path)
    parser(objeto_protocolo)