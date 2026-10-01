# LockedIn

LockedIn is a student productivity dashboard that combines goal tracking, live posture monitoring, and optional Gemini-powered academic support. The project is meant to show applied AI product work rather than a single isolated model demo.

CHECK OUR DEVPOST:
**https://devpost.com/software/lockedin-k35v4y**


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
