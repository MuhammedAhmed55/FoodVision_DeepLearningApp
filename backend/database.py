from supabase import create_client

from config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)


def save_prediction(
    image_url: str,
    prediction: str,
    confidence: float,
    user_id: str | None = None,
):
    """
    Save prediction record to Supabase.
    """

    if not user_id:
        print("Skipping database save: no user_id provided")
        return None

    response = (
        supabase
        .table("predictions")
        .insert(
            {
                "user_id": user_id,
                "image_url": image_url,
                "prediction": prediction,
                "confidence": confidence,
            }
        )
        .execute()
    )

    return response