import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
MAP_TOKEN = str(os.getenv("MAP_TOKEN"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
DBHOST = str(os.getenv("DBHOST"))

ADMINS = str(os.getenv("ADMINS")).split(',')
CHANNELS = str(os.getenv("CHANNELS")).split(',')

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

MEDIA_URL = 'media'

POSTGRES_UGI = f"postgresql://{PGUSER}:{PGPASSWORD}@{DBHOST}/{DATABASE}"
PATH_MEDIA = f'django_project/telegrambot/{MEDIA_URL}/'

LANGUAGE_RU = 'ru'  # default
LANGUAGE_EN = 'en'
LANGUAGE_UZ = 'uz'

MAIN_LANGUAGE_INLINE_MODE = LANGUAGE_RU
MAX_ROW = 25
MORE_ORDER_CHECK_COUNT = True
LIST_KEYS_TO_THE_ADD_ORDER = ['running']
MAX_PER_ADDITIONAL_ORDER = 5
SEND_FILE_ITEMS = False
SEND_ALL_PRODUCTS_TEXT = True
CONVERT_FILE_TO_PNG = False
SEND_ALL_PRODUCTS = False
