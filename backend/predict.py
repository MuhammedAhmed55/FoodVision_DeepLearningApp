import torch
from PIL import Image

from model import load_model, DEVICE
from transforms import auto_transform
from classes import CLASS_NAMES

# Load the model only ONCE when FastAPI starts
model = load_model()


def predict_image(image_path: str):
    """
    Predicts the class of an image.

    Args:
        image_path (str): Path to image.

    Returns:
        dict: prediction and confidence.
    """

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Transform image
    image = auto_transform(image)

    # Add batch dimension
    image = image.unsqueeze(0)

    # Move image to GPU/CPU
    image = image.to(DEVICE)

    # Turn off gradient calculations
    with torch.inference_mode():

        outputs = model(image)

        probabilities = torch.softmax(outputs, dim=1)

        confidence, predicted_class = torch.max(
            probabilities,
            dim=1
        )

    return {
        "prediction": CLASS_NAMES[predicted_class.item()],
        "confidence": round(confidence.item() * 100, 2)
    }