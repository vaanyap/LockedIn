# LockedIn

LockedIn is a student productivity dashboard that combines goal tracking, live posture monitoring, and optional Gemini-powered academic support. The project is meant to show applied AI product work rather than a single isolated model demo.

## What it includes

- A Streamlit dashboard for goals, focus, and study support.
- A Flask-based posture monitoring experience powered by MediaPipe and OpenCV.
- A yoga pose prompt-to-code generator.
- An optional AI study assistant backed by Vertex AI and Google Cloud Storage.

## Features

- It combines UI, backend integration, computer vision, and generative AI in one project.
- The core experience still works locally even when cloud AI credentials are unavailable.
- The posture-monitoring backend is separated from the Streamlit dashboard, which makes the architecture easier to explain.

## Stack

- Python
- Streamlit
- Flask
- MediaPipe
- OpenCV
- Vertex AI
- Google Cloud Storage

## Run locally

Use Python 3.9 to 3.11 for best compatibility with MediaPipe.

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Start the posture backend in one terminal:

```bash
python poseDetection.py
```

Start the dashboard in another terminal:

```bash
streamlit run app.py
```

## Optional AI setup

For the Study Buddy and yoga code generation features, configure Google Cloud credentials and optionally set these environment variables:

```bash
export VERTEX_PROJECT_ID="your-project-id"
export VERTEX_LOCATION="us-central1"
export LOCKEDIN_BUCKET="your-bucket-name"
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/service-account.json"
```

If these are not configured, the app will still load and show a fallback experience.

## Vercel deployment

This repository now includes a Vercel-friendly static showcase layer.

- Deploying to Vercel serves [index.html](index.html), which presents the project, architecture, setup flow, and resume-ready framing.
- The full Streamlit dashboard and webcam posture monitor still run locally.
- This split is intentional because Vercel is a good fit for a public-facing portfolio page, but not for a persistent webcam stream or server-side MediaPipe runtime.

To deploy:

```bash
vercel
```

Or import the GitHub repository directly in the Vercel dashboard and deploy with the default static-site settings.
