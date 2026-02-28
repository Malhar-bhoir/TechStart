from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from unsloth import FastLanguageModel
import torch

# 1. Initialize API
app = FastAPI(title="SLM Tutor API")

# 2. Global Model Variables (Loaded on Startup)
model = None
tokenizer = None
max_seq_length = 2048

# 3. Load the Model (Only runs once when server starts)
@app.on_event("startup")
async def load_model():
    global model, tokenizer
    print("⏳ Loading Base Model & Adapters... This may take time.")
    
    # Load Base Model + Your Adapters
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "SLM_Sample", # Path to your folder containing adapter_model.safetensors
        max_seq_length = max_seq_length,
        dtype = None,
        load_in_4bit = True, # Must match your training settings
    )
    FastLanguageModel.for_inference(model) # Enable native 2x faster inference
    print("✅ Model Loaded Successfully!")

# 4. Define Request Structure (What Django sends to us)
class LearningRequest(BaseModel):
    mode: str          # "teach", "quiz", or "grade"
    topic: str         # e.g., "Variables"
    language: str      # "Hindi", "Marathi", "English"
    user_input: str = "" # Optional: User's answer for grading

# 5. Define the Prompt Template (Must match your training!)
alpaca_prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{}

### Response:
"""

# 6. The API Endpoint
@app.post("/generate")
async def generate_response(request: LearningRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Dynamic System Prompt Logic (The "Brain" Switch)
    system_instruction = ""
    
    if request.mode == "teach":
        # Instruction for Teaching
        system_instruction = f"You are a friendly Tutor. Explain the topic '{request.topic}' in {request.language}."
        user_query = f"Teach me about {request.topic}."
        
    elif request.mode == "quiz":
        # Instruction for Quizzing
        system_instruction = f"You are a Quiz Master. Ask a multiple-choice question about '{request.topic}' in {request.language}."
        user_query = f"Generate a quiz question for {request.topic}."
        
    elif request.mode == "grade":
        # Instruction for Grading
        system_instruction = f"You are a helpful Tutor. Correct the user's answer in {request.language}."
        user_query = f"The topic is '{request.topic}'. The user answered: '{request.user_input}'. Is this correct? Explain why."

    else:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'teach', 'quiz', or 'grade'.")

    # Combine into the training format
    # Note: We merge System + User query into the 'Instruction' slot if your training data combined them,
    # OR if you trained with a separate 'System' field, we format it specifically.
    # Assuming standard Alpaca format from your notebook:
    full_prompt = alpaca_prompt.format(
        f"{system_instruction}\n\nTask: {user_query}", 
        "", 
        ""
    )

    # Convert to tokens
    inputs = tokenizer([full_prompt], return_tensors="pt").to("cuda")

    # Generate Output
    outputs = model.generate(
        **inputs, 
        max_new_tokens=256, 
        use_cache=True,
        temperature=0.7 # Adds a little creativity
    )
    
    # Decode Output
    response_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    
    # Clean up (remove the prompt from the answer)
    response_clean = response_text.split("### Response:")[-1].strip()

    return {"response": response_clean}

# Run with: uvicorn main:app --reload --port 8000