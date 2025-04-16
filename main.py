from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from app.handlers.handler import register_handlers
from app.services.config import load_config


async def on_startup(app):
    """
    Выполняется при запуске приложения.

    Параметры:
        app (Application): Экземпляр веб-приложения.

    Действия:
        - Загружает конфигурацию приложения.
        - Создает экземпляры бота и диспетчера.
        - Регистрирует обработчики событий.
        - Устанавливает вебхук для бота.
        - Сохраняет объекты бота, диспетчера и конфигурации в приложение.
    """
    config = load_config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    register_handlers(dp)
    app['bot'] = bot
    app['dp'] = dp
    app['config'] = config

    await bot.set_webhook(config.webhook_url + '/webhook')

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path='/webhook')


async def on_shutdown(app):
    """
    Выполняется при завершении работы приложения.

    Параметры:
        app (Application): Экземпляр веб-приложения.

    Действия:
        - Закрывает сессию бота.
    """
    await app['bot'].session.close()


def create_app():
    """
    Создает и настраивает экземпляр веб-приложения.

    Действия:
        - Регистрирует функции запуска и завершения приложения.
        - Возвращает настроенное приложение.

    Возвращает:
        Application: Настроенное веб-приложение.
    """
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == '__main__':
    web.run_app(create_app(), host='0.0.0.0', port=8000)
