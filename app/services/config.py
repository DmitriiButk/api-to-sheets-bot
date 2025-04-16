import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Config:
    bot_token: str
    database_url: str
    webhook_url: str
    spreadsheet_id: str
    credentials_file: str
    url: str


def load_config() -> Config:
    db_user = os.getenv('DATABASE_USER')
    db_password = os.getenv('DATABASE_PASSWORD')
    db_name = os.getenv('DATABASE_NAME')
    db_host = os.getenv('DATABASE_HOST')
    return Config(
        bot_token=os.getenv('TG_TOKEN'),
        database_url=f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432/{db_name}',
        webhook_url=os.getenv('WEBHOOK_URL'),
        spreadsheet_id=os.getenv('SPREADSHEET_ID'),
        credentials_file=os.getenv('CREDENTIALS_FILE'),
        url='https://jsonplaceholder.typicode.com/'
    )
