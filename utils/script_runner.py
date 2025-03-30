import subprocess
import json

def run_script(script_path: str):
    try:
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True
        )
        output= result.stdout.strip()
        return json.loads(output)
    except Exception as e:
        return{"error": str(e)}