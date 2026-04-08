import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel

# -------- Phase 1: Backend --------
api = FastAPI()

class StepInput(BaseModel):
    action: str

state = {
    "history": []
}

@api.get("/state")
def get_state():
    return state

@api.post("/reset")
def reset():
    state["history"] = []
    return {"status": "reset"}

@api.post("/step")
def step(input: StepInput):
    user_input = input.action

    response = f"Bot says: {user_input[::-1]}"

    state["history"].append({
        "user": user_input,
        "bot": response
    })

    return {
        "response": response,
        "state": state
    }

# -------- Phase 2: UI --------
def chatbot(user_input):
    return f"Bot says: {user_input[::-1]}"

ui = gr.Interface(
    fn=chatbot,
    inputs="text",
    outputs="text",
    title="RL Customer Support Agent"
)

# Mount UI + API
app = gr.mount_gradio_app(api, ui, path="/")
