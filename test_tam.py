from agents.tam_agent import tam_agent
from evaluation.evaluator import Evaluator


TEST_CASES = [

    "ACC-3336",

    "ACC-8113",

    "ACC-4213",

    "ACC-7397",

    "INVALID_ACCOUNT"

]


def validator(result):

    required = [

        "executive_summary",

        "open_risks",

        "talking_points",

    ]

    return all(

        field in result

        for field in required

    )


def run():

    results = []

    for account in TEST_CASES:

        try:

            prediction = tam_agent.generate_summary(account)

            evaluation = Evaluator.evaluate(

                account,

                prediction.model_dump(),

                validator,

            )

        except Exception:

            evaluation = Evaluator.evaluate(

                account,

                {},

                lambda _: False,

            )

        results.append(evaluation)

    return results