from agents.triage_agent import triage_agent
from models.schemas import TicketInput
from evaluation.evaluator import Evaluator


TEST_CASES = [

    {
        "name": "Login Failure",

        "ticket": TicketInput(
            subject="Cannot login",
            body="Users cannot login after password reset."
        )
    },

    {
        "name": "Billing",

        "ticket": TicketInput(
            subject="Incorrect Invoice",
            body="We were charged twice."
        )
    },

    {
        "name": "Performance",

        "ticket": TicketInput(
            subject="Application slow",
            body="Dashboard taking 40 seconds."
        )
    },

    {
        "name": "Integration",

        "ticket": TicketInput(
            subject="Slack Integration Failed",
            body="Webhook failing."
        )
    },

    {
        "name": "Adversarial",

        "ticket": TicketInput(
            subject="Help",
            body="Nothing works."
        )
    }

]


def validator(result):

    required = [

        "product_area",

        "issue_category",

        "urgency",

        "reasoning",

        "knowledge_base_article",

        "responder_team",

        "first_response"

    ]

    data = result.model_dump()

    return all(field in data for field in required)


def run():

    results = []

    for case in TEST_CASES:

        prediction = triage_agent.classify(
            case["ticket"]
        )

        evaluation = Evaluator.evaluate(
            case["name"],
            prediction.model_dump(),
            validator,
        )

        results.append(evaluation)

    return results