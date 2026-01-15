import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retell import Retell
import uvicorn

load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Retell(api_key=os.getenv("RETELL_API_KEY"))

class RegisterCallResponse(BaseModel):
    access_token: str

@app.post("/register-call", response_model=RegisterCallResponse)
async def register_call():
    agent_id = os.getenv("RETELL_AGENT_ID")
    if not agent_id:
        raise HTTPException(status_code=500, detail="RETELL_AGENT_ID not set in .env")

    try:
        # Register the call to get an access token
        call_response = client.call.register(
            agent_id=agent_id,
        )
        print(f"Call registered: {call_response.call_id}")
        return {"access_token": call_response.access_token}
    except Exception as e:
        print(f"Error registering call: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
