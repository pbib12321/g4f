import g4f
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread executor to handle g4f blocking calls
executor = ThreadPoolExecutor(max_workers=1)

# In-memory chat history
chat_memory = {}

# Request model
class Query(BaseModel):
    text: str
    userid: str

# Sync wrapper for g4f
def g4f_sync(messages: list) -> str:
    try:
        return g4f.ChatCompletion.create(
            model="",  # empty model param
            messages=messages
        )
    except Exception as e:
        return f"Error from g4f: {e}"

# POST endpoint
@app.post("/chat")
async def chat(query: Query):
    loop = asyncio.get_running_loop()
    user_id = query.userid.strip()

    # Create memory if needed
    if user_id not in chat_memory:
        chat_memory[user_id] = []

    # Add user message
    chat_memory[user_id].append({"role": "user", "content": query.text})

    try:
        # Get response from g4f using full history
        result = await loop.run_in_executor(executor, g4f_sync, chat_memory[user_id])

        # If result is valid, store and return it
        if isinstance(result, str):
            clean = result.strip()
            chat_memory[user_id].append({"role": "assistant", "content": clean})
            return {"response": clean}

        return {"response": "Error: Invalid reply format from g4f."}

    except Exception as e:
        return {"response": f"Error processing request: {str(e)}"}








