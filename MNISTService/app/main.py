from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
from app import predict
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the MNIST Service"}

@app.post("/")
async def run_prediction(file: UploadFile = File(...)):
    is_valid_ext = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if is_valid_ext:
        img = Image.open(BytesIO(await file.read()))
        return {
            "filename": file.filename,
            "prediction": predict.predict_number(img)
        }
