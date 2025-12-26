# Connecting JARVIS Frontend to Flask Backend

## Overview
The JARVIS frontend is now connected to the Python Flask backend API. This document explains how to run both components together.

## Prerequisites
- Python 3.8+ installed
- Node.js 18+ installed
- All dependencies installed for both backend and frontend

## Setup Instructions

### 1. Install Backend Dependencies
```bash
cd jarvis-ai
pip install -r requirements-api.txt
```

### 2. Install Frontend Dependencies
```bash
cd jarvis-frontend
npm install
```

### 3. Configure Environment Variables
The frontend is pre-configured to connect to `http://localhost:5000`. If you need to change the API URL:

1. Copy `.env.example` to `.env`
2. Update `VITE_API_URL` with your Flask server URL

```bash
# In jarvis-frontend/.env
VITE_API_URL=http://localhost:5000
```

## Running the Application

### Option 1: Run Separately (Recommended for Development)

**Terminal 1 - Start Flask Backend:**
```bash
cd jarvis-ai
python api_server.py
```
The Flask server will start on http://localhost:5000

**Terminal 2 - Start Frontend:**
```bash
cd jarvis-frontend
npm run dev
```
The Vite dev server will start on http://localhost:5173

### Option 2: Use Start Scripts

**Windows:**
```bash
# Start Flask API
cd jarvis-ai
.\start-api-server.bat

# Start Frontend (in another terminal)
cd jarvis-frontend
npm run dev
```

## API Integration Features

### 1. Chat & Command Processing
- User messages are sent to `/api/chat` or `/api/command` endpoints
- Commands are processed by the intent parser and action executor
- Responses are displayed in real-time

### 2. Voice Integration
- Voice input is captured via `/api/listen`
- Transcribed text is processed as commands
- Text-to-speech via `/api/speak` (when implemented)

### 3. System Status Monitoring
- Frontend checks `/api/health` every 10 seconds
- Connection status displayed in System Stats panel
- Real-time component status updates

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/status` | GET | System status |
| `/api/chat` | POST | Send chat messages |
| `/api/command` | POST | Execute commands |
| `/api/listen` | POST | Voice input |
| `/api/speak` | POST | Text-to-speech |

## Troubleshooting

### Frontend can't connect to backend
1. Ensure Flask server is running on port 5000
2. Check `.env` file has correct API URL
3. Verify CORS is enabled in Flask (already configured)
4. Check browser console for connection errors

### Voice features not working
1. Ensure microphone permissions are granted
2. Check Flask backend has voice_engine initialized
3. Verify audio input device is working

### Commands not executing
1. Check Flask logs for errors
2. Verify intent_parser and action_executor are initialized
3. Test endpoints directly with curl or Postman

## Testing the Connection

Open browser console and check:
- Network tab shows successful API calls
- System Stats panel shows "LIVE" status
- Messages get actual responses from Flask API

Or test manually:
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello JARVIS"}'
```

## Development Tips

1. **Hot Reload**: Frontend hot-reloads automatically, Flask needs manual restart
2. **Debugging**: Check Flask terminal for backend logs
3. **API Changes**: Update `src/services/api.ts` when adding new endpoints
4. **Types**: TypeScript interfaces in api.ts match Flask response formats

## Architecture

```
┌─────────────────┐         HTTP/REST API         ┌──────────────────┐
│  React Frontend │◄──────────────────────────────►│  Flask Backend   │
│  (Port 5173)    │                                │  (Port 5000)     │
└─────────────────┘                                └──────────────────┘
        │                                                   │
        ├─ API Service (api.ts)                           ├─ Voice Engine
        ├─ System Status Hook                             ├─ Intent Parser
        ├─ Voice Integration                              ├─ Action Executor
        └─ UI Components                                  └─ AI Brain
```

## Next Steps

- Add authentication if needed
- Implement WebSocket for real-time updates
- Add error boundary components
- Enhance voice recognition features
- Add command history and favorites
