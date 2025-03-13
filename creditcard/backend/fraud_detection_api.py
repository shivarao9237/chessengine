from fastapi import FastAPI, HTTPException
import uvicorn
import numpy as np
import joblib  # To load the trained model
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load the trained model
model = joblib.load("fraud_detection_model.pkl")  # Ensure this file exists

# Define FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class Transaction(BaseModel):
    features: list  # List of features for prediction

@app.post("/predict")
def predict_fraud(transaction: Transaction):
    try:
        # Convert input data to NumPy array and reshape for prediction
        data = np.array(transaction.features).reshape(1, -1)
        prediction = model.predict(data)
        
        return {"fraud": bool(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
