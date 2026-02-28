# TechStart
📘 AI Tutor Backend (SLM Service)This is the AI Inference Service for the TechStart AI Tutor platform. It uses FastAPI to serve a fine-tuned Small Language Model (SLM) based on Qwen 2.5 3B.The model is trained to act as a Tutor, Quiz Master, and Grader in three languages: English, Hindi, and Marathi.🚀 Features3 Distinct Modes:teach: Explains concepts simply (Teacher Persona).quiz: Generates multiple-choice questions (Quiz Master Persona).grade: Evaluates user answers and provides feedback (Grader Persona).Multi-Language Support: English, Hindi (Devanagari), and Marathi (Devanagari).Optimized Inference: Runs on CPU (via peft/transformers) or GPU (via unsloth).Voice-Ready: Designed to work with TTS (Text-to-Speech) and STT (Speech-to-Text) pipelines.🛠️ Tech StackFramework: FastAPI + UvicornModel: Qwen 2.5 3B Instruct (Fine-Tuned with LoRA)Libraries: torch, transformers, peft, acceleratePython Version: 3.11 (Recommended for stability)📂 Project StructurePlaintext/fastapi_slm
│
├── /SLM_Sample            # <--- YOUR FINE-TUNED MODEL FOLDERS
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   ├── tokenizer.json
│   └── ... (other model files)
│
├── main.py                # The main FastAPI application
├── requirements.txt       # Dependencies list
├── test_api.py            # Script to verify the API works
└── README.md              # This file
⚙️ Installation1. PrerequisitesEnsure you have Python 3.11 installed.(Note: Python 3.13 is currently incompatible with many AI libraries).2. Create a Virtual EnvironmentBash# Windows
python -m venv myenv3_11
myenv3_11\Scripts\activate

# Mac/Linux
python3 -m venv myenv3_11
source myenv3_11/bin/activate
3. Install DependenciesFor CPU Only (Standard Laptop):Bashpip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
For NVIDIA GPU:Bashpip install torch --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
(Note: If you encounter PreTrainedModel import errors, run pip uninstall transformers peft -y followed by pip install transformers peft to fix conflicts.)🏃‍♂️ How to RunNavigate to the project directory:Bashcd fastapi_slm
Start the Server:Bashuvicorn main:app --reload --port 8000
Wait for the logs to say:✅ Model Loaded Successfully!Application startup complete.🔌 API UsageEndpoint: POST /generateExample Request (JSON)JSON{
  "mode": "teach",
  "topic": "Python Variables",
  "language": "Marathi"
}
Example ResponseJSON{
  "response": "Python Variables म्हणजे काय? \n\nसमजा तुमच्याकडे एक डबा (box) आहे ज्यावर तुम्ही 'Score' असे नाव लिहिले आहे..."
}
Modes ExplainedModePurposeRequired FieldsteachExplains a concept.mode, topic, languagequizAsks a question.mode, topic, languagegradeCorrects a user answer.mode, topic, language, user_input🧪 TestingYou can verify the API is running using the included test script:Bashpython test_api.py
Or open your browser to http://localhost:8000/docs to use the interactive Swagger UI.🐛 TroubleshootingError: NotImplementedError: Unsloth currently only works on NVIDIA...Fix: You are trying to use unsloth on a CPU. Switch the code in main.py to use AutoModelForCausalLM and peft instead.Error: ImportError: cannot import name 'PreTrainedModel'Fix: Your libraries are corrupted. Run:pip uninstall transformers peft accelerate -ypip cache purgepip install transformers peft accelerateSlow Response?On CPU, it is normal for a response to take 10-40 seconds. On GPU, it takes <2 seconds.
