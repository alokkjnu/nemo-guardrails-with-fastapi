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
config_path = Path(__file__).parent / "guardrails_config.yaml"
config = RailsConfig.from_path(str(config_path))

if config.models and len(config.models) > 0:
    model_config = config.models[0]
    model_config.parameteres['azure_endpoint'] = os.getenv("AZURE_OPENAI_ENDPOINT")
    model_config.parameteres['azure_deployment'] = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    model_config.parameteres['azure_version'] = os.getenv("AZURE_OPENAI_VERSION")
    model_config.parameteres['azure_key'] = os.getenv("AZURE_OPENAI_KEY ")

rails = LLMRails(config)
class InputData(BaseModel):
    input: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/process")
async def process_input(data:InputData):
    input_text = data.input
    nemo_response = await rails.generate_asyn(
        messages = [{"role": "user", "content": input_text}]
    )
    nemo_output = nemo_response["content"]

    if "refuse" in nemo_output.lower():
        return {"error": "Input was refused by guardrails."}
    
    if "no" in nemo_output.lower():
        return {"error": "Input was rejected by guardrails."}

    return {"processed_input": input_text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
