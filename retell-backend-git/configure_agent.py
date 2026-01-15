import os
from dotenv import load_dotenv
from retell import Retell

load_dotenv()

api_key = os.getenv("RETELL_API_KEY")
agent_id = os.getenv("RETELL_AGENT_ID")
ngrok_url = "wss://subaggregately-portionless-elza.ngrok-free.dev/llm-websocket"

client = Retell(api_key=api_key)

print(f"Updating Agent {agent_id}...")
try:
    response = client.agent.update(
        agent_id=agent_id,
        llm_websocket_url=ngrok_url
    )
    print("✅ Agent Updated Successfully!")
    print(f"New Websocket URL: {response.llm_websocket_url}")
except Exception as e:
    print(f"❌ Error updating agent: {e}")
