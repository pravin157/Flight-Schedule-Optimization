# File: backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

# Import the analysis engine functions
from App.analysis_engine import (
    get_airport_traffic_analysis,
    predict_delay,
    get_runway_analysis,
    get_delay_reason_analysis,
    find_high_impact_flights
)
# STEP 1: Import the new formatter function
from App.formatter import format_response

# The toolbox remains the same
TOOLBOX = {
    "get_airport_traffic_analysis": get_airport_traffic_analysis,
    "predict_delay": predict_delay,
    "get_runway_analysis": get_runway_analysis,
    "get_delay_reason_analysis": get_delay_reason_analysis,
    "find_high_impact_flights": find_high_impact_flights,
}

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/ask', methods=['POST'])
def ask_assistant():
    user_prompt = request.json.get('prompt')
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    print(f"Received prompt: {user_prompt}")

    try:
        ollama_payload = { "model": "flight-assistant", "prompt": user_prompt, "stream": False }
        response = requests.post(OLLAMA_API_URL, json=ollama_payload)
        response.raise_for_status()
        
        ollama_response_text = response.json().get('response', '{}')
        print(f"Ollama response: {ollama_response_text}")
        
        json_response = ollama_response_text[ollama_response_text.find('{'):ollama_response_text.rfind('}')+1]
        command = json.loads(json_response)
        function_name = command.get('function')
        params = command.get('params', {})

    except (requests.RequestException, json.JSONDecodeError, IndexError) as e:
        print(f"Error getting command from Ollama or parsing it: {e}")
        return jsonify({"type": "conversational", "content": ollama_response_text or "Sorry, I had trouble understanding that."})

    if function_name in TOOLBOX:
        try:
            function_to_call = TOOLBOX[function_name]
            result = function_to_call(**params)
            print(f"Execution result: {result}")

            # STEP 2: Use the formatter to convert the JSON result into HTML
            formatted_content = format_response(function_name, result)
            
            # Send the final formatted HTML to the frontend
            return jsonify({"type": "data", "content": formatted_content})

        except Exception as e:
            print(f"Error executing function '{function_name}': {e}")
            return jsonify({"type": "error", "content": f"An error occurred while executing the command: {e}"}), 500
    else:
        print(f"Unknown function called: {function_name}")
        return jsonify({"type": "error", "content": f"The model tried to call an unknown function: '{function_name}'"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
