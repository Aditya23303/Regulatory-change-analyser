import json
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_prompt(old_text=None, new_text=None):
    prompt = "You are an expert in regulatory analysis.\n\nAnalyze the following change in the regulatory document.\n\n"
    if old_text:
        prompt += f"OLD TEXT:\n{old_text}\n\n"
    if new_text:
        prompt += f"NEW TEXT:\n{new_text}\n\n"

    prompt += """Provide the following JSON output:
{
  "change_summary": "...",
  "change_type": "New Requirement / Clarification of Existing Requirement / Deletion of Requirement / Minor Edit"
}"""

    return prompt

def call_llm(prompt):
    payload = {
        "model": "phi3",   
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    return result['response']

def extract_json(llm_output):
    try:
        json_part = llm_output[llm_output.find('{'):llm_output.rfind('}')+1]
        return json.loads(json_part)
    except:
        return {"change_summary": "Parsing failed", "change_type": "Unknown"}
