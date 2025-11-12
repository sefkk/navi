# Railway Deployment Guide

## Quick Deploy Steps

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Configure for Railway deployment"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your `navi` repository
   - Railway will automatically:
     - Detect Python
     - Install dependencies from `requirements.txt`
     - Use `Procfile` to start the app
     - Assign a public URL

3. **That's it!** Your app will be live in ~2-3 minutes.

## Configuration Files

- ✅ `Procfile` - Tells Railway how to start the app
- ✅ `railway.json` - Railway-specific configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Configured to use PORT environment variable

## After Deployment

Railway will provide you with:
- A public URL (e.g., `https://navi-production.up.railway.app`)
- Automatic HTTPS
- Environment variable management
- Logs and metrics

## Troubleshooting

If deployment fails:
1. Check Railway logs in the dashboard
2. Ensure all files are committed to GitHub
3. Verify `requirements.txt` has all dependencies
4. Make sure `Procfile` is in the root directory

## Cost

- Free tier: $5/month credit
- Your app will likely stay within free tier limits
- Railway charges per hour of usage

