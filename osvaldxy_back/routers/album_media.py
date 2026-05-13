import shutil
import os
from sqlmodel import Session, select
from fastapi import Depends, status, APIRouter, UploadFile, HTTPException
from ..database import get_session
from ..models import *

router = APIRouter()

@router.get("/", response_model=list[AlbumMediaReturn])
def get_all_album(*, session: Session = Depends(get_session)):
    album_media_db = session.exec(select(AlbumMedia)).all()
    if not album_media_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media found')
    return album_media_db

#Need to test, idfk how this withmedia works   
@router.post("/", status_code=status.HTTP_201_CREATED)
def post_album(*, session: Session = Depends(get_session), albumMedia: AlbumMediaBase):
   
     #need to validate the model to upload for some reason
    album_media_db = AlbumMedia.model_validate(albumMedia)
    session.add(album_media_db)
    session.commit()
    session.refresh(album_media_db)
    return album_media_db

@router.patch("/{id}", response_model=AlbumMediaReturn)
def modify_album(*, session: Session =  Depends(get_session), id: int, album: AlbumMediaUpdate):

    album_media_db = session.get(AlbumMedia, id)
    
    if not album_media_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media with this id: {id} found')


    album_update_data = album.model_dump(exclude_unset=True)
    album_media_db.sqlmodel_update(album_update_data)
    session.add(album_media_db)
    session.commit()
    session.refresh(album_media_db)
    
    return album_media_db

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(*, session: Session = Depends(get_session), id: int):
    album_media_db = session.get(AlbumMedia, id)
    
    if not album_media_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media with this id: {id} found')

    #commiting to db
    session.delete(album_media_db)
    session.commit()
    return None




