"""
Week 4 RAG Pipeline Validation Tests

Tests:
1. IoT alert input processing
2. Retrieval workflow
3. Recommendation generation
"""


from rag_pipeline import RAGPipeline



def test_pipeline_initialization():

    pipeline = RAGPipeline()

    assert pipeline is not None

    print("PASS : Pipeline initialization")



def test_short_circuit_alert():


    pipeline = RAGPipeline()


    alert = {

        "machine_id":"HVAC_TEST_001",

        "sensor":"Voltage Sensor",

        "sensor_value":"220 V",

        "error_code":"SHORT_CIRCUIT",

        "severity":"HIGH"

    }


    result = pipeline.process_alert(alert)


    assert result is not None


    print("PASS : SHORT_CIRCUIT scenario")




def test_refrigerant_alert():


    pipeline = RAGPipeline()


    alert = {


        "machine_id":"HVAC_TEST_002",

        "sensor":"Pressure Sensor",

        "sensor_value":"30 psi",

        "error_code":"REFRIGERANT_LEAK",

        "severity":"MEDIUM"


    }


    result = pipeline.process_alert(alert)


    assert result is not None


    print("PASS : REFRIGERANT_LEAK scenario")




def test_overheating_alert():


    pipeline = RAGPipeline()


    alert = {


        "machine_id":"HVAC_TEST_003",

        "sensor":"Temperature Sensor",

        "sensor_value":"100 C",

        "error_code":"OVERHEATING",

        "severity":"HIGH"


    }


    result = pipeline.process_alert(alert)


    assert result is not None


    print("PASS : OVERHEATING scenario")





if __name__ == "__main__":


    print("\n===== RAG PIPELINE VALIDATION =====\n")


    test_pipeline_initialization()


    test_short_circuit_alert()


    test_refrigerant_alert()


    test_overheating_alert()


    print("\nALL TESTS COMPLETED SUCCESSFULLY")