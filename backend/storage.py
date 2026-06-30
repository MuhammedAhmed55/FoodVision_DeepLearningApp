import os
import uuid

from database import supabase
from config import SUPABASE_BUCKET


def upload_image(file_path: str):

    file_extension = os.path.splitext(file_path)[1]

    filename = f"{uuid.uuid4()}{file_extension}"

    with open(file_path, "rb") as file:

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            filename,
            file
        )

    public_url = (
        supabase.storage
        .from_(SUPABASE_BUCKET)
        .get_public_url(filename)
    )

    return public_url