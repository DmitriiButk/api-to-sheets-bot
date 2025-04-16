from pydantic import BaseModel


class PostValidate(BaseModel):
    user_id: int
    id: int
    title: str
    body: str


class CommentValidate(BaseModel):
    post_id: int
    id: int
    name: str
    email: str
    body: str


class PhotoValidate(BaseModel):
    album_id: int
    id: int
    title: str
    url: str
    thumbnail_url: str


class AlbumValidate(BaseModel):
    user_id: int
    id: int
    title: str


class TodoValidate(BaseModel):
    user_id: int
    id: int
    title: str
    completed: bool


class GeoValidate(BaseModel):
    lat: str
    lng: str


class AddressValidate(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoValidate


class CompanyValidate(BaseModel):
    name: str
    catch_phrase: str
    bs: str


class UserValidate(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: AddressValidate
    phone: str
    website: str
    company: CompanyValidate
