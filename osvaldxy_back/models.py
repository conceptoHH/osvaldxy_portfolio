from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_admin: bool = Field(default=False)

#AlbumMedia model and DTOs
class AlbumMediaBase(SQLModel):
    media_id: int | None = Field(default=None, foreign_key="media.id")
    album_id: int | None = Field(default=None, foreign_key="album.id")
   
class AlbumMedia(AlbumMediaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class AlbumMediaReturn(AlbumMediaBase):
    id: int

class AlbumMediaUpdate(SQLModel):
    media_id: int | None = None
    album_id: int | None = None

    
#Media model and DTOs
class MediaBase(SQLModel):
    name_media: str
    type_media: str
    slug: str
    path_url: str 

class Media(MediaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    albums: list["Album"] = Relationship(back_populates="media_items", link_model=AlbumMedia)

class MediaCreate(MediaBase):
    pass

class MediaReturn(MediaBase):
    id: int

class MediaUpdate(SQLModel):
    name_media: str | None = None
    type_media: str | None = None

#Album model and DTOs
class AlbumBase(SQLModel):
    name_album: str
    slug: str
    cover_media_int: int | None = Field(default=None, foreign_key="media.id")

class Album(AlbumBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    media_items: list["Media"] = Relationship(back_populates="albums", link_model=AlbumMedia)

class AlbumReturn(AlbumBase):
    id: int

class AlbumUpdate(SQLModel):
    name_album: str | None = None
    cover: str | None = None

class AlbumWithMediaReturn(AlbumBase):
    id: int
    media_items: list[MediaReturn]


