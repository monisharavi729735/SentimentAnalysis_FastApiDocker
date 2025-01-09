import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

app = FastAPI()

# Ensure models are loaded only if they exist
model_path = "/model/sentiment_model.pkl"
vectorizer_path = "/model/vectorizer.pkl"

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    raise FileNotFoundError(f"Required files are missing: {model_path} or {vectorizer_path}")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

joblib.dump(model, 'model/sentiment_model.pkl')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with domain names- e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    with open("app/static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

class InputText(BaseModel):
    text: str

@app.post('/predict/')
def predict_sentiment(input_text: InputText):
    transformed_text = vectorizer.transform([input_text.text])
    prediction = model.predict(transformed_text)[0]
    return {"sentiment": prediction}