# Carlo Health Backend

FastAPI backend for the Carlo Health Chatbot. Wraps Groq API and exposes a standard `/chat` endpoint for Carlo enforcement connection.

## Local Development

```bash
pip install -r requirements.txt
GROQ_API_KEY=your_key uvicorn main:app --reload
```

Visit `http://localhost:8000`

## Deploy to Render

1. Push to GitHub
2. Go to render.com → New → Web Service → connect repo
3. Add environment variable: `GROQ_API_KEY`
4. Deploy

## Carlo Enforcement Connection

Once deployed, use these values in Carlo dashboard:

- **API Endpoint URL:** `https://your-render-url.onrender.com/chat`
- **API Key:** your Groq API key
- **Auth Type:** Bearer Token
- **Request Structure:**
```json
{"messages": [{"role": "user", "content": "Hello"}], "model": "llama-3.3-70b-versatile", "max_tokens": 100}
```
- **Response Structure:**
```json
{"choices": [{"message": {"content": "Hi"}}]}
```
- Select `"Hello"` as request text field, `"Hi"` as response text field
