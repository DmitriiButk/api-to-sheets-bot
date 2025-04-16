import aiohttp
from typing import List, Dict, Union
import re


def to_snake_case(name: str) -> str:
    """
    Преобразует строку из camelCase в snake_case.

    Параметры:
        name (str): Строка в формате camelCase.

    Возвращает:
        str: Строка в формате snake_case.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def convert_keys_to_snake_case(obj: Union[Dict, List]) -> Union[Dict, List]:
    """
    Рекурсивно преобразует ключи словаря или элементов списка из camelCase в snake_case.

    Параметры:
        obj (Union[Dict, List]): Словарь или список для преобразования.

    Возвращает:
        Union[Dict, List]: Объект с преобразованными ключами.
    """
    if isinstance(obj, dict):
        return {to_snake_case(k): convert_keys_to_snake_case(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_snake_case(elem) for elem in obj]
    else:
        return obj


async def fetch_data_from_api(url: str) -> List[Dict]:
    """
    Выполняет GET-запрос к API и возвращает данные с преобразованными ключами.

    Параметры:
        url (str): URL API для выполнения запроса.

    Возвращает:
        List[Dict]: Список словарей с данными, где ключи преобразованы в snake_case.

    Исключения:
        Exception: Если запрос завершился с ошибкой.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                snake_case_data = convert_keys_to_snake_case(data)
                return snake_case_data
            else:
                raise Exception(f'API request failed with status {response.status}')


async def fetch_data(api_url: str, validation_model):
    """
    Загружает данные из API и валидирует их с использованием модели.

    Параметры:
        api_url (str): URL API для загрузки данных.
        validation_model: Pydantic-модель для валидации данных.

    Возвращает:
        List: Список объектов, валидированных с помощью модели.
    """
    data = await fetch_data_from_api(api_url)
    return [validation_model(**item) for item in data]
