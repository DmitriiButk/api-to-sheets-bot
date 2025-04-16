from sqlalchemy import Integer, String,ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(String)


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(String)


class Photo(Base):
    __tablename__ = 'photos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    album_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    thumbnail_url: Mapped[str] = mapped_column(String)


class Album(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)


class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    completed: Mapped[bool] = mapped_column(Boolean)


class Geo(Base):
    __tablename__ = 'geo'

    address_user_id: Mapped[int] = mapped_column(ForeignKey('address.user_id'), primary_key=True)
    lat: Mapped[str] = mapped_column(String)
    lng: Mapped[str] = mapped_column(String)

    address: Mapped['Address'] = relationship(back_populates='geo', uselist=False)


class Address(Base):
    __tablename__ = 'address'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    street: Mapped[str] = mapped_column(String)
    suite: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    zipcode: Mapped[str] = mapped_column(String)

    geo: Mapped['Geo'] = relationship(
        back_populates='address', uselist=False, cascade='all, delete'
    )
    user: Mapped['User'] = relationship(back_populates='address', uselist=False)


class Company(Base):
    __tablename__ = 'company'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    catch_phrase: Mapped[str] = mapped_column(String)
    bs: Mapped[str] = mapped_column(String)

    user: Mapped['User'] = relationship(back_populates='company', uselist=False)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    website: Mapped[str] = mapped_column(String)

    address: Mapped['Address'] = relationship(
        back_populates='user', uselist=False, cascade='all, delete'
    )
    company: Mapped['Company'] = relationship(
        back_populates='user', uselist=False, cascade='all, delete'
    )
