from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_admin: bool = Field(default=False)
    
#Media model and DTOs

class MediaBase(SQLModel):
    name_media: str
    type_media: str
    slug: str
    path_url: str 

class Media(MediaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class MediaCreate(MediaBase):
    pass

class MediaReturn(MediaBase):
    id: int

class MediaUpdate(SQLModel):
    name_media: str | None = None
    type_media: str | None = None
    slug: str | None = None
    path_url: str | None = None

class Album(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name_album: str
    cover: str

class AlbumMedia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    media_id: int | None = Field(default=None, foreign_key="media.id")
    album_id: int | None = Field(default=None, foreign_key="album.id")
   
