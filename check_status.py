import os
from dotenv import load_dotenv
from retell import Retell

load_dotenv()
api_key = os.getenv("RETELL_API_KEY")
agent_id = os.getenv("RETELL_AGENT_ID")

client = Retell(api_key=api_key)

print(f"Checking status for Agent: {agent_id}...")

try:
    agent = client.agent.retrieve(agent_id)
    print("\n--- Current Configuration ---")
    print(f"Agent Name: {agent.agent_name}")
    print(f"LLM Model: {agent.response_engine.type}") # Should be 'custom-llm' or similar
    if hasattr(agent.response_engine, 'llm_websocket_url'):
         print(f"Websocket URL: {agent.response_engine.llm_websocket_url}")
    else:
         print("Websocket URL: NOT SET")
    print("-----------------------------")

except Exception as e:
    print(f"Error: {e}")
