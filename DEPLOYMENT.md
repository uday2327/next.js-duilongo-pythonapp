# Deployment Guide

## Overview

This project is a full-stack language learning app with:
- **Frontend**: Next.js (React)
- **Backend**: FastAPI (Python)
- **Database**: SQLite (persistently stored)

## Critical: SQLite Persistence on Render

Render's default filesystem is **ephemeral** — files are deleted when your service restarts or redeploys. Since this assignment requires SQLite, you **must** use a **persistent disk** to keep your database.

### Option 1: Render Persistent Disk (Recommended)

#### Step 1: Enable Persistent Disk
1. Go to your Render service dashboard
2. Navigate to **Environment** → **Disks**
3. Add a new persistent disk:
   - **Mount Path**: `/var/data`
   - **Size**: 1GB (free tier allows this)

#### Step 2: Update Backend `.env`
```env
DATABASE_URL=sqlite:////var/data/duolingo_clone.db
FRONTEND_URL=https://your-frontend-url.onrender.com
```

**Important**: Note the **four slashes** (`////`) in the path:
- First two (`//`) = file URL protocol
- Second two (`//`) = absolute path starting at `/var/data`

#### Step 3: Deploy Backend
Push your changes and Render will redeploy with the persistent disk mounted.

---

## Deployment Steps

### Backend (FastAPI)

#### 1. Create Render Web Service
```bash
git push  # Push to your repository
```

Visit https://dashboard.render.com and create a new Web Service:
- **Repository**: Your GitHub repo
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 2. Add Environment Variables
In Render dashboard **Environment** tab:
```
DATABASE_URL=sqlite:////var/data/duolingo_clone.db
FRONTEND_URL=https://your-frontend-url.onrender.com
```

#### 3. Add Persistent Disk (Critical!)
- Mount Path: `/var/data`
- Size: 1GB

#### 4. Verify
Visit: `https://your-backend-url.onrender.com/api/health`

Should return:
```json
{"ok": true}
```

---

### Frontend (Next.js)

#### 1. Deploy to Vercel (Easiest)
```bash
npm install -g vercel
vercel --prod
```

Or connect your GitHub repo directly at https://vercel.com

#### 2. Set Environment Variables
In Vercel dashboard **Settings** → **Environment Variables**:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

#### 3. Verify
Visit your frontend URL — should load without API errors.

---

### Alternative: Deploy Both on Render

If deploying both on Render:

1. Create a Render Web Service for backend (steps above)
2. Create another Render Static Site for frontend:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/.next`
   - Note: This works if you're okay with static export; otherwise use Web Service for Next.js

---

## Local Development

### Quick Start
```bash
# Terminal 1: Backend
cd backend
python -m pip install -r requirements.txt
export PYTHONPATH=.
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000

---

## Testing Your Deployment

### 1. Health Check
```bash
curl https://your-backend-url.onrender.com/api/health
# Should return: {"ok":true}
```

### 2. API Connectivity
Open frontend in browser, check:
- Login page loads
- Leaderboard fetches data
- No CORS errors in browser console

### 3. Database Persistence
- Login and play lessons
- Redeploy backend
- Verify data persists (check leaderboard)

---

## Troubleshooting

### "Database file not found" after restart
- ❌ Your persistent disk isn't configured
- ✅ Add disk at `/var/data` in Render dashboard
- ✅ Update `DATABASE_URL` to `/var/data/duolingo_clone.db`

### "ModuleNotFoundError: No module named 'app'"
- ❌ Wrong working directory
- ✅ Use `cd backend &&` in start command

### "CORS error in browser"
- ❌ `FRONTEND_URL` doesn't match your actual frontend URL
- ✅ Update in backend `.env`: `FRONTEND_URL=https://your-frontend-url`

### "Hydration mismatch" errors
- ✅ Already fixed in `Header.tsx` — redeploy frontend

---

## Security Notes

For production (beyond this assignment):
- Use a real database (PostgreSQL, MySQL)
- Add JWT authentication
- Use environment secrets (never commit `.env`)
- Enable HTTPS (automatic on Render/Vercel)
- Set secure CORS origins (not `*`)

---

## File Structure

```
duilongo-nextjs-app/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── database.py        # SQLite configuration
│   │   ├── models.py          # Database models
│   │   ├── routes/            # API endpoints
│   │   └── services/          # Business logic
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Backend config (not in git)
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js pages
│   │   ├── components/        # React components
│   │   └── lib/api.ts         # API client
│   ├── package.json           # Node dependencies
│   └── .env.local             # Frontend config (not in git)
└── DEPLOYMENT.md              # This file
```

---

## Questions?

See `README.md` for project overview and tech stack details.
