from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from nemoguardrails import RailsConfig,LLMRails
from pathlib import Path
#schema for input
class UserInput(BaseModel):
    input_text: str

app = FastAPI()

config_path = Path(__file__).parent / "guardrails_config"
config = RailsConfig.from_path(str(config_path))

rails = LLMRails(config)

if config.models and len(config.models) > 0:
    models_config = config.models[0]
    models_config.parameters["azure_endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT")
    models_config.parameters["azure_deployment"] = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    models_config.parameters["api_version"] = os.getenv("AZUEE_OPENAI_API_VERSION")
    models_config.parameters["azure_key"] = os.getenv("AZURE_OPENAI_KEY")


rails = LLMRails(config)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat(user_input: UserInput):
    # Here you would integrate your guardrails logic to process the user input
    # For demonstration, we will just return the input text
    nemo_response = await rails.generate_async(messages=[{"role": "user", "content": user_input.input_text}])
    nemo_output = nemo_response["content"]
    if "refuse" in nemo_output.lower():
        return {"response": "Sorry, I cannot process that request."}
    if "error" in nemo_output.lower():
        return {"response": "An error occurred while processing your request."}
    if "warning" in nemo_output.lower():
        return {"response": "Warning: Your request may not be appropriate."}
    if "no" in nemo_output.lower():
        return {"response": "Sorry, I cannot process that request."}

    return {"response": f"You said: {user_input.input_text}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)