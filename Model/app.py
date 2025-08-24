# File: app.py
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from App.analysis_engine import (
    get_airport_traffic_analysis,
    find_high_impact_flights,
    predict_delay,
    get_runway_analysis,  # Corrected to match your engine
    get_delay_reason_analysis    # Added the new function
)

# --- Load the Fine-Tuned Model ---
base_model_id = "Qwen/Qwen2-0.5B-Instruct"
adapter_path = "./qwen2-flight-assistant-final"

print("Loading base model (this may take a moment)...")
model = AutoModelForCausalLM.from_pretrained(base_model_id, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

print("Loading fine-tuned adapter...")
model = PeftModel.from_pretrained(model, adapter_path)
model.eval()

def query_assistant(user_prompt):
    """Gets a response from the fine-tuned LLM."""
    
    # This "cheat sheet" is expanded to guide the model on all its skills.
    messages = [
        {"role": "system", "content": "You are a helpful flight analysis assistant. You convert user questions into structured JSON commands."},
        # Example 1: Traffic Analysis
        {"role": "user", "content": "Show me the best hours to avoid delays."},
        {"role": "assistant", "content": "{\"function\": \"get_airport_traffic_analysis\", \"params\": {\"airport_code\": \"default\"}}"},
        # Example 2: Runway Analysis (Corrected function name)
        {"role": "user", "content": "How many runways does Chennai have?"},
        {"role": "assistant", "content": "{\"function\": \"get_airport_runway_analysis\", \"params\": {\"airport_code\": \"MAA\"}}"},
        # Example 3: Delay Reason Analysis (New example)
        {"role": "user", "content": "What's the average delay due to weather?"},
        {"role": "assistant", "content": "{\"function\": \"get_delay_reason_analysis\", \"params\": {\"delay_reason\": \"Weather\"}}"},
        # The actual user prompt:
        {"role": "user", "content": user_prompt}
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(**model_inputs, max_new_tokens=256, eos_token_id=tokenizer.eos_token_id)
    
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def main():
    """Main application loop."""
    print("\n✈️  Flight Analysis Assistant is ready!")
    print("Type your question or 'exit' to quit.")
    
    while True:
        prompt = input("\n> ")
        if prompt.lower() == 'exit':
            break

        print("\n🤖 Thinking...")
        model_response = query_assistant(prompt)
        
        try:
            command = json.loads(model_response)
            function_name = command.get('function')
            params = command.get('params', {})

            print(f"🔍 LLM generated command: {json.dumps(command)}")

            # This logic block is now fully updated and correct
            if function_name == "get_airport_traffic_analysis":
                result = get_airport_traffic_analysis(**params)
            elif function_name == "predict_delay":
                result = predict_delay(**params)
            elif function_name == "find_high_impact_flights":
                result = find_high_impact_flights(**params)
            elif function_name == "get_airport_runway_analysis":
                result = get_runway_analysis(**params)
            elif function_name == "get_delay_reason_analysis":
                result = get_delay_reason_analysis(**params)
            else:
                result = {"error": f"Unknown function: {function_name}"}

            print("\n✅ Result:")
            print(json.dumps(result, indent=2))
        
        except (json.JSONDecodeError, IndexError):
            print("\n✅ Conversational Response:")
            print(model_response)

if __name__ == "__main__":
    main()
