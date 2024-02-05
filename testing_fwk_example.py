import CAFTestingFwk as fwk
import json

initial_conditions=["Estar apagado","Ser un poco Fruko"]
case_description="Esto comprueba si con el tren apagado se te ve igual de fruko"
case_id="1.2"
test_case_list=[]

def main():
   
   #Primera implementación

    #test_suite=fwk.test_suite("Putu Suite","1.00")
    #
    #for n in range(2):
    #    test_case = fwk.test_case("Test Case",initial_conditions,case_description,"1.00"+str(n))
    #    for i in range(2):
    #        test_case.add_test_step(fwk.test_step("1.00"+str(n)+"."+str(i)))
    #    test_suite.add_test_case(test_case)
    #test_suite.title()
    #test_suite.execute()
    #print(test_suite.get_log())
   

    #implementación con json


    
    test_suite=fwk.test_suite("Putu Suite","1.00")
    #
    #for n in range(2):
    #    test_case = fwk.test_case("Test Case",initial_conditions,case_description,"1.00"+str(n))
    #    for i in range(2):
    #        test_case.add_test_step(fwk.test_step("1.00"+str(n)+"."+str(i)))
    #    test_suite.add_test_case(test_case)
    #test_suite.title()
    #test_suite.execute()
    #print(test_suite.get_log())

    with open('input_data.json') as config:
        data_object=json.load(config)
    for case in data_object["Test_Cases"]:
        test_case = fwk.test_case(case["name"],case["initial_conditions"],case["description"],str(case["id"]))
        for step in case["test_steps"]:        
            for action in step["test_actions"]:
                test_case.add_test_step(fwk.test_step(action["text"]))
            test_suite.add_test_case(test_case)
    test_suite.execute()
    


if __name__ == "__main__":
   main()