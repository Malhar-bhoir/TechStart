# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# app = FastAPI(title="SLM Tutor API")

# MODEL_PATH = r"D:\SEM7\major prj\Techstart\fastapi_slm\SLM_MERGED"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = None
# tokenizer = None


# # # ==========================
# # # Load Model on Startup
# # # ==========================
# # @app.on_event("startup")
# # async def load_model():
# #     global model, tokenizer

# #     print("🚀 Loading merged model...")

# #     tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# #     model = AutoModelForCausalLM.from_pretrained(
# #         MODEL_PATH,
# #         torch_dtype=torch.float16,
# #         device_map="auto"
# #     )

# #     model.eval()

# #     print("✅ Model Loaded Successfully!")

# # ==========================
# # Load Model on Startup
# # ==========================
# @app.on_event("startup")
# async def load_model():
#     global model, tokenizer

#     print(f"🚀 Loading merged model on: {device.type.upper()}...")

#     tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

#     # Automatically choose the right data type
#     # GPUs love float16, but CPUs need float32
#     chosen_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    
#     # Explicitly map to CPU if no GPU is found
#     chosen_device_map = "auto" if torch.cuda.is_available() else "cpu"

#     model = AutoModelForCausalLM.from_pretrained(
#         MODEL_PATH,
#         torch_dtype=chosen_dtype,
#         device_map=chosen_device_map
#     )

#     model.eval()

#     print("✅ Model Loaded Successfully!")

# # ==========================
# # Request Body
# # ==========================
# class LearningRequest(BaseModel):
#     mode: str
#     topic: str
#     language: str
#     user_input: str = ""
#     context: str = ""


# # ==========================
# # Prompt Template
# # ==========================
# alpaca_prompt = """### Instruction:
# {}

# ### Response:
# """


# # ==========================
# # Generate Endpoint
# # ==========================
# # @app.post("/generate")
# # async def generate_response(request: LearningRequest):

# #     if model is None:
# #         raise HTTPException(status_code=500, detail="Model not loaded")

# #     if request.mode == "teach":
# #         instruction = f"You are a friendly Tutor. Explain {request.topic} in {request.language}."
# #     elif request.mode == "quiz":
# #         instruction = f"You are a Quiz Master. Ask a multiple-choice question about {request.topic} in {request.language}."
# #     elif request.mode == "grade":
# #         instruction = f"Evaluate this answer: {request.user_input}"
# #     else:
# #         raise HTTPException(status_code=400, detail="Invalid mode")

# #     prompt = alpaca_prompt.format(instruction)

# #     inputs = tokenizer(prompt, return_tensors="pt").to(device)

# #     with torch.no_grad():
# #         outputs = model.generate(
# #             **inputs,
# #             max_new_tokens=128,
# #             temperature=0.7,
# #             top_p=0.9,
# #             do_sample=True,
# #             pad_token_id=tokenizer.eos_token_id
# #         )

# #     response = tokenizer.decode(outputs[0], skip_special_tokens=True)

# #     clean_response = response.split("### Response:")[-1].strip()

# #     return {"response": clean_response}
# @app.post("/generate")
# async def generate_response(request: LearningRequest):

#     if model is None:
#         raise HTTPException(status_code=500, detail="Model not loaded")

#     # Dynamic System Prompt Logic
#     system_instruction = ""
#     user_query = ""

#     if request.mode == "teach":
#         system_instruction = f"You are a Java Programming Tutor. Explain in {request.language}."
#         user_query = f"Teach me about {request.topic} in Java."
#     elif request.mode == "quiz":
#         system_instruction = f"You are a Quiz Master. Ask a question in {request.language}."
#         user_query = f"Ask a multiple-choice question about {request.topic}."
#     elif request.mode == "grade":
#         system_instruction = f"You are a helpful Tutor. Correct the user's answer in {request.language}."
#         user_query = f"The topic is {request.topic}. The user answered: {request.user_input}. Is this correct? Explain."
#     elif request.mode == "chat":
#         system_instruction = f"You are a friendly and polite AI computer tutor. Converse with the user naturally in {request.language}."
#         user_query = request.user_input
#     else:
#         raise HTTPException(status_code=400, detail="Invalid mode")

#     # Format exactly like your training data
#     prompt = alpaca_prompt.format(user_query, system_instruction)

#     inputs = tokenizer(prompt, return_tensors="pt").to(device)

#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=128,
#             temperature=0.7,
#             top_p=0.9,
#             do_sample=True,
#         )

#     response_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    
#     # Clean up output to only show the response
#     response_clean = response_text.split("### Response:")[-1].strip()

#     return {"response": response_clean}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI(title="SLM Tutor API")

MODEL_PATH = r"D:\SEM7\major prj\Techstart\fastapi_slm\SLM_MERGED_v2"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = None
tokenizer = None

# ==========================
# Load Model on Startup
# ==========================
@app.on_event("startup")
async def load_model():
    global model, tokenizer

    print(f"🚀 Loading merged model on: {device.type.upper()}...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    # Automatically choose the right data type
    chosen_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    chosen_device_map = "auto" if torch.cuda.is_available() else "cpu"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=chosen_dtype,
        device_map=chosen_device_map
    )

    model.eval()
    print("✅ Model Loaded Successfully!")

# ==========================
# Request Body
# ==========================
class LearningRequest(BaseModel):
    mode: str
    topic: str
    language: str
    user_input: str = ""
    context: str = ""

# ==========================
# Prompt Template (Matches your Colab Training)
# ==========================
alpaca_prompt = """### Instruction:
{}

### Response:
"""

# ==========================
# ENDPOINT
# ==========================
@app.post("/generate")
async def generate_response(request: LearningRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    user_query = ""

    # --- Mode Logic ---
    if request.mode == "teach":
        if request.user_input and len(request.user_input) > 2:
            user_query = f"User Question: {request.user_input}\nAnswer this specific question about {request.topic} in {request.language}."
        else:
            user_query = f"Teach me about {request.topic} in {request.language}."
            
    elif request.mode == "quiz":
        user_query = f"Generate a multiple-choice quiz question for the topic: {request.topic} in {request.language}."
        
    elif request.mode == "grade":
        # CRITICAL FIX: Pass the context so it knows what the question was!
        user_query = f"The Question was: {request.context}\n\nThe User Answered: '{request.user_input}'.\n\nTask: Evaluate if the user's answer is correct in {request.language}. If it matches, say 'Correct'. If not, explain why."
        
    elif request.mode == "chat":
        # STRONGER PERSONA PROMPT: Overrides the base model's default identity
        user_query = f"The user said: '{request.user_input}'. Respond nicely in {request.language}. Introduce yourself exactly as the 'TechStart AI Tutor'. Ask the user if they are ready to start learning about {request.topic}."
    
        
    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

    # Format the prompt
    prompt = alpaca_prompt.format(user_query)

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512, # Increased so answers aren't cut off
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )

    response_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    
    # Clean up output
    response_clean = response_text.split("### Response:")[-1].strip()
    
    # Stop Leakage (In case the model tries to generate another example)
    if "### Instruction:" in response_clean:
        response_clean = response_clean.split("### Instruction:")[0].strip()

    return {"response": response_clean}