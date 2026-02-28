from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# 1. Initialize API
app = FastAPI(title="SLM Tutor API")

# 2. Global Variables
model = None
tokenizer = None
BASE_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
ADAPTER_PATH = "SLM_Sample"

# 3. Load Model (CPU Compatible)
@app.on_event("startup")
async def load_model():
    global model, tokenizer
    print("⏳ Loading Model on CPU... (This might take 1-2 minutes)")

    try:
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_NAME,
            device_map="cpu",
            torch_dtype=torch.float32,
            trust_remote_code=True
        )

        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
        model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
        model = model.merge_and_unload()
        
        print("✅ Model Loaded Successfully on CPU!")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise e

# 4. Request Body
class LearningRequest(BaseModel):
    mode: str
    topic: str
    language: str
    user_input: str = ""
    context: str = ""

# 5. Prompt Template
alpaca_prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{}

### Response:
"""

@app.post("/generate")
async def generate_response(request: LearningRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    system_instruction = ""
    user_query = ""

    if request.mode == "teach":
        system_instruction = f"You are a friendly Tutor. Explain the topic '{request.topic}' in {request.language}."
        if request.user_input and len(request.user_input) > 2:
            user_query = f"User Question: {request.user_input}\nAnswer this specific question."
        else:
            user_query = f"Teach me about {request.topic}."
            
    elif request.mode == "quiz":
        system_instruction = f"You are a Quiz Master. Ask a multiple-choice question about '{request.topic}' in {request.language}."
        user_query = f"Generate a quiz question for {request.topic}."
        
    elif request.mode == "grade":
        # CHANGE 1: Neutral System Prompt to reduce bias
        system_instruction = f"You are a fair Teacher. Evaluate if the user's answer is correct in {request.language}."
        
        # CHANGE 2: Simplified Grading Prompt for 3B Model
        user_query = f"The Question was: {request.context}\n\nThe User Answered: '{request.user_input}'.\n\nTask: Compare the User Answer to the Correct Answer in the question. If it matches, say 'Correct'. If not, explain why."
        
    else:
        raise HTTPException(status_code=400, detail="Invalid mode.")

    full_prompt = alpaca_prompt.format(f"{system_instruction}\n\nTask: {user_query}")

    inputs = tokenizer(full_prompt, return_tensors="pt").to("cpu")

    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=256, 
            use_cache=True,
            temperature=0.7
        )
    
    response_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    response_clean = response_text.split("### Response:")[-1].strip()

    # CHANGE 3: STOP LEAKAGE - Cut off if the model starts generating a new instruction
    if "### Instruction:" in response_clean:
        response_clean = response_clean.split("### Instruction:")[0].strip()

    return {"response": response_clean}