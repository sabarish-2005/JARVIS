# Deploying JARVIS to Render

## Quick Deploy (Recommended)

### Option 1: Blueprint Auto-Deploy
1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **"New"** → **"Blueprint"**
4. Connect your GitHub repo
5. Render will detect `render.yaml` and deploy both services automatically

---

## Manual Deploy

### Step 1: Deploy Backend API

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Name:** `jarvis-api`
   - **Root Directory:** `jarvis-ai`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements-api.txt`
   - **Start Command:** `gunicorn api_server:app --bind 0.0.0.0:$PORT`
5. Click **"Create Web Service"**
6. Copy the URL (e.g., `https://jarvis-api.onrender.com`)

### Step 2: Deploy Frontend

1. Click **"New"** → **"Static Site"**
2. Connect the same GitHub repo
3. Configure:
   - **Name:** `jarvis-frontend`
   - **Root Directory:** `jarvis-frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Add Environment Variable:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://jarvis-api.onrender.com` (your backend URL from Step 1)
5. Click **"Create Static Site"**

---

## Environment Variables

### Backend (jarvis-api)
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Optional |
| `GOOGLE_API_KEY` | Google Gemini API key | Optional |

### Frontend (jarvis-frontend)
| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | **Yes** |

---

## Post-Deployment

1. **Test Backend:** Visit `https://jarvis-api.onrender.com/api/health`
2. **Test Frontend:** Visit `https://jarvis-frontend.onrender.com`

---

## Troubleshooting

### Backend not starting?
- Check logs in Render dashboard
- Ensure `gunicorn` is in requirements
- Verify `api_server.py` has `app` Flask instance

### Frontend can't connect to API?
- Verify `VITE_API_URL` is set correctly
- Check CORS settings in backend
- Rebuild frontend after changing env vars

### Free tier sleeping?
- Free tier services sleep after 15 mins of inactivity
- First request after sleep takes ~30 seconds
- Consider upgrading for always-on service
