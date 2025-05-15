import g4f
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=1)

class Query(BaseModel):
    text: str

def g4f_sync(text: str) -> str:
    return g4f.ChatCompletion.create(
        model="",  # required param, empty string works
        messages=[{"role": "user", "content": text}]
    )

@app.post("/chat")
async def chat(query: Query):
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(executor, g4f_sync, query.text)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}




