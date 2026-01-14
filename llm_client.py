import os
import google.generativeai as genai

class LlmClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Using Flash for speed

    async def draft_response(self, request_data):
        transcript = request_data.get('transcript', [])
        
        # Build prompt from transcript
        # Load system prompt from file
        try:
            with open("system_prompt.txt", "r", encoding="utf-8") as f:
                system_prompt = f.read().strip()
        except Exception:
            system_prompt = "You are a helpful assistant."
        conversation_history = []
        
        for turn in transcript:
            role = "model" if turn['role'] == "agent" else "user"
            conversation_history.append({'role': role, 'parts': [turn['content']]})

        # Gemini requires starting with user or system (handled in config usually or just prepended)
        # We'll use a chat session approach
        
        chat = self.model.start_chat(history=conversation_history[:-1] if conversation_history else [])
        
        last_message = conversation_history[-1]['parts'][0] if conversation_history else "Hello"
        
        # Add system instruction as prefix to the last message if needed, or rely on model behavior
        # Simplest way for streaming now:
        full_prompt = f"{system_prompt}\n\nConversation so far:\n"
        for msg in conversation_history:
            full_prompt += f"{msg['role']}: {msg['parts'][0]}\n"
        full_prompt += "model: "

        # Creating a fresh generation request for simplicity/speed over chat session state management in this demo loop
        response = await self.model.generate_content_async(full_prompt, stream=True)

        async for chunk in response:
            if chunk.text:
                yield {
                    "response_id": request_data['response_id'],
                    "content": chunk.text,
                    "content_complete": False,
                    "end_call": False,
                }
        
        # Final signal
        yield {
            "response_id": request_data['response_id'],
            "content": "",
            "content_complete": True,
            "end_call": False,
        }
