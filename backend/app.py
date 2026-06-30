from fastapi import FastAPI, UploadFile, File , Form
from fastapi.middleware.cors import CORSMiddleware
from storage import upload_image
from database import save_prediction
import shutil
import os

from predict import predict_image

app = FastAPI(
    title="FoodVision API",
    description="Image Classification API using EfficientNet-B2",
    version="1.0.0"
)

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "FoodVision API is running 🚀"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...) , user_id: str = Form(...)):
    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print("Step 1: Image saved")

        # Run the model first so prediction is returned even if storage or database writes fail.
        result = predict_image(file_path)
        print("Step 2: Prediction complete")
        print(result)

        image_url = None

        try:
            image_url = upload_image(file_path)
            print("Step 3: Image uploaded")
        except Exception as storage_error:
            print("Storage upload failed:")
            print(storage_error)

        try:
            if image_url:
                save_prediction(
                    user_id=user_id,
                    image_url=image_url,
                    prediction=result["prediction"],
                    confidence=result["confidence"],
                )
                print("Step 4: Saved to database")
        except Exception as database_error:
            print("Database save failed:")
            print(database_error)

        return {
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "image_url": image_url,
        }

    except Exception as e:
        print("========================")
        print("ERROR:")
        print(e)
        print("========================")
        raise

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)