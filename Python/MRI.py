import sys
import numpy as np
import requests
from tensorflow.keras.models import load_model
from PIL import Image

PORT = 5058

labels = [
    "Mild Demented",
    "Moderate Demented",
    "Non Demented",
    "Very Mild Demented"
]

def preprocess(path):
    img = Image.open(path).convert("RGB").resize((128,128))
    arr = np.array(img)/255.0
    return np.expand_dims(arr,0)

model = load_model("Python/model.h5")

image_path = sys.argv[1]

arr = preprocess(image_path)
pred = model.predict(arr)

idx = int(np.argmax(pred))
label = labels[idx]
score = round(float(np.max(pred))*100,2)

requests.post(
    f"http://localhost:{PORT}/Home/ReceiveFinalResult",
    json={"result": label, "score": score}
)
