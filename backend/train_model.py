import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
import joblib

# Load the dataset
file_path = "model/earthquake_1995-2023.csv"
df = pd.read_csv(file_path)

# Selecting features and target variable
target = "magnitude"
features = ["latitude", "longitude", "depth", "cdi", "mmi", "tsunami", "sig", "dmin", "gap", "nst", "magType"]

# Drop rows with missing target
df = df.dropna(subset=[target])

# Fill missing numerical values with median
for col in ["cdi", "mmi", "sig", "dmin", "gap", "nst"]:
    df[col] = df[col].fillna(df[col].median())

# Split features into numerical and categorical
categorical_features = ["magType"]
numerical_features = [f for f in features if f not in categorical_features]

# Create preprocessor with explicit feature names
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_features),
        ("cat", OneHotEncoder(sparse_output=False, handle_unknown="ignore"), categorical_features)
    ],
    verbose_feature_names_out=False  # Don't prefix feature names
)

# Split the dataset
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model
model = Pipeline([
    ("scaler", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model
model.fit(X_train, y_train)

# Print feature names after preprocessing
print("Model steps:", model.named_steps)

# Save the model
joblib.dump(model, "model/earthquake_model.pkl")
print("Model saved successfully")

# Test prediction
sample_input = pd.DataFrame([{
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
}])

# Ensure columns are in the correct order
sample_input = sample_input[features]

# Make a test prediction
prediction = model.predict(sample_input)
print(f"\nTest prediction for sample input: {prediction[0]:.2f}") 