# Vaani AI Assistant

A simple ChatGPT-style Streamlit application for Vaani using an OpenAI-compatible API through OpenRouter.

## Files

- `app.py` - Streamlit application
- `requirements.txt` - Python dependencies
- `.gitignore` - Prevents secrets and Python temporary files from being committed
- `.streamlit/secrets.toml.example` - Example secret configuration

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this project folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.streamlit/secrets.toml` from `.streamlit/secrets.toml.example` and put your OpenRouter API key there.
5. Start the app:

```bash
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, `.gitignore`, `.streamlit/secrets.toml.example`, and `README.md`.
3. Do NOT upload `.streamlit/secrets.toml`.
4. In Streamlit Community Cloud, create a new app and select:
   - Repository: your GitHub repository
   - Branch: `main`
   - Main file: `app.py`
5. Open the app's Settings/Secrets and add:

```toml
OPENROUTER_API_KEY = "YOUR_REAL_API_KEY"
```

6. Save and redeploy.

## Model

The default model is:

`openrouter/free`

This lets OpenRouter route the request to an available free model. Free model availability and rate limits can change, so the model can also be changed from the sidebar.

## Security

Never put your API key directly inside `app.py`, commit it to GitHub, or share it publicly.
