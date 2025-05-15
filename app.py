import g4f
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# Allow frontend from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create thread executor for blocking calls
executor = ThreadPoolExecutor(max_workers=1)

# Request schema
class Query(BaseModel):
    text: str

# Blocking call to g4f
def g4f_sync(text: str) -> str:
    try:
        return g4f.ChatCompletion.create(
            model="",  # required but empty string works
            messages=[{"role": "user", "content": text}]
        )
    except Exception as e:
        return f"Error from g4f: {e}"

# API endpoint
@app.post("/chat")
async def chat(query: Query):
    loop = asyncio.get_running_loop()
    try:
        # Run g4f in background thread
        result = await loop.run_in_executor(executor, g4f_sync, query.text)

        # Ensure it's just a string for frontend
        if isinstance(result, str):
            return {"response": result.strip()}
        else:
            return {"error": "Invalid response type from g4f."}

    except Exception as e:
        return {"error": str(e)}





