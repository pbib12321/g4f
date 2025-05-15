import g4f
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=1)

# Store memory per user ID
chat_memory = {}  # Format: { "userid": [ {role, content}, ... ] }

class Query(BaseModel):
    text: str
    userid: str  # required for per-user memory

def g4f_sync(messages: list) -> str:
    return g4f.ChatCompletion.create(
        model="",  # required param
        messages=messages
    )

@app.post("/chat")
async def chat(query: Query):
    loop = asyncio.get_running_loop()

    # Get or create user's message history
    user_id = query.userid
    if user_id not in chat_memory:
        chat_memory[user_id] = []

    # Append the new user message
    chat_memory[user_id].append({"role": "user", "content": query.text})

    try:
        # Get AI response with full chat history
        result = await loop.run_in_executor(executor, g4f_sync, chat_memory[user_id])

        # Save assistant response
        if isinstance(result, str):
            chat_memory[user_id].append({"role": "assistant", "content": result.strip()})
            return {"response": result.strip()}
        else:
            return {"error": "Invalid response from g4f"}

    except Exception as e:
        return {"error": str(e)}







