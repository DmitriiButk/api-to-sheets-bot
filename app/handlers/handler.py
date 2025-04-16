from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from app.services.config import load_config
from app.database.db import AsyncSessionLocal
from app.database.models import Post, Comment, Photo, Album, Todo, User, Address, Company, Geo
from app.database.dao import PostDAO, CommentDAO, PhotoDAO, AlbumDAO, TodoDAO, UserDAO
from app.services.schemas import PostValidate, CommentValidate, PhotoValidate, AlbumValidate, TodoValidate, UserValidate
from app.services.utils import fetch_data
from app.services.google_sheets_service import write_to_google_sheets


url = load_config().url


async def start_command(message: Message):
    """
    Обрабатывает команду /start.

    Параметры:
        message (Message): Сообщение, содержащее команду.

    Действия:
        - Отправляет пользователю приветственное сообщение с клавиатурой для выбора данных.
    """
    try:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Посты', callback_data='fetch_posts')],
            [InlineKeyboardButton(text='Комментарии', callback_data='fetch_comments')],
            [InlineKeyboardButton(text='Альбомы', callback_data='fetch_albums')],
            [InlineKeyboardButton(text='Фотографии', callback_data='fetch_photos')],
            [InlineKeyboardButton(text='Задачи', callback_data='fetch_todos')],
            [InlineKeyboardButton(text='Пользователи', callback_data='fetch_users')]
        ])
        await message.answer(
            'Привет. Я бот, который выгружает данные из jsonplaceholder и загружает их в базу данных '
            'и в гугл таблицы. Выберите какие данные вы хотите загрузить:',
            reply_markup=keyboard)
    except Exception:
        await message.answer('Произошла ошибка при обработке команды. Пожалуйста, попробуйте позже.')


async def fetch_posts_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Посты".

    Параметры:
        callback_query (types.CallbackQuery): Объект обратного вызова.

    Действия:
        - Загружает данные о постах из API.
        - Валидирует данные.
        - Сохраняет данные в базу данных.
        - Записывает данные в Google Sheets.
    """
    try:
        await callback_query.message.answer('Данные о постах записываются, подождите...')

        api_url = f'{url}posts'
        validated_data = await fetch_data(api_url, PostValidate)

        async with AsyncSessionLocal() as session:
            post_repository = PostDAO(session)
            await post_repository.delete_all()

            for item in validated_data:
                post = Post(user_id=item.user_id, id=item.id, title=item.title, body=item.body)
                await post_repository.create(post)

        sheets_data = [[item.user_id, item.id, item.title, item.body] for item in validated_data]
        headers = ['user_id', 'id', 'title', 'body']
        sheets_data.insert(0, headers)
        await write_to_google_sheets(sheets_data, 'Posts')

        count = len(validated_data)
        await callback_query.message.answer(
            f'Данные о постах успешно записаны в базу данных и в гугл таблицы! Количество записей: {count}'
        )
    except Exception:
        await callback_query.message.answer('Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.')


async def fetch_comments_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Комментарии".

    Параметры:
        callback_query (types.CallbackQuery): Объект обратного вызова.

    Действия:
        - Загружает данные о комментариях из API.
        - Валидирует данные.
        - Сохраняет данные в базу данных.
        - Записывает данные в Google Sheets.
    """
    try:
        await callback_query.message.answer('Данные о комментариях записываются, подождите...')

        api_url = f'{url}comments'
        validated_data = await fetch_data(api_url, CommentValidate)

        async with AsyncSessionLocal() as session:
            comment_repository = CommentDAO(session)
            await comment_repository.delete_all()

            for item in validated_data:
                comment = Comment(post_id=item.post_id, id=item.id, name=item.name, email=item.email, body=item.body)
                await comment_repository.create(comment)

        sheets_data = [[item.post_id, item.id, item.name, item.email, item.body] for item in validated_data]
        headers = ['post_id', 'id', 'name', 'email', 'body']
        sheets_data.insert(0, headers)
        await write_to_google_sheets(sheets_data, 'Comments')

        count = len(validated_data)
        await callback_query.message.answer(
            f'Данные о комментариях успешно записаны в базу данных и гугл таблицы! Количество записей: {count}')

    except Exception:
        await callback_query.message.answer('Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.')


async def fetch_photos_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Фотографии".

    Параметры:
        callback_query (types.CallbackQuery): Объект обратного вызова.

    Действия:
        - Загружает данные о фотографиях из API.
        - Валидирует данные.
        - Сохраняет данные в базу данных.
        - Записывает данные в Google Sheets.
    """
    try:
        await callback_query.message.answer('Данные о фотографиях записываются, подождите...')

        api_url = f'{url}photos'
        validated_data = await fetch_data(api_url, PhotoValidate)

        async with AsyncSessionLocal() as session:
            photo_repository = PhotoDAO(session)
            await photo_repository.delete_all()

            for item in validated_data:
                photo = Photo(album_id=item.album_id, id=item.id, title=item.title, url=item.url,
                              thumbnail_url=item.thumbnail_url)
                await photo_repository.create(photo)

        sheets_data = [[item.album_id, item.id, item.title, item.url, item.thumbnail_url] for item in validated_data]
        headers = ['album_id', 'id', 'title', 'url', 'thumbnail_url']
        sheets_data.insert(0, headers)
        await write_to_google_sheets(sheets_data, 'Photos')

        count = len(validated_data)
        await callback_query.message.answer(
            f'Данные о фотографиях успешно записаны в базу данных и в гугл таблицы! Количество записей: {count}'
        )

    except Exception:
        await callback_query.message.answer('Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.')


async def fetch_albums_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Альбомы".

    Параметры:
        callback_query (types.CallbackQuery): Объект обратного вызова.

    Действия:
        - Загружает данные об альбомах из API.
        - Валидирует данные.
        - Сохраняет данные в базу данных.
        - Записывает данные в Google Sheets.
    """
    try:
        await callback_query.message.answer('Данные об альбомах записываются, подождите...')

        api_url = f'{url}albums'
        validated_data = await fetch_data(api_url, AlbumValidate)

        async with AsyncSessionLocal() as session:
            album_repository = AlbumDAO(session)
            await album_repository.delete_all()

            for item in validated_data:
                album = Album(user_id=item.user_id, id=item.id, title=item.title)
                await album_repository.create(album)

        sheets_data = [[item.user_id, item.id, item.title] for item in validated_data]
        headers = ['user_id', 'id', 'title']
        sheets_data.insert(0, headers)
        await write_to_google_sheets(sheets_data, 'Albums')

        count = len(validated_data)
        await callback_query.message.answer(
            f'Данные об альбомах успешно записаны в базу данных и в гугл таблицы! Количество записей: {count}'
        )
    except Exception:
        await callback_query.message.answer('Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.')


async def fetch_todos_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Задачи".

    Параметры:
        callback_query (types.CallbackQuery): Объект обратного вызова.

    Действия:
        - Загружает данные о задачах из API.
        - Валидирует данные.
        - Сохраняет данные в базу данных.
        - Записывает данные в Google Sheets.
    """
    try:
        await callback_query.message.answer('Данные о задачах записываются, подождите...')

        api_url = f'{url}todos'
        validated_data = await fetch_data(api_url, TodoValidate)

        async with AsyncSessionLocal() as session:
            todo_repository = TodoDAO(session)
            await todo_repository.delete_all()

            for item in validated_data:
                todo = Todo(user_id=item.user_id, id=item.id, title=item.title, completed=item.completed)
                await todo_repository.create(todo)

        sheets_data = [[item.user_id, item.id, item.title, item.completed] for item in validated_data]
        headers = ['user_id', 'id', 'title', 'completed']
        sheets_data.insert(0, headers)
        await write_to_google_sheets(sheets_data, 'Todos')

        count = len(validated_data)
        await callback_query.message.answer(
            f'Данные о задачах успешно записаны в базу данных и в гугл таблицы! Количество записей: {count}'
        )
    except Exception:
        await callback_query.message.answer('Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.')


async def fetch_users_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Пользователи".

    Параметры:
        callback_query (types.CallbackQuery): Объект обратного вызова.

    Действия:
        - Загружает данные о пользователях из API.
        - Валидирует данные.
        - Сохраняет данные в базу данных.
        - Записывает данные в Google Sheets.
    """
    try:
        await callback_query.message.answer('Данные о пользователях записываются, подождите...')

        api_url = f'{url}users'
        validated_data = await fetch_data(api_url, UserValidate)

        async with AsyncSessionLocal() as session:
            user_repository = UserDAO(session)
            await user_repository.delete_all()

            for item in validated_data:
                geo = Geo(
                    address_user_id=item.id,
                    lat=item.address.geo.lat,
                    lng=item.address.geo.lng
                )

                address = Address(
                    user_id=item.id,
                    street=item.address.street,
                    suite=item.address.suite,
                    city=item.address.city,
                    zipcode=item.address.zipcode,
                )

                company = Company(
                    user_id=item.id,
                    name=item.company.name,
                    catch_phrase=item.company.catch_phrase,
                    bs=item.company.bs
                )

                user = User(
                    id=item.id,
                    name=item.name,
                    username=item.username,
                    email=item.email,
                    phone=item.phone,
                    website=item.website,
                )

                await user_repository.create_user(user, address, company, geo)

        sheets_data = [[
            item.id, item.name, item.username, item.email,
            item.address.street, item.address.suite, item.address.city, item.address.zipcode,
            item.address.geo.lat, item.address.geo.lng,
            item.phone, item.website,
            item.company.name, item.company.catch_phrase, item.company.bs
        ] for item in validated_data]

        headers = [
            'id', 'name', 'username', 'email',
            'address_street', 'address_suite', 'address_city', 'address_zipcode',
            'geo_lat', 'geo_lng',
            'phone', 'website',
            'company_name', 'company_catch_phrase', 'company_bs'
        ]
        sheets_data.insert(0, headers)
        await write_to_google_sheets(sheets_data, 'Users')

        count = len(validated_data)
        await callback_query.message.answer(
            f'Данные о пользователях успешно записаны в базу данных и в гугл таблицы! Количество записей: {count}'
        )
    except Exception as e:
        await callback_query.message.answer('Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.')


def register_handlers(dp: Dispatcher):
    """
    Регистрирует обработчики команд и обратных вызовов.

    Параметры:
        dp (Dispatcher): Диспетчер для регистрации обработчиков.

    Действия:
        - Регистрирует обработчик команды /start.
        - Регистрирует обработчики для кнопок обратного вызова.
    """
    dp.message.register(start_command, Command(commands=['start']))
    dp.callback_query.register(fetch_posts_callback, lambda c: c.data == 'fetch_posts')
    dp.callback_query.register(fetch_comments_callback, lambda c: c.data == 'fetch_comments')
    dp.callback_query.register(fetch_albums_callback, lambda c: c.data == 'fetch_albums')
    dp.callback_query.register(fetch_photos_callback, lambda c: c.data == 'fetch_photos')
    dp.callback_query.register(fetch_todos_callback, lambda c: c.data == 'fetch_todos')
    dp.callback_query.register(fetch_users_callback, lambda c: c.data == 'fetch_users')
