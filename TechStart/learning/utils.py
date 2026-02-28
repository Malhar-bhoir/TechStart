import requests
import requests

# def get_ai_tutor_response(mode, topic, language, user_input=""):
#     """
#     Connects to your local FastAPI SLM server.
#     """
#     url = "http://localhost:8001/generate"
#     payload = {
#         "mode": mode,
#         "topic": topic,
#         "language": language,
#         "user_input": user_input
#     }
    
#     try:
#         # 30s timeout as requested due to LLM latency
#         response = requests.post(url, json=payload, timeout=600)
#         response.raise_for_status() 
#         return response.json().get("response", "Error: No response")
#     except requests.exceptions.RequestException as e:
#         return f"AI Server Error: {str(e)}"

def get_ai_tutor_response(mode, topic, language, user_input="", context=""):
    url = "http://localhost:8001/generate" # Ensure port matches your running server
    
    payload = {
        "mode": mode,
        "topic": topic,
        "language": language,
        "user_input": user_input,
        "context": context # <--- Send the context
    }
    
    try:
        response = requests.post(url, json=payload, timeout=3600)
        response.raise_for_status() 
        return response.json().get("response", "Error: No response")
    except requests.exceptions.RequestException as e:
        return f"AI Server Error: {str(e)}"