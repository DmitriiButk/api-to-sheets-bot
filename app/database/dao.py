from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, Address, Company, Geo, Post, Comment, Photo, Album, Todo


class BaseDAO:
    """
    Базовый класс для работы с базой данных.

    Атрибуты:
        session (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.
        model (Type): Модель базы данных, с которой работает DAO.

    Методы:
        create(entity): Создает новую запись в базе данных.
        delete_all(): Удаляет все записи из таблицы, связанной с моделью.
    """
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def create(self, entity):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        entities = result.scalars().all()
        for entity in entities:
            await self.session.delete(entity)
        await self.session.commit()


class UserDAO(BaseDAO):
    """
    DAO для работы с пользователями.

    Методы:
        create_user(user, address, company, geo): Создает пользователя с привязанными адресом, компанией и геолокацией.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def create_user(self, user: User, address: Address, company: Company, geo: Geo):
        self.session.add_all([geo, address, company, user])
        await self.session.commit()
        await self.session.refresh(user)
        return user


class PostDAO(BaseDAO):
    """
    DAO для работы с постами.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, Post)


class CommentDAO(BaseDAO):
    """
    DAO для работы с комментариями.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, Comment)


class PhotoDAO(BaseDAO):
    """
    DAO для работы с фотографиями.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, Photo)


class AlbumDAO(BaseDAO):
    """
    DAO для работы с альбомами.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, Album)


class TodoDAO(BaseDAO):
    """
    DAO для работы с задачами.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, Todo)
