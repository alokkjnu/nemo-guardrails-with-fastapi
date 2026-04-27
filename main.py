from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn

#schema for input
class UserInput(BaseModel):
    input_text: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat(user_input: UserInput):
    # Here you would integrate your guardrails logic to process the user input
    # For demonstration, we will just return the input text
    return {"response": f"You said: {user_input.input_text}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)