from fileinput import filename
import shutil
import os
from sqlmodel import Session, select
from fastapi import Depends, status, APIRouter, UploadFile, HTTPException
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
def post_image(*, session: Session = Depends(get_session), file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File missing")
    
    #Path to directory
    path = os.path.abspath("osvaldxy_back/uploads") 

    safe_filename = os.path.basename(file.filename)
    mime_type = file.content_type

    if not mime_type:
        raise HTTPException(status_code=400, detail="MIME type could not be determined")

    if mime_type.startswith("image/"):
        calculated_type_media = "photo"
    elif mime_type.startswith("video/"):
        calculated_type_media = "video"
    else:
        # Reject the upload! It's a PDF, an EXE, or something you don't want.
        raise HTTPException(status_code=400, detail="Invalid file type")

    subfolder = "photos" if calculated_type_media == "photo" else "videos"
    target_dir = os.path.join(path, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    full_path = os.path.normpath(os.path.join(target_dir, safe_filename))
    
    #Writing the media to disk    
    try:
        with open(full_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise e
    finally:
        file.file.close()
    

    base_name = os.path.splitext(safe_filename)[0]
    generated_slug = base_name.replace(" ", "-").lower()
    relative_path_url = f"/static/{subfolder}/{safe_filename}"
    #Creating the media object to commit to the db
    media = Media(
        name_media=base_name,
        type_media=calculated_type_media,
        slug=generated_slug,
        path_url=relative_path_url
    )

     #need to validate the model to upload for some reason
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


