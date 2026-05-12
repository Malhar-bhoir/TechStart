

---

```markdown
# 🚀 TechStart: AI-Powered Interactive Learning Management System

TechStart is a next-generation, AI-driven Learning Management System (LMS) developed as a Major Project.  
It bridges the gap between theoretical learning and practical execution. Unlike traditional platforms, TechStart features a custom Fine-Tuned Small Language Model (SLM), browser-based OS/Office simulations, and in-browser coding IDEs to allow users to practice real-world skills instantly.

---

## ✨ Key Features

### 🧠 Custom AI Tutor (FastAPI + Hugging Face)
- Local SLM Integration: Powered by an open-weight model (e.g., Qwen 2.5) running on a dedicated FastAPI server.
- Auto-Hardware Detection: Automatically detects and utilizes NVIDIA CUDA GPUs for 10x–50x faster inference, with CPU fallback.
- Context-Aware Chat: The AI knows exactly which topic you are on and grades your practical tasks.
- **3 Distinct Modes**:
  - `teach`: Explains concepts simply (Teacher Persona).
  - `quiz`: Generates multiple-choice questions (Quiz Master Persona).
  - `grade`: Evaluates user answers and provides feedback (Grader Persona).

### 🌐 Multilingual Accessibility
- Text-to-Speech (TTS): Native browser voice synthesis with fallback algorithms. Auto-detects Devanagari script to switch to Hindi/Marathi voices.
- Speech-to-Text (STT): Voice-activated input for hands-free learning.
- UI Translations: Seamlessly switch between English, Hindi, and Marathi.

### 🖥️ Web-Based Practical Simulations (Zero Install Required)
- **Windows OS Simulator**: Context menus, folder creation, file explorer tasks (Ctrl+C, Ctrl+V, Delete).
- **Web Browser Simulator**: Interactive Chrome-like environment for tabs and bookmarks.
- **MS Office Suite Simulators**:
  - Excel: Formula bar with auto-grading for `=SUM()`, basic math, and `MAX()`.
  - Word: Interactive ribbon for Text Emphasis (Bold) and Paragraph Alignment.
  - PowerPoint: Slide creation (Ctrl+M) and Presentation Mode (F5).

### 👨‍💻 In-Browser Programming IDEs
- Python (via Pyodide): Runs entirely in the browser using WebAssembly.
- C, C++, Java (via Piston API): Remote compilation and execution with real-time terminal output.
- Auto-Grading: Hidden test cases evaluate code output and update progress.

### 📈 Student Analytics & Gamification
- Curriculum Heatmap: GitHub-style contribution grid tracking mastered vs. locked topics.
- Advanced Metrics: Real-time progress percentage and AI-quiz accuracy.
- Seamless Authentication: 1-click Google OAuth login.

---

## 🛠️ Technology Stack

**Frontend**  
- HTML5, CSS3, Vanilla JavaScript  
- Tailwind CSS (Modern, responsive UI)  
- Web Speech API (TTS/STT)  

**Main Backend (Web App)**  
- Django (Python Web Framework)  
- SQLite / PostgreSQL  
- Django Allauth (Google OAuth Integration)  

**AI Backend (Inference Server)**  
- FastAPI (High-performance API)  
- PyTorch & Transformers (Hugging Face)  
- Hardware Auto-Detection (CUDA/CPU)  

**External Tools**  
- Pyodide: WebAssembly Python environment  
- Piston API: Code execution engine for C, C++, Java  

---

## 📂 Project Structure

```
TechStart/
│
├── fastapi_slm/           # AI Tutor Backend
│   ├── SLM_Sample         # Fine-tuned model files
│   ├── main.py            # FastAPI application
│   ├── requirements.txt   # Dependencies
│   └── test_api.py        # API verification script
│
├── django_app/            # Main LMS Web App
│   ├── manage.py
│   ├── requirements.txt
│   └── ...
```

---

## ⚙️ Local Installation & Setup

This project uses a **Dual-Server Architecture**. You need to run both the Django Web Server and the FastAPI AI Server.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/TechStart.git
cd TechStart
```

### 2. Setup the AI Inference Server (FastAPI)
```bash
cd fastapi_slm
python -m venv venv
# Activate venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install fastapi uvicorn pydantic transformers
# For GPU support:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

uvicorn main:app --reload --port 8001
```

### 3. Setup the Main Web App (Django)
```bash
cd django_app
python -m venv venv
# Activate venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

# Setup Environment Variables
# Create a .env file based on .env.example and add SECRET_KEY + Google OAuth Keys.

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000). The platform will automatically communicate with the FastAPI server on port 8001.

---

## 🔌 API Usage (AI Tutor Backend)

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
  "response": "Python Variables म्हणजे काय? ... (explanation in Marathi)"
}
```

---

## 🧪 Testing

Verify API is running:
```bash
python test_api.py
```

Or open Swagger UI:  
👉 `http://localhost:8001/docs` [(localhost in Bing)](https://www.bing.com/search?q="http%3A%2F%2Flocalhost%3A8001%2Fdocs")

---

## 🐛 Troubleshooting

- **Error:** `NotImplementedError: Unsloth currently only works on NVIDIA...`  
  **Fix:** Switch to `AutoModelForCausalLM` with `peft` for CPU.

- **Error:** `ImportError: cannot import name 'PreTrainedModel'`  
  **Fix:**  
  ```bash
  pip uninstall transformers peft accelerate -y
  pip cache purge
  pip install transformers peft accelerate
  ```

- **Slow Response?**  
  - CPU: 10–40 seconds (normal).  
  - GPU: <2 seconds.

---

## 📸 Screenshots
(Add high-quality screenshots before submission)
- AI Chat Interface  
- Fake Windows/Excel Simulation  
- Python/C++ Web IDE  
- Analytics Dashboard & Heatmap  

---

## 📝 License
This project was developed for educational purposes as a Major University Project.

---


```

---

