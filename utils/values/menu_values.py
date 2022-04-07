from data.config import LANGUAGE_EN, LANGUAGE_UZ, LANGUAGE_RU
from utils.db_api import db_commands
from utils.values import others

BACK_BUTTON = {
    LANGUAGE_RU: '◀ Назад',
    LANGUAGE_UZ: '◀ Ортга',
    LANGUAGE_EN: '◀ Back'
}

HOME_BUTTON = {
    LANGUAGE_RU: '🏠 Главное меню',
    LANGUAGE_UZ: '🏠 Асосий меню',
    LANGUAGE_EN: '🏠 Main menu'
}

PRODUCTS = {
    LANGUAGE_RU: '📦 Товары',
    LANGUAGE_EN: '📦 Products',
    LANGUAGE_UZ: '📦 Махсулотлар'
}

PRICE_LIST = {
    LANGUAGE_RU: '📋 Дефицитный лист',
    LANGUAGE_EN: '📋 Deficit list',
    LANGUAGE_UZ: '📋 Дефитсит варақаси'
}

PRODUCTS_WITHOUT_PICTURE = {
    LANGUAGE_RU: '📦 Товары (без картинок)',
    LANGUAGE_EN: '📦 Products (no pictures)',
    LANGUAGE_UZ: '📦 Махсулотлар (расмлар йук)'
}

REVIEW = {
    LANGUAGE_RU: '✍ Оставить отзыв',
    LANGUAGE_EN: '✍ Leave a feedback',
    LANGUAGE_UZ: '✍ Фикр билдириш'
}

READY = {
    LANGUAGE_RU: '✅ Готово',
    LANGUAGE_EN: '✅ Ready',
    LANGUAGE_UZ: '✅ Таййор'
}

BASKET = {
    LANGUAGE_RU: '🛒 Корзина',
    LANGUAGE_EN: '🛒 Basket',
    LANGUAGE_UZ: '🛒 Сават'
}

SEARCH = {
    LANGUAGE_RU: '🔍 Поиск',
    LANGUAGE_EN: '🔍 Search',
    LANGUAGE_UZ: '🔍 Қидикмоқ'
}

ABOUT_US = {
    LANGUAGE_RU: '☎ О нас',
    LANGUAGE_EN: '☎ About us',
    LANGUAGE_UZ: '☎ Биз хақимизда'
}

ACT_OF_RECONCILIATION = {
    LANGUAGE_RU: '💰 Акт сверки',
    LANGUAGE_EN: '💰 Act of reconciliation',
    LANGUAGE_UZ: '💰 Akt sverki'
}

CHANGE_LANGUAGE = {
    LANGUAGE_RU: '🇷🇺🔄🇬🇧 Сменить язык',
    LANGUAGE_EN: '🇬🇧🔄🇺🇿 Language',
    LANGUAGE_UZ: '🇺🇿🔄🇷🇺 Тилни ўзгартириш'
}

MY_ORDERS = {
    LANGUAGE_RU: '📖 Мои заказы',
    LANGUAGE_EN: '📖 My orders',
    LANGUAGE_UZ: '📖 Менинг буюртмаларим'
}

PLUS_emoji = '➕'
MINUS_emoji = '➖'
CANCEL_emoji = '❌'

ADD_BASKET = {
    LANGUAGE_RU: '🛒 Добавить в корзину',
    LANGUAGE_EN: '🛒 Add to shopping cart',
    LANGUAGE_UZ: '🛒 Саватга қўшиш'
}

OTHERS = {
    LANGUAGE_RU: '🔽 Другие',
    LANGUAGE_EN: '🔽 Others',
    LANGUAGE_UZ: '🔽 Бошқалар'
}

CANCEL = {
    LANGUAGE_RU: '❌ Отмена',
    LANGUAGE_EN: '❌ Cancel',
    LANGUAGE_UZ: '❌ Бекор қилиш'
}

RESET_BASKET = {
    LANGUAGE_RU: '❌ Очистить корзину',
    LANGUAGE_EN: '❌ Empty trash',
    LANGUAGE_UZ: '❌ Ахлат қутиси'
}

RESET_ADDITIONAL_ORDER = {
    LANGUAGE_RU: '🗑 Очистить доп. заказ',
    LANGUAGE_EN: '🗑 Clear additional order',
    LANGUAGE_UZ: '🗑 Аниқ қўшимча буюртма'
}

EDIT_QUANTITY = {
    LANGUAGE_RU: '🛒 Изменить количество',
    LANGUAGE_EN: '🛒 Change quantity',
    LANGUAGE_UZ: '🛒 Миқдорни ўзгартириш'
}

TO_ORDER = {
    LANGUAGE_RU: '🚗 Заказать',
    LANGUAGE_EN: '🚗 To order',
    LANGUAGE_UZ: '🚗 Буюртма қилиш'
}

MY_CONTACT = {
    LANGUAGE_RU: '📱 Мой номер телефона',
    LANGUAGE_UZ: '📱 Менинг телефон рақамим',
    LANGUAGE_EN: '📱 My phone number'
}

NEXT_BUTTON = {
    LANGUAGE_RU: 'Следующий ⏩',
    LANGUAGE_EN: 'Next ⏩',
    LANGUAGE_UZ: 'Кейинги ⏩'
}


SKIP_BUTTON = {
    LANGUAGE_RU: 'Пропустить ⏩',
    LANGUAGE_EN: 'Skip ⏩',
    LANGUAGE_UZ: 'Ўтказиб юбориш ⏩'
}


LOCATION_BUTTON = {
    LANGUAGE_RU: '📍 Поделиться локацией',
    LANGUAGE_EN: '📍 Share location',
    LANGUAGE_UZ: '📍 Жойлашувни бахам кўринг'
}

TO_CONFIRM = {
    LANGUAGE_RU: '✅ Подтвердить',
    LANGUAGE_EN: '✅ Confirm',
    LANGUAGE_UZ: '✅ Тасдиқланг'
}

UPDATE = {
    LANGUAGE_RU: '🔄 Обновить',
    LANGUAGE_EN: '🔄 Update',
    LANGUAGE_UZ: '🔄 Янгилаш'
}


async def get_categories(language: str):
    categories_db, key_str = await db_commands.get_categories_from_items(language=language)

    categories = [val[key_str] for val in categories_db]
    return categories


async def get_mainReviews(language: str, **kwargs):
    mainReviews_db, key_str = await db_commands.get_reviews_main(language=language, **kwargs)

    reviews = [getattr(val, key_str) for val in mainReviews_db]
    return reviews


async def get_subcategories_or_items_by_category(language: str, category: str, subcategory: str = None):
    items_by_category = await db_commands.get_subcategories_or_items_by_category(
        language=language,
        category=category,
        subcategory=subcategory)
    attr = others.get_attribute_by_language(language=language)
    subcategories_or_items = []
    items_category = []
    subcategories = []
    items_full = []
    for item in items_by_category:
        if not item.subcategory:
            items_category.append(getattr(item, attr))
        else:
            subcategories.append(getattr(item.subcategory, attr))
        items_full.append(getattr(item, attr))
    subcategories = set(subcategories)
    items_category = set(items_category)
    subcategories_or_items.extend(subcategories)
    subcategories_or_items.extend(items_category)
    subcategories_or_items = set(sorted(subcategories_or_items))
    return {others.SUBCATEGORIES_OR_ITEMS: subcategories_or_items,
            others.ITEMS_CATEGORY: items_category,
            others.SUBCATEGORIES: subcategories,
            others.ITEMS_FULL: items_full}
