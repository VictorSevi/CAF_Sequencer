import CAFTestingFwk as fwk
import json
import os
import shutil
import pandas as pd

os.system('cls' if os.name == 'nt' else 'clear')

def main():
    with open('D0000006245_Propulsion Management Functional Factory Type Test.json') as test_json:
        protocol_object=json.load(test_json)
    test_json.close()

    protocol=fwk.protocol(protocol_object["Protocol_name"],protocol_object["Protocol_edition"])

    for suite in protocol_object["Test_Suites"]:
        test_suite=fwk.test_suite(suite["name"],suite["id"])
        for case in suite["Test_Cases"]:
            test_case = fwk.test_case(case["name"],case["initial_conditions"],case["description"],str(case["id"]))
            for step in case["test_steps"]:
                test_step = fwk.test_step(step["id"],"xxx")   
                for index,action in enumerate(step["test_actions"]):
                    test_action = fwk.test_action(step["id"],action["text"],action["type"],cmd=False,row=index)
                    test_step.add_test_action(test_action)
                test_case.add_test_step(test_step)
            test_suite.add_test_case(test_case)
        protocol.add_test_suite(test_suite)
    protocol.execute()



    with open("C://Users//17940//Python_Testing//CAF_Sequencer//results//results.json", "w") as outfile:
        print(protocol.get_result_json())
        json.dump(protocol.get_result_json(), outfile, indent = 4)
    
    #protocol_object.write_log()
    
    #write_results(result_list,template_path,result_folder )

    input("Test end, please press enter....")
    

if __name__ == "__main__":
    main()
    #mark_ok("ProtPrueba.xlsx")