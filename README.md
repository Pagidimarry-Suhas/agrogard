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

**5. Start the Frontend Application**
In a new terminal window:
```bash
streamlit run frontend/streamlit_app.py
```
> The UI will pop open in your browser at http://localhost:8501.

---
*Happy Farming!*
