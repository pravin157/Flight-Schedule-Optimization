# Flight Assistant Project

A local flight analysis assistant combining a fine-tuned Qwen model (served via Ollama) with a Flask backend that can execute structured data analysis functions over historical flight performance datasets.

## Repository Structure

- `App/`
  - `backend.py` – Flask API exposing `/ask` endpoint to interact with the assistant.
  - `analysis_engine.py` – Data analysis functions (traffic, delay prediction, runway, delay reasons, cascading impact).
  - `formatter.py` – Converts JSON analysis outputs into HTML snippets for the frontend/UI.
  - `data_paths.py` – Centralized data path configuration (portable file location resolution).
  - `index.html` – (If used) basic frontend page to query the assistant.
- `Data/` – Local Excel data sources (ignored by git via `.gitignore`).
- `Model/`
  - `Modelfile` – Ollama model recipe referencing merged fine‑tuned weights.
  - `merged-flight-assistant-model/` – Merged base + adapter weights (large; ignored).
  - `qwen2-flight-assistant-final/` – Adapter artifacts from PEFT fine-tuning (ignored).
  - `app.py` – Console interface for direct local model querying (bypasses REST API).
  - `merge_model.py` – (If present) utility for merging base + adapter.
  - `training_data.jsonl` – Structured instruction/chat fine‑tuning data (tracked).
- `requirements.txt` – Python dependencies.
- `.gitignore` – Excludes large model artifacts, raw data files, virtual env, caches.

## Prerequisites

- Python 3.10+
- (Optional) Virtual environment
- Ollama installed and running locally (for serving the merged model) – https://ollama.com
- Sufficient disk space for model weights.

## Setup

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Place the required Excel data files in the `Data/` directory:
- `Chennai_FlightData_Processed.xlsx`
- `cascading_delays.xlsx`
- (Optional) `weather_cascading_delays.xlsx`, `Flight_Summary_By_Hour.xlsx`, `summary_table.xlsx`

## Running the Flask Backend

1. Ensure Ollama has your model available. Build (or rebuild) the model from the Modelfile inside `Model/`:

```cmd
cd Model
ollama create flight-assistant -f Modelfile
```

2. Start Ollama (if not already):

```cmd
ollama serve
```

3. Run the backend API (from repo root or ensure `PYTHONPATH` resolves `App`):

```cmd
venv\Scripts\activate
python -m App.backend
```

The API listens on `http://localhost:5001/ask` expecting JSON: `{ "prompt": "your question" }`.

## Example API Call (PowerShell)
```powershell
Invoke-RestMethod -Uri http://localhost:5001/ask -Method Post -Body '{"prompt":"Show me the best hours to avoid delays"}' -ContentType 'application/json'
```

## Direct Console Mode

Instead of the REST API you can query the model directly:
```cmd
python Model\app.py
```
Type a natural language question; the model responds either with a JSON command (then executed) or a conversational fallback.

## Adding New Analysis Functions

1. Implement function in `App/analysis_engine.py`.
2. Export it in `App/backend.py` TOOLBOX.
3. Add formatting logic (optional) in `App/formatter.py`.
4. Provide an example mapping (system prompt or training data) so the model learns the tool call.

## Data Path Management

All file locations are centralized in `App/data_paths.py`. Use those constants (e.g., `PRIMARY_DATA_FILE`) rather than hardcoding strings to keep portability.

## Training / Fine-Tuning (High Level)

- Base model: `Qwen/Qwen2-0.5B-Instruct`.
- Adapter path: `Model/qwen2-flight-assistant-final/` (PEFT).
- Merge step produces `Model/merged-flight-assistant-model/` which the `Modelfile` references for Ollama.
- Training dataset: `Model/training_data.jsonl`.

(If re‑running fine‑tuning, document scripts & hyperparameters separately.)

## Modelfile Notes

`Model/Modelfile` sets a structured system prompt with examples and a chat template compatible with the merged model to ensure JSON tool-call style outputs.

## Security & Privacy

- Raw operational data remains local; not committed (see `.gitignore`).
- Ensure no secrets are embedded in prompts or training data.

## Troubleshooting

- Missing data file: Confirm placement under `Data/` and filename match.
- Model load OOM: Reduce precision or switch to a smaller base model.
- API returns unknown function: Add the function to `TOOLBOX` and update examples.
- JSON parse error from model: Adjust system prompt examples; keep them minimal and deterministic.

## Future Enhancements

- Add caching layer for repeated queries.
- Implement lightweight front-end UI consuming `/ask`.
- Add unit tests for analysis functions (e.g., with small synthetic DataFrame fixtures).
- Extend dataset ingestion & validation pipeline.

---
© 2025 Flight Assistant Project
