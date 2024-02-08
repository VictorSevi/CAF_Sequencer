import CAFTestingFwk as fwk
import pandas as pd
import json
import os
import shutil


def main():
    
    test_suite=fwk.test_suite("Putu Suite","5")

    with open('structure.json') as config:
        data_object=json.load(config)
    config.close()

    #with open('file_structure.json') as paths_file:
    #    paths_object=json.load(paths_file)
    #config.close()

    for case in data_object["Test_Cases"]:
        test_case = fwk.test_case(case["name"],case["initial_conditions"],case["description"],str(case["id"]))
        for step in case["test_steps"]:
            test_step = fwk.test_step(step["id"],"xxx")   
            for action in step["test_actions"]:
                test_action = fwk.test_action(step["id"],action["text"],action["type"])   
                test_step.add_test_action(test_action)
            test_case.add_test_step(test_step)
        test_suite.add_test_case(test_case)
    test_suite.execute()


    with open("C://Users//17940//Python_Testing//CAF_Sequencer//results//results.json", "w") as outfile:
        json.dump(test_suite.get_result_json(), outfile, indent = 4)
    
    test_suite.write_log()
    
    #write_results(result_list,template_path,result_folder )

    input("Test end, please press enter....")
    

if __name__ == "__main__":
    main()
    #mark_ok("ProtPrueba.xlsx")