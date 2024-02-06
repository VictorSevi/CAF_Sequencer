import CAFTestingFwk as fwk
import json

initial_conditions=["Estar apagado","Ser un poco Fruko"]
case_description="Esto comprueba si con el tren apagado se te ve igual de fruko"
case_id="1.2"
test_case_list=[]

def main():
    
    test_suite=fwk.test_suite("Putu Suite","1.00")

    with open('structure.json') as config:
        data_object=json.load(config)
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
    input("Test end, please press enter....")
    

if __name__ == "__main__":
   main()