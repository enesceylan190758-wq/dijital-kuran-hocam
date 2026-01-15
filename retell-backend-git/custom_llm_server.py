import asyncio
import os
import json
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from concurrent.futures import TimeoutError as ConnectionTimeoutError
from retell import Retell
from llm_client import LlmClient  # We will create this next

load_dotenv()

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("retell_custom_llm")

app = FastAPI()
retell = Retell(api_key=os.getenv("RETELL_API_KEY"))

# LLM Client initialization
llm_client = LlmClient()

@app.websocket("/llm-websocket/{call_id}")
async def websocket_endpoint(websocket: WebSocket, call_id: str):
    await websocket.accept()
    logger.info(f"WebSocket connected for call: {call_id}")
    
    # Send initial config to Retell
    # This tells Retell we are ready and might send some config events
    # For now, just a simple greeting logic inside the loop
    
    try:
        # Initial greeting (optional)
        first_event = await websocket.receive_text()
        first_data = json.loads(first_event)
        
        if first_data['interaction_type'] == "call_details":
            logger.info("Received call details")
            # You can send a greeting here if you want:
            # yield_response = llm_client.draft_begin_message()
            # await websocket.send_json(yield_response)

        async for data in websocket.iter_json():
            if data['interaction_type'] == "update_only":
                continue
                
            if data['interaction_type'] == "response_required":
                # Retell is waiting for an answer
                logger.info(f"Response required for: {data.get('transcript', '')}")
                
                # Stream the response from LLM to Retell
                async for chunk in llm_client.draft_response(data):
                    await websocket.send_json(chunk)
                    
            if data['interaction_type'] == "reminder_required":
                 # Similar logic for reminders
                 pass

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for call: {call_id}")
    except Exception as e:
        logger.error(f"Error in websocket: {e}")
        await websocket.close()

@app.post("/webhook")
async def handle_webhook(request: dict):
    # Optional: Handle call analysis webhooks here
    return JSONResponse(status_code=200, content={"received": True})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
