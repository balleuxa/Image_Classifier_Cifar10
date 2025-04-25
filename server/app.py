from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
model = load_model("model/my_model.keras")
class_names = ["airplane", "automobile", "bird", "cat", "deer",
               "dog", "frog", "horse", "ship", "truck"]

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((32, 32))

    img_array = np.array(image) / 255.0
    img_array = img_array.reshape(1, 32, 32, 3)

    predictions = model.predict(img_array)
    probabilities = tf.nn.softmax(predictions[0]).numpy()
    predicted_index = int(np.argmax(probabilities))
    confidence = round(float(np.max(probabilities)) * 100, 2)
    predicted_label = class_names[predicted_index]

    return JSONResponse({
        "prediction": predicted_label,
        "confidence": confidence
    })
