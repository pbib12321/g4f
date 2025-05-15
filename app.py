import g4f
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.post("/chat")
async def chat(query: Query):
    try:
        response = g4f.ChatCompletion.create(
            messages=[{"role": "user", "content": query.text}]
        )
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

