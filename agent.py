import json
import subprocess
import urllib.request
import urllib.error

# Set your model name (e.g., "gemma", "gemma:2b", "gemma2", "llama3")
MODEL = "gemma4:e2b" 
OLLAMA_URL = "http://localhost:11434/api/generate"

# Get user input from terminal
user_request = input("Enter your instruction for Mac (e.g., 'Check free disk space'): ")

prompt = f"""You are a Mac operations agent.
Output ONLY the Mac Bash command required to satisfy the request in the following JSON format. Do not include any other text.

{{"command": "command_to_run"}}

Request: {user_request}
"""

payload = json.dumps(
    {"model": MODEL, "prompt": prompt, "format": "json", "stream": False}
).encode("utf-8")

req = urllib.request.Request(
    OLLAMA_URL,
    data=payload,
    headers={"Content-Type": "application/json"},
)

try:
    with urllib.request.urlopen(req) as res:
        response = json.loads(res.read().decode("utf-8"))

    # Extract command from JSON response
    cmd_data = json.loads(response["response"])
    command = cmd_data.get("command")

    print(f"\n[AI Suggested Command]: {command}")
    confirm = input("Do you want to execute this command on your Mac? (y/N): ")

    if confirm.lower() == "y":
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        print("\n--- Execution Output ---")
        print(result.stdout if result.returncode == 0 else result.stderr)
    else:
        print("Execution canceled.")

except urllib.error.HTTPError as e:
    if e.code == 404:
        print(f"Error: Model '{MODEL}' not found (404).")
        print("Run `ollama list` in your terminal to check installed model names and update the MODEL variable in this script.")
    else:
        print(f"HTTP Error occurred: {e}")