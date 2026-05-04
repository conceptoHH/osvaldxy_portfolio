from sqlmodel import Session, select
from fastapi import Depends, status, APIRouter
from ..database import get_session
from ..models import *

router = APIRouter()

@router.get("/") #response_model=list[MediaReturn])
def get_all_media():
    return {"Hello":" from media controller"}

@router.get("/{slug}")
def get_detail_media():
    pass
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def post_image(*, session: Session = Depends(get_session), media: MediaCreate):
    db_media = Media.model_validate(media)

    session.add(db_media)
    session.commit()
    session.refresh(db_media)
    return db_media

@router.patch("/{id}")
def modify_image():
    pass

@router.delete("/{id}")
def delete_image():
    pass


