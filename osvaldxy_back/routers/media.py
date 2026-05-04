from sqlmodel import Session, select
from fastapi import Depends, status, APIRouter
from database import get_session
from models import MediaReturn, MediaCreate

router = APIRouter()

@router.get("/") #response_model=list[MediaReturn])
def get_all_media():
    return {"Hello":" from media controller"}

@router.get("/{slug}")
def get_detail_media():
    pass
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def post_image(*, session: Session = Depends(get_session), media: MediaCreate):
    session.add(media)
    session.commit()
    session.refresh(media)
    return media

@router.patch("/{id}")
def modify_image():
    pass

@router.delete("/{id}")
def delete_image():
    pass


