import json

from evaluation.test_triage import run as triage_tests
from evaluation.test_tam import run as tam_tests


report = {

    "triage": [],

    "tam": []

}


for result in triage_tests():

    report["triage"].append(

        {

            "test": result.test_name,

            "passed": result.passed,

            "score": result.score,

            "message": result.message,

        }

    )


for result in tam_tests():

    report["tam"].append(

        {

            "test": result.test_name,

            "passed": result.passed,

            "score": result.score,

            "message": result.message,

        }

    )


with open(

    "evaluation/eval_report.json",

    "w",

) as f:

    json.dump(

        report,

        f,

        indent=4,

    )

print(

    "Evaluation completed."

)