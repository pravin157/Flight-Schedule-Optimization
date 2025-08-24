# File: merge_model.py
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- Configuration ---
base_model_id = "Qwen/Qwen2-0.5B-Instruct"
adapter_path = "./qwen2-flight-assistant-final"
merged_model_path = "./merged-flight-assistant-model" # This is the output directory

# --- Load the Base Model and Tokenizer ---
print(f"Loading base model: {base_model_id}")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)

# --- Load the PEFT Adapter ---
print(f"Loading adapter from: {adapter_path}")
model = PeftModel.from_pretrained(base_model, adapter_path)

# --- Merge the Adapter into the Base Model ---
print("Merging the adapter into the base model...")
model = model.merge_and_unload()
print("Merge complete.")

# --- Save the Merged Model ---
print(f"Saving the merged model to: {merged_model_path}")
model.save_pretrained(merged_model_path)
tokenizer.save_pretrained(merged_model_path)
print("✅ Merged model saved successfully!")