# TechStart



# 📘 AI Tutor Backend (SLM Service)

This is the AI Inference Service for the **TechStart AI Tutor** platform.  
It uses **FastAPI** to serve a fine‑tuned **Small Language Model (SLM)** based on **Qwen 2.5 3B**.  
The model is trained to act as a **Tutor**, **Quiz Master**, and **Grader** in three languages: **English, Hindi, and Marathi**.

---

## 🚀 Features
- **3 Distinct Modes**
  - `teach`: Explains concepts simply (Teacher Persona).
  - `quiz`: Generates multiple‑choice questions (Quiz Master Persona).
  - `grade`: Evaluates user answers and provides feedback (Grader Persona).
- **Multi‑Language Support**: English, Hindi (Devanagari), Marathi (Devanagari).
- **Optimized Inference**: Runs on CPU (via `peft/transformers`) or GPU (via `unsloth`).
- **Voice‑Ready**: Designed to work with TTS (Text‑to‑Speech) and STT (Speech‑to‑Text) pipelines.

---

## 🛠️ Tech Stack
- **Framework**: FastAPI + Uvicorn  
- **Model**: Qwen 2.5 3B Instruct (Fine‑Tuned with LoRA)  
- **Libraries**: torch, transformers, peft, accelerate  
- **Python Version**: 3.11 (Recommended for stability)  

---

## 📂 Project Structure
```
fastapi_slm/
│
├── /SLM_Sample            # Fine‑tuned model files
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   ├── tokenizer.json
│   └── ... (other model files)
│
├── main.py                # FastAPI application
├── requirements.txt       # Dependencies list
├── test_api.py            # API verification script
└── README.md              # Documentation
```

---

## ⚙️ Installation

### 1. Prerequisites
- Ensure **Python 3.11** is installed.  
  *(Note: Python 3.13 is currently incompatible with many AI libraries).*

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv myenv3_11
myenv3_11\Scripts\activate

# Mac/Linux
python3 -m venv myenv3_11
source myenv3_11/bin/activate
```

### 3. Install Dependencies
**For CPU Only (Standard Laptop):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

**For NVIDIA GPU:**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

> 💡 If you encounter `PreTrainedModel` import errors:  
> Run:
> ```bash
> pip uninstall transformers peft -y
> pip install transformers peft
> ```

---

## 🏃‍♂️ How to Run

Navigate to the project directory:
```bash
cd fastapi_slm
```

Start the server:
```bash
uvicorn main:app --reload --port 8000
```

Wait for logs to confirm:
```
✅ Model Loaded Successfully!
Application startup complete.
```

---

## 🔌 API Usage

**Endpoint:** `POST /generate`

### Example Request
```json
{
  "mode": "teach",
  "topic": "Python Variables",
  "language": "Marathi"
}
```

### Example Response
```json
{
  "response": "Python Variables म्हणजे काय? \n\nसमजा तुमच्याकडे एक डबा (box) आहे ज्यावर तुम्ही 'Score' असे नाव लिहिले आहे..."
}
```

---

## 🎯 Modes Explained

| Mode   | Purpose                  | Required Fields                          |
|--------|--------------------------|------------------------------------------|
| teach  | Explains a concept       | mode, topic, language                     |
| quiz   | Generates MCQs           | mode, topic, language                     |
| grade  | Evaluates user answers   | mode, topic, language, user_input         |

---

## 🧪 Testing

Verify API is running:
```bash
python test_api.py
```

Or open Swagger UI in your browser:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐛 Troubleshooting

- **Error:** `NotImplementedError: Unsloth currently only works on NVIDIA...`  
  **Fix:** You are trying to use `unsloth` on CPU. Switch `main.py` to use `AutoModelForCausalLM` and `peft`.

- **Error:** `ImportError: cannot import name 'PreTrainedModel'`  
  **Fix:** Your libraries are corrupted. Run:
  ```bash
  pip uninstall transformers peft accelerate -y
  pip cache purge
  pip install transformers peft accelerate
  ```

- **Slow Response?**  
  - On CPU: 10–40 seconds (normal).  
  - On GPU: <2 seconds.

---

## 📜 License

