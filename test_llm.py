from services.llm_service import llm_service

response = llm_service.generate(
    "Reply with exactly: Gemini Connected"
)

print(response)