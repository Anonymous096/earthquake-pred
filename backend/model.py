import pickle

# Load the model
with open("model/earthquake_model.pkl", "rb") as f:
    model = pickle.load(f)

# Check type
print(type(model))  # Should be <class 'sklearn.pipeline.Pipeline'>

# Test Prediction
import pandas as pd
sample_input = pd.DataFrame([{
    "latitude": 35.5, "longitude": -120.5, "depth": 10.0, "cdi": 3.2, "mmi": 2.5,
    "tsunami": 0, "sig": 450, "dmin": 0.2, "gap": 45.0, "nst": 25
}])

prediction = model.predict(sample_input)
print("Predicted Magnitude:", prediction[0])
