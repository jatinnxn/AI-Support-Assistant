from models.schemas import TicketInput

ticket = TicketInput(
    subject="Cannot Login",
    body="Nobody can login after deployment."
)

print(ticket)