# Epoch — World Events in Real Time

An interactive 3D globe that shows real-time global news and crisis events. Click any country on the globe to get a Gemini-powered news summary read aloud by ElevenLabs, with headlines displayed in a sleek side panel.

## Setup

### 1. Get API Keys

- **Gemini**: https://aistudio.google.com/apikey
- **ElevenLabs**: https://elevenlabs.io (Settings → API Keys)
- **NewsAPI**: https://newsapi.org/register (free tier available)
- **Cesium Ion**: https://cesium.com/ion/tokens (free token)

### 2. Backend Setup

```bash
cd epoch-api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `epoch-api/.env` file with your API keys:

```
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd epoch-web
npm install
```

Create `epoch-web/.env` file with your Cesium token:

```
VITE_CESIUM_TOKEN=your_cesium_ion_token_here
```

Start the frontend development server:

```bash
npm run dev
```

### 4. Open the Application

Navigate to http://localhost:5173 in your browser.

Click any country on the globe to see real-time news summaries and hear them read aloud!

## Project Structure

```
epoch/
├── epoch-api/          # FastAPI backend
│   ├── main.py         # FastAPI app entry point
│   ├── routers/        # API route handlers
│   └── services/       # News, Gemini, ElevenLabs services
└── epoch-web/          # React + Vite frontend
    ├── src/
    │   ├── components/ # React components (Globe, CountryPanel, etc.)
    │   └── lib/        # API client
    └── index.html      # HTML entry point
```

## Features

- **Interactive 3D Globe**: Powered by CesiumJS with 50+ clickable countries
- **Real-time News**: Fetches latest headlines from NewsAPI with GDELT fallback
- **AI Summarization**: Gemini 2.0 Flash generates natural news anchor summaries
- **Text-to-Speech**: ElevenLabs provides realistic voice narration
- **Modern UI**: Sleek dark theme with smooth animations

## Technology Stack

**Backend:**
- FastAPI
- Google Gemini API
- ElevenLabs API
- NewsAPI / GDELT

**Frontend:**
- React 18
- Vite
- CesiumJS
- Tailwind CSS

## Notes

- The backend runs on port 8000
- The frontend runs on port 5173 (Vite default)
- CORS is configured to allow requests from localhost:5173
- All audio is returned as base64-encoded MP3 data
