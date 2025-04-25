from fastapi import APIRouter, UploadFile, Depends, File

from constant import API_PREFIX
from auth import get_current_user

router = APIRouter(prefix=f"{API_PREFIX}")

@router.post("/field")
def send_field_data():
    pass


@router.post("/image")
def upload_image(file: UploadFile = File(...), user=Depends(get_current_user)):
    print(user)
    return "1"