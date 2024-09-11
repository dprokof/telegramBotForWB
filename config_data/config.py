import os
from dotenv import load_dotenv,find_dotenv

if not find_dotenv():
    exit('Environment variables are not loaded because the ".env" file is missing')
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
DEFAULT_COMMANDS = (
    ('start', 'Запуск бота'),
    ('help', 'Помощь'),
    ('ref', 'Получение реферальной ссылки'),
    ('sub', 'Управление подписками')
)

host = os.getenv('host')
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv('database')

POSTGRES_URI = f'postgresql://{user}:{password}@{host}/{database}'