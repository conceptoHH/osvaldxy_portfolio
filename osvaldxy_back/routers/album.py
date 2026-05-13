import shutil
import os
from sqlmodel import Session, select
from fastapi import Depends, status, APIRouter, UploadFile, HTTPException
from ..database import get_session
from ..models import *

router = APIRouter()

@router.get("/", response_model=list[AlbumReturn])
def get_all_album(*, session: Session = Depends(get_session)):
    album_db = session.exec(select(Album)).all()
    if not album_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media found')
    return album_db

#Need to test, idfk how this withmedia works
@router.get("/{slug}", response_model=AlbumWithMediaReturn)
def get_detail_album(*, session: Session =  Depends(get_session), slug: str):
    album_db = session.exec(select(Album).where(Album.slug == slug)).one_or_none()
    if not album_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No album with this slug: {slug} found')
    return album_db
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def post_album(*, session: Session = Depends(get_session), album: AlbumBase):
   
     #need to validate the model to upload for some reason
    album_db = Album.model_validate(album)
    session.add(album_db)
    session.commit()
    session.refresh(album_db)
    return album_db

@router.patch("/{id}", response_model=AlbumReturn)
def modify_album(*, session: Session =  Depends(get_session), id: int, album: AlbumUpdate):

    album_db = session.get(Album, id)
    
    if not album_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media with this id: {id} found')


    album_update_data = album.model_dump(exclude_unset=True)
    album_db.sqlmodel_update(album_update_data)
    session.add(album_db)
    session.commit()
    session.refresh(album_db)
    
    return album_db

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(*, session: Session = Depends(get_session), id: int):
    album_db = session.get(Album, id)
    
    if not album_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media with this id: {id} found')

    #commiting to db
    session.delete(album_db)
    session.commit()
    return None



