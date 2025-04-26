import uuid

from fastapi import APIRouter, UploadFile, Depends, File

from constant import API_PREFIX
from auth import get_current_user
from utils import store_image_to_cdn
from settings import client

router = APIRouter(prefix=f"{API_PREFIX}")

@router.post("/field")
def send_field_data(data):
    print(data)


@router.post("/image")
def upload_image(file: UploadFile = File(...), user=Depends(get_current_user)):
    url = store_image_to_cdn(file)
    image_info = {"url": url}
    image_res = client.table("image").insert(image_info).execute()
    
    field_res = client.table("field_history").select("*").eq("user_id", uuid.UUID(user)).execute()
    is_field_empty = True
    if len(field_res.data) != 0:
        is_field_empty = False
    
    forecast_info = {"user_id": user, "image_id": image_res.data[0]["id"]}
    forecast_res = client.table("forecast").insert(forecast_info).execute()
    return {"forecast_id": forecast_res.data[0]["id"], "is_field_empty": is_field_empty}