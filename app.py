import g4f
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/chat")
async def chat(query: Query):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query.text}]
        )
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
