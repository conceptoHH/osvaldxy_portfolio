import shutil
import os
from sqlmodel import Session, select
from fastapi import Depends, status, APIRouter, UploadFile, HTTPException
from ..database import get_session
from ..models import *

router = APIRouter()

@router.get("/", response_model=list[MediaReturn])
def get_all_media(*, session: Session = Depends(get_session)):
    media = session.exec(select(Media)).all()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media found')
    return media

@router.get("/{slug}", response_model=MediaReturn)
def get_detail_media(*, session: Session =  Depends(get_session), slug: str):
    media = session.exec(select(Media).where(Media.slug == slug)).one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media with this slug: {slug} found')
    return media
    
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

@router.patch("/{id}", response_model=MediaReturn)
def modify_image(*, session: Session =  Depends(get_session), id: int, media: MediaUpdate):

    media_get_db = session.get(Media, id)
    
    if not media_get_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media with this id: {id} found')


    media_update_data = media.model_dump(exclude_unset=True)
    media_get_db.sqlmodel_update(media_update_data)
    session.add(media_get_db)
    session.commit()
    session.refresh(media_get_db)
    
    return media_get_db

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(*, session: Session = Depends(get_session), id: int):
    media_db = session.get(Media, id)
    
    if not media_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media with this id: {id} found')

    #Deleting from disk

    relative_path = media_db.path_url.replace("/static", "/uploads")
    abs_path = os.path.abspath("osvaldxy_back"+relative_path)
    
    try:
        os.remove(abs_path)
    except FileNotFoundError as e:
        raise e

    #commiting to db
    session.delete(media_db)
    session.commit()
    return None


