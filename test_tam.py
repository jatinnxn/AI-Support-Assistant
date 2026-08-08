from agents.tam_agent import tam_agent

summary = tam_agent.generate_summary("ACC-3336")

print(summary.model_dump_json(indent=4))