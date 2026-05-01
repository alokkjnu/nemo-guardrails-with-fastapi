from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uvicorn
from nemoguardrails import LLMRails, RailsConfig
from pathlib import Path
load_dotenv()

app = FastAPI()

#configure guardrails env variables manually or use .env file


class InputData(BaseModel):
    input: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/process")
async def process_input(data:InputData):
    input_text = data.input

    return {"processed_input": input_text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
