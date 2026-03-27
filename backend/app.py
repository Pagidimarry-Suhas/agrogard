from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.model_loader import WeedDetectionModel

app = FastAPI(title="AgroGard Simplified API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def load_model():
    app.state.model = WeedDetectionModel.get_instance()

@app.get("/")
async def root():
    return {"message": "Welcome to AgroGard API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint for predicting weed/crop from an image.
    Works for both uploaded files and camera captures.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Read image bytes
        image_bytes = await file.read()

        # Process and predict
        prediction_result = app.state.model.predict(image_bytes)

        return {
            "prediction": prediction_result.get("prediction", "Unknown"),
            "confidence": prediction_result.get("confidence", 0.0),
            "image_b64": prediction_result.get("image_b64", None)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
