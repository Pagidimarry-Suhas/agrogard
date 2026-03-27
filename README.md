# 🌱 AgroGard - AI Powered Weed Detection System

A lightweight, minimal web application designed to detect weeds using an AI custom model.
Built with **FastAPI** (Backend) and **Streamlit** (Frontend).

## 🚀 Features
- **Clean Interface:** Single-page dashboard focused completely on inference.
- **Dual Input Options:** Upload a file from your hard drive or use your device camera directly in the browser.
- **YOLOv11 AI Engine:** Pluggable PyTorch/ultralytics model backend loader.
- **Local History Export:** Predictions are saved to your active browser session and can be downloaded as a standard `.csv` file!

---

## 📁 Project Structure

```text
agrogard/
├── frontend/
│   └── streamlit_app.py      # Main UI application
├── backend/
│   ├── app.py                # FastAPI routing
│   └── model_loader.py       # YOLOv11 Model inference setup
├── utils/
│   └── preprocessing.py      # Basic image parsing utilities
├── model/
│   └── best.pt               # Your YOLOv11 weights
└── requirements.txt          # Minimal Python dependencies
```

---

## 🛠️ Setup Instructions

**1. Create a Python Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

*(Note: If you run into Wheel build errors involving Rust/pydantic, you might need to use Python 3.11/3.12 instead of 3.14 alpha!)*

**3. Add Your Machine Learning Model**
- Place your trained YOLOv11 model (`best.pt`) explicitly into a folder named `model/` at the root of the project.

**4. Start the Backend Server**
```bash
uvicorn backend.app:app --reload --port 8000
```
> The API will be running at http://localhost:8000.

---

## 🌍 How to Deploy (To the Cloud for Free)

Because AgroGard is split into a **Frontend** and a **Backend**, you must deploy them separately. The easiest and completely free way to do this is using **Render** for the API and **Streamlit Cloud** for the UI.

### Step 1: Push Code to GitHub
Ensure all your files (including `requirements.txt` and the `model/best.pt` file) are uploaded to a public or private repository on your GitHub account.

### Step 2: Deploy the Backend (FastAPI) on Render
1. Go to [Render.com](https://render.com) and sign in.
2. Click **New +** > **Web Service**.
3. Connect your GitHub account and select your `agrogard` repository.
4. Settings to use:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**. 
6. Wait for it to build and deploy. Once live, copy your backend URL (e.g., `https://agrogard.onrender.com`).

### Step 3: Deploy the Frontend (Streamlit)
1. Go to [Streamlit Community Cloud](https://share.streamlit.io) and sign in with GitHub.
2. Click **New App**.
3. Select your `agrogard` repository.
4. Set the **Main file path** to: `frontend/streamlit_app.py`
5. Click **Advanced Settings**:
   - Under **Secrets**, you must tell the frontend where your new Render backend is! Add the following line:
     ```toml
     API_URL = "https://agrogard.onrender.com"
     ```
     *(Make sure to replace the URL with your actual Render URL from Step 2)*
6. Click **Deploy!**

Your beautiful AgroGard dashboard will now be live on the internet! 🌿
