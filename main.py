from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from agents.triage_agent import triage_agent
from agents.tam_agent import tam_agent

from models.schemas import (
    TicketInput,
    TicketTriageResponse,
    AccountSummaryResponse,
)

app = FastAPI(
    title="Support AI Assistant",
    version="1.0.0",
    description="Production-grade AI Support & TAM Assistant",
)


@app.get("/")
def health():
    return {
        "status": "healthy",
        "application": "Support AI Assistant",
        "version": "1.0.0",
    }


# -------------------------------------------------------------------
# TASK 1
# Ticket Triage
# -------------------------------------------------------------------
@app.post(
    "/triage",
    response_model=TicketTriageResponse,
    tags=["Ticket Triage"],
)
def classify_ticket(ticket: TicketInput):

    try:

        return triage_agent.classify(ticket)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# -------------------------------------------------------------------
# TASK 2
# TAM Summary
# -------------------------------------------------------------------
@app.get(
    "/tam/{account_id}",
    response_model=AccountSummaryResponse,
    tags=["TAM"],
)
def account_summary(account_id: str):

    try:

        return tam_agent.generate_summary(account_id)

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detail": str(exc),
        },
    )