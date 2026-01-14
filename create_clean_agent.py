import os
from dotenv import load_dotenv
from retell import Retell

load_dotenv()
api_key = os.getenv("RETELL_API_KEY")
# We will use the voice from the existing agent if possible, or a default
source_agent_id = os.getenv("RETELL_AGENT_ID")

client = Retell(api_key=api_key)
ngrok_url = "wss://subaggregately-portionless-elza.ngrok-free.dev/llm-websocket"

print("Creating a BRAND NEW Custom LLM Agent...")

try:
    # Try to get voice_id from existing agent
    voice_id = "11labs-Adrian" # Default fallback
    try:
        source = client.agent.retrieve(source_agent_id)
        voice_id = source.voice_id
        print(f"Using Voice ID from existing agent: {voice_id}")
    except:
        print("Using default voice.")

    new_agent = client.agent.create(
        agent_name="MJA Dental - Custom LLM (API Created)",
        voice_id=voice_id,
        response_engine={
            "type": "custom-llm",
            "llm_websocket_url": ngrok_url
        }
    )
    
    print("\n✅ SUCCESS! New Agent Created.")
    print(f"New Agent ID: {new_agent.agent_id}")
    print(f"Agent Name: {new_agent.agent_name}")
    print(f"Linked to: {ngrok_url}")
    print("\nAction Required: Update .env with this new ID.")
    
except Exception as e:
    print(f"❌ Error creating agent: {e}")
