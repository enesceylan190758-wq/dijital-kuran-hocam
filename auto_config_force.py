import os
from dotenv import load_dotenv
from retell import Retell

load_dotenv()
api_key = os.getenv("RETELL_API_KEY")
agent_id = os.getenv("RETELL_AGENT_ID")
# The URL user confirmed
ngrok_url = "wss://subaggregately-portionless-elza.ngrok-free.dev/llm-websocket"

print(f"Connecting to Retell for Agent: {agent_id}...")
client = Retell(api_key=api_key)

try:
    # Update the agent to use Custom LLM with our URL
    response = client.agent.update(
        agent_id=agent_id,
        response_engine={
            "type": "custom-llm",
            "llm_websocket_url": ngrok_url
        }
    )
    print("✅ SUCCESS! Agent URL updated automatically.")
    print(f"Linked to: {ngrok_url}")
except Exception as e:
    print(f"❌ Failed to update: {e}")
    # Try alternative key just in case library changed
    try:
        response = client.agent.update(
            agent_id=agent_id,
            llm_websocket_url=ngrok_url
        )
        print("✅ SUCCESS! Agent URL updated (Method 2).")
    except Exception as e2:
         print(f"❌ Failed (Method 2): {e2}")
