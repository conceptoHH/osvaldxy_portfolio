from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_admin: bool = Field(default=False)
    
class Media(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name_media: str
    type_media: str
    slug: str
    path_url: str


class Album(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name_album: str
    cover: str

class AlbumMedia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    media_id: int | None = Field(default=None, foreign_key="media.id")
    album_id: int | None = Field(default=None, foreign_key="album.id")
   
