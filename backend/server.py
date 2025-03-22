from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, model_validator
from typing import Literal
import logging
import traceback
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load training data for medians
try:
    df = pd.read_csv("model/earthquake_1995-2023.csv")
    features = ["latitude", "longitude", "depth", "cdi", "mmi", "tsunami", "sig", "dmin", "gap", "nst", "magType"]
    numerical_features = ["latitude", "longitude", "depth", "cdi", "mmi", "tsunami", "sig", "dmin", "gap", "nst"]
    categorical_features = ["magType"]

    # Calculate medians for numerical features
    feature_medians = {}
    for col in numerical_features:
        feature_medians[col] = float(df[col].median())

    # Load the trained model (which includes preprocessing)
    model = joblib.load("model/earthquake_model.pkl")
    logger.info("Model loaded successfully")
    logger.info(f"Model type: {type(model)}")
    logger.info(f"Model steps: {model.named_steps}")

except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    raise

# Initialize FastAPI app
app = FastAPI(
    title="Earthquake Magnitude Prediction API",
    description="API for predicting earthquake magnitudes based on seismic data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EarthquakeFeatures(BaseModel):
    latitude: float = Field(ge=-90, le=90, description="Latitude of the earthquake (-90 to 90)")
    longitude: float = Field(ge=-180, le=180, description="Longitude of the earthquake (-180 to 180)")
    depth: float = Field(ge=0, description="Depth of the earthquake in kilometers")
    magType: Literal["mww", "Mi", "mb", "ms", "md", "ml"] = Field(description="Type of magnitude measurement")
    cdi: float = Field(ge=0, le=12, description="Community Decimal Intensity (0-12)")
    mmi: float = Field(ge=0, le=12, description="Modified Mercalli Intensity (0-12)")
    tsunami: int = Field(ge=0, le=1, description="Tsunami flag (0 or 1)")
    sig: float = Field(ge=0, description="Significance of the event")
    dmin: float = Field(ge=0, description="Minimum distance to stations")
    gap: float = Field(ge=0, le=360, description="Largest azimuthal gap between stations")
    nst: int = Field(ge=0, description="Number of stations that reported the event")

    @model_validator(mode='before')
    @classmethod
    def set_defaults_for_missing(cls, data: dict) -> dict:
        for field_name in numerical_features:
            if data.get(field_name) is None and field_name in feature_medians:
                data[field_name] = feature_medians[field_name]
        return data

    model_config = {
        "json_schema_extra": {
            "example": {
                "latitude": 35.5,
                "longitude": -120.5,
                "depth": 10.0,
                "magType": "mww",
                "cdi": 3.5,
                "mmi": 4.0,
                "tsunami": 0,
                "sig": 100,
                "dmin": 0.5,
                "gap": 180.0,
                "nst": 50
            }
        }
    }

@app.get("/")
async def root():
    return {
        "message": "Earthquake Magnitude Prediction API",
        "status": "active",
        "endpoints": {
            "/predict": "POST - Make earthquake magnitude predictions",
            "/features": "GET - Get information about required features"
        }
    }

@app.get("/features")
async def get_features():
    return {
        "numerical_features": {
            feature: {
                "median": feature_medians.get(feature, 0),
                "description": "Numerical feature"
            } for feature in numerical_features
        },
        "categorical_features": {
            "magType": {
                "allowed_values": ["mww", "Mi", "mb", "ms", "md", "ml"],
                "description": "Type of magnitude measurement"
            }
        }
    }

@app.post("/predict")
async def predict_magnitude(feature_input: EarthquakeFeatures):
    try:
        # Convert input to DataFrame
        input_dict = feature_input.model_dump()
        logger.info(f"Received input data: {input_dict}")
        
        # Create DataFrame with correct column order
        input_df = pd.DataFrame([input_dict])
        
        # Ensure all required features are present and reorder columns
        if not all(f in input_df.columns for f in features):
            missing = [f for f in features if f not in input_df.columns]
            logger.error(f"Missing columns: {missing}")
            raise ValueError(f"Missing required features: {missing}")
        
        # Reorder columns to match the features list
        input_data = input_df[features]
        logger.info(f"Input DataFrame shape: {input_data.shape}")
        logger.info(f"Input DataFrame columns: {input_data.columns.tolist()}")
        
        # Make prediction using the model's pipeline
        prediction = model.predict(input_data)[0]
        logger.info(f"Prediction: {prediction}")

        return {
            "predicted_magnitude": float(prediction),
            "input_features": input_dict
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "message": "Error occurred during prediction"
            }
        )
