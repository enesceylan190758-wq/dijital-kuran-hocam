import os
from dotenv import load_dotenv
from retell import Retell

load_dotenv()

api_key = os.getenv("RETELL_API_KEY")
source_agent_id = os.getenv("RETELL_AGENT_ID")
ngrok_url = "wss://subaggregately-portionless-elza.ngrok-free.dev/llm-websocket"

client = Retell(api_key=api_key)

print(f"Reading source agent {source_agent_id}...")
try:
    source_agent = client.agent.retrieve(source_agent_id)
    voice_id = source_agent.voice_id
    print(f"Found voice_id: {voice_id}")
    
    print("Creating NEW Custom Agent...")
    new_agent = client.agent.create(
        agent_name="Gemini Custom Agent",
        voice_id=voice_id,
        response_engine={
            "type": "custom-llm",
            "llm_websocket_url": ngrok_url
        }
    )
    
    print("✅ New Agent Created Successfully!")
    print(f"New Agent ID: {new_agent.agent_id}")
    print(f"New Websocket URL: {new_agent.response_engine.llm_websocket_url}")
    
except Exception as e:
    print(f"❌ Error: {e}")
