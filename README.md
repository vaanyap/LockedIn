**Live Posture Tracking & Productivity Insights**

This project implements a real-time posture tracking system with personalized productivity insights. It leverages MediaPipe for posture detection, integrates Gemini for contextual feedback, and uses GCP for cloud-based inference and analytics.

**Features**
Live Posture Tracking:
- Captures body posture in real-time using MediaPipe and converts raw signals into high-level posture events.
Contextual Feedback & Productivity Insights:
- Integrates Gemini to analyze posture events and provide personalized productivity suggestions via prompt engineering.
Cloud Backend:
- Lightweight backend deployed on Google Cloud Platform (GCP) to handle inference requests, store analytics, and enable downstream applications.
- 
**Tech Stack**
MediaPipe: Real-time body pose detection.
Gemini: Contextual analysis and personalized feedback.
GCP (Cloud Functions / App Engine / Firestore): Backend infrastructure for inference and data storage.
Python / Flask / FastAPI: Backend API handling inference requests.
