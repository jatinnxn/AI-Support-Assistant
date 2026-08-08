from agents.triage_agent import triage_agent
from models.schemas import TicketInput

ticket = TicketInput(
    subject="Unable to login",
    body="Customer cannot login after password reset."
)

result = triage_agent.classify(ticket)

print(result.model_dump_json(indent=4))