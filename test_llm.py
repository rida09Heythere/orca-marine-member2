from app.services.llm import ask_llm

response = ask_llm("Say hello and confirm that you are connected to ORCA.")

print(response)