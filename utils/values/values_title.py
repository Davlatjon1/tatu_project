from typing import Union
from datetime import date
from aiogram.utils import markdown

from data.config import LANGUAGE_UZ, LANGUAGE_EN, LANGUAGE_RU
from utils.values.values_django import ORDER_STATUSES, TYPES_OF_PAYMENT
from django_project.telegrambot.constants.models import Constants
from django_project.telegrambot.usersmanage.models import Item, OrderItem
from loader import dp
from utils.db_api import db_commands
from utils.values import others

CHOOSE_CATEGORY_OR_ITEMS = {
    LANGUAGE_RU: 'Выберите категорию или продукт',
    LANGUAGE_EN: 'Select a category or product',
    LANGUAGE_UZ: 'Тоифани еки махсулотни танланг'
}

CHOOSE_CATEGORY = {
    LANGUAGE_RU: 'Выберите категорию',
    LANGUAGE_EN: 'Select a category',
    LANGUAGE_UZ: 'Бир тоифани танланг'
}

NOT_FOUND_CLIENT = {
    LANGUAGE_RU: '🙅 Не найден клиент',
    LANGUAGE_EN: '🙅 Client not found',
    LANGUAGE_UZ: '🙅 Мижоз топилмади'
}

CHOOSE_BELOW = {
    LANGUAGE_RU: 'Выберите кнопку ⬇',
    LANGUAGE_UZ: 'Қуйидагилардан бирини танланг ⬇',
    LANGUAGE_EN: 'Select button ⬇'
}

CHOOSE_CLIENT = {
    LANGUAGE_RU: 'Выберите один из клиентов ⬇',
    LANGUAGE_UZ: 'Мижозлардан бирини танланг ⬇',
    LANGUAGE_EN: 'Choose one of these clients ⬇'
}

CHOOSE_CATEGORY_OF_REVIEW = {
    LANGUAGE_RU: 'Выберите категорию отзыва 📋',
    LANGUAGE_UZ: 'Кўриб чиқиш тоифасини танланг 📋',
    LANGUAGE_EN: 'Select a review category 📋'
}

CHOOSE_PRODUCT = {
    LANGUAGE_RU: 'Выберите товар',
    LANGUAGE_UZ: 'Махсулотни танланг',
    LANGUAGE_EN: 'Select a product'
}

EMPTY = {
    LANGUAGE_RU: 'Пусто 🤔',
    LANGUAGE_UZ: 'Бўш 🤔',
    LANGUAGE_EN: 'Empty 🤔'
}

REMAINDER = {
    LANGUAGE_RU: 'Остаток',
    LANGUAGE_UZ: 'Қолган қисми',
    LANGUAGE_EN: 'Remainder'
}

PRICE = {
    LANGUAGE_RU: 'Цена',
    LANGUAGE_UZ: 'Нарх',
    LANGUAGE_EN: 'Price'
}

SUM = {
    LANGUAGE_RU: 'Сум',
    LANGUAGE_EN: 'Sum',
    LANGUAGE_UZ: 'Сўм'
}


def get_currency(language: str):
    constanta = Constants.default_constant()
    currency = SUM[language]
    if constanta and constanta.currency is not None:
        attr = others.get_attribute_by_language(language=language)
        currency = getattr(constanta.currency, attr)
    return currency


DAY = {
    LANGUAGE_RU: 'День',
    LANGUAGE_UZ: 'Кун',
    LANGUAGE_EN: 'Day'
}

WEEK = {
    LANGUAGE_RU: 'Неделя',
    LANGUAGE_UZ: 'Хафта',
    LANGUAGE_EN: 'Week'
}

MONTH = {
    LANGUAGE_RU: 'Месяц',
    LANGUAGE_UZ: 'Ой',
    LANGUAGE_EN: 'Month'
}

CONTACT_TO_REVIEW = {
    LANGUAGE_RU: '📝 Обратиться можно через отзывы',
    LANGUAGE_EN: '📝 You can contact through reviews',
    LANGUAGE_UZ: '📝 Шархлар орқали мурожаат қилишингиз мумкин',
}

ENTER_QUANTITY = {
    LANGUAGE_RU: 'Выберите или отправьте сообщение с количеством',
    LANGUAGE_EN: 'Select or send message with quantity',
    LANGUAGE_UZ: 'Хабарни танланг еки юборинг'
}


def opportunity_delete_order(language: str, timeout_cancel_order):
    if language == LANGUAGE_EN:
        return f'You have {timeout_cancel_order} seconds to cancel your order',
    elif language == LANGUAGE_UZ:
        return f'Буюртмани бекор қилиш учун {timeout_cancel_order} сония бор'
    else:
        return f'У вас есть {timeout_cancel_order} секунд, чтобы отменить заказ'


NOT_ACCESS = {
    LANGUAGE_RU: 'Доступ к боту запрещен 🚫',
    LANGUAGE_EN: 'Access to the bot is denied 🚫',
    LANGUAGE_UZ: 'Ботга кириш тақиқланган 🚫'
}

NOT_ACCESS_TO_ACT_SVERKI = {
    LANGUAGE_RU: 'Доступ к <b>акт сверки</b> запрещен 🚫',
    LANGUAGE_EN: 'Access to <b>act sverki</b> is denied 🚫',
    LANGUAGE_UZ: '<b>Акт сверки</b>га кириш тақиқланган 🚫'
}

NOT_ALLOW_TO_ADD_ORDER = {
    LANGUAGE_RU: '<b>Не доступно для доп. заказа</b> 🚫',
    LANGUAGE_EN: '<b>Not available for add. order</b> 🚫',
    LANGUAGE_UZ: '<b>Қўшиш учун мавжуд эмас. буюртма</b> 🚫'
}


def not_allow_to_add_order(item_name, language):
    return f"{NOT_ALLOW_TO_ADD_ORDER[language]}\n{item_name}"


FILL_IN_THE_ADD_ORDER = {
    LANGUAGE_RU: '❗️ Заполните доп. заказ',
    LANGUAGE_EN: '❗️ Fill in the add. order',
    LANGUAGE_UZ: '❗️ Кўшимчани тўлдиринг буюртма'
}

WRITE_MORE_INLINE = {
    LANGUAGE_RU: 'Введите не менее 3 символа 📝',
    LANGUAGE_EN: 'Please enter at least 3 characters 📝',
    LANGUAGE_UZ: 'Илтимос, камида 3та белгини киритинг 📝'
}

GO_SEARCH = {
    LANGUAGE_RU: 'Найти товар 👇',
    LANGUAGE_EN: 'Find a product 👇',
    LANGUAGE_UZ: 'Махсулотни топинг 👇'
}

REVIEW_MESSAGE = {
    LANGUAGE_RU: '📨 <b>Отправьте сообщение, фото или голосовое сообщение с вашим отзывом</b>',
    LANGUAGE_EN: '📨 <b>Send a message, photo or voice message with your review</b>',
    LANGUAGE_UZ: '📨 <b>Шархингиз билан хабар, расм ёки овозли хабар юборинг</b>'
}

ADD_MORE_ORDER = {
    LANGUAGE_RU: '📝 Добавьте еще товары, если у вас останется место в машине',
    LANGUAGE_EN: '📝 Add more items if you have more space in your car',
    LANGUAGE_UZ: '📝 Автомобилингизда кўпроқ жой бўлса, кўпроқ нарсаларни кўшинг'
}

GOT_REVIEW = {
    LANGUAGE_RU: '😊 <b>Получено, благодарю за отзыв</b>',
    LANGUAGE_EN: '😊 <b>Received, thank you for your feedback</b>',
    LANGUAGE_UZ: '😊 <b>Қабул қилинди, фикр-мулохазангиз учун ташаккур</b>'
}

RULES_ADDING_TO_ADD_ORDER = {
    LANGUAGE_RU: '👇 <b>Правила добавления в доп. заказ:</b>\n'
                 '1) Не дефицитный товар.\n'
                 '2) Общее количество доп. заказов не больше 5% от общего количества заказов.\n',
    LANGUAGE_UZ: '👇 <b>Қўшимча буюртма қўшиш қоидалари:</b>\n'
                 '1) Дефицит махсулот емас\n'
                 '2) Қўшилганларнинг умумий сони. Буюртмалар умумий сонининг 5% дан кўп бўлмаган буюртмалар\n',
    LANGUAGE_EN: '👇 <b>Rules for adding to an additional order:</b>\n'
                 '1) Not a hot product\n'
                 '2) The total number of add. orders no more than 5% of the total number of orders\n'
}

RULE_LIMIT_ADD_ORDER = {
    LANGUAGE_RU: 'Общее количество доп. заказов должно быть не больше 5% от общего количества заказов.',
    LANGUAGE_UZ: 'Қўшимчаларнинг умумий сони. Буюртмалар умумий буюртмалар сонининг 5% дан кўп бўлмаслиги керак',
    LANGUAGE_EN: 'The total number of add. orders should be no more than 5% of the total number of orders'
}

FORBIDDEN = {
    LANGUAGE_RU: '❌ Запрещено',
    LANGUAGE_UZ: '❌ Тақиқланган',
    LANGUAGE_EN: '❌ Forbidden'
}


def get_rate_limit(language: str, limit: Union[str, int]):
    RATE_LIMIT = {
        LANGUAGE_RU: f'Выдан мут на {limit} секунд 🕑',
        LANGUAGE_EN: f'Issued a mut for {limit} seconds 🕑',
        LANGUAGE_UZ: f'{limit} сония давомида мут чиқарилди 🕑'
    }
    return RATE_LIMIT[language]


def get_remainder(language: str, num="0", tag=True):
    if not num:
        num = NOT_SET[language].lower()
    return f"{REMAINDER[language].lower()[:3]}: {'<code>' if tag else ''}{('100+' if not isinstance(num, str) and num > 100 else num)}{'</code>' if tag else ''}"


def get_amount(language: str, num="0", tag=True):
    return f"{PRICE[language].capitalize()}: {'<code>' if tag else ''}{num}{'</code>' if tag else ''} {get_currency(language=language).lower()}"


def get_total(language: str, total: Union[str, int] = "0"):
    return f"{TOTAL[language]}: <code>{total}</code> {get_currency(language=language).lower()}"


def get_quantity(language: str, quantity: Union[str, int] = "0"):
    return f"{QUANTITY[language]}: <code>{quantity}</code> {UNIT_WT_low[language]}"


def get_sample_quantity(language: str, num: Union[str, int] = "0"):
    result = f'➖ Выб. количество: <code>{num}</code> шт. ➖'
    if language == LANGUAGE_EN:
        result = f'➖ Sample quantity: <code>{num}</code> pc. ➖'
    elif language == LANGUAGE_UZ:
        result = f'➖ Намуна миқдори: <code>{num}</code> дона ➖'

    return result


def get_caption_cat_or_product(language: str, items, subcategory):
    result = CHOOSE_BELOW[language]
    if len(items) > 0 and len(subcategory) > 0:
        result = CHOOSE_CATEGORY_OR_ITEMS[language]
    elif len(items) > 0:
        result = CHOOSE_PRODUCT[language]
    elif len(subcategory) > 0:
        result = CHOOSE_CATEGORY[language]
    return result


NOT_FOUND_ITEM = {
    LANGUAGE_RU: f'К сожалению нет такого товара... 😔',
    LANGUAGE_EN: f'Unfortunately there is no such product... 😔',
    LANGUAGE_UZ: f'Афсуски бундай махсулот йўк... 😔'
}

NOT_FOUND_TO_ADMIN = {
    LANGUAGE_RU: f'К сожалению произошла ошибка... Обратитесь к администратору',
    LANGUAGE_EN: f'Sorry, an error has occurred ... Contact out administrator',
    LANGUAGE_UZ: f'Кечирасиз, хатолик юз берди... Илтимос, администраторимиз билан боғланинг'
}

RECORDED_TO_BASKET = {
    LANGUAGE_RU: 'Добавлено в корзину',
    LANGUAGE_EN: 'Added to cart',
    LANGUAGE_UZ: 'Саватга қўшилти'
}

RECORDED_TO_MORE_ORDER = {
    LANGUAGE_RU: 'Добавлено в доп. заказ',
    LANGUAGE_EN: 'Added to add. order',
    LANGUAGE_UZ: 'Қўшимча буюртмага қўшилди'
}

UNIT_WT = {
    LANGUAGE_RU: 'Штук',
    LANGUAGE_EN: 'Pieces',
    LANGUAGE_UZ: 'Доналар'
}

UNIT_WT_low = {
    LANGUAGE_RU: 'шт',
    LANGUAGE_EN: 'pc',
    LANGUAGE_UZ: 'дона'
}

SCARCE = {
    LANGUAGE_RU: 'Дефицит',
    LANGUAGE_EN: 'Дефицит',
    LANGUAGE_UZ: 'Deficit'
}


def get_desc_of_good(language: str, item: Item):
    text = ''
    if item.running:
        text = SCARCE[language]

    return text.upper()


def def_determine_period(language: str):
    today = date.today().strftime('%d %m %Y')
    initial_period = date.today().replace(day=1).strftime('%d %m %Y')
    determine_period = 'Определите период'
    format_period = 'В таком формате и пример'
    or_choose_below = 'Либо выберите ниже'
    if language == LANGUAGE_EN:
        determine_period = 'Determine the period'
        format_period = 'In this format and an example'
        or_choose_below = 'Or choose below'
    elif language == LANGUAGE_UZ:
        determine_period = 'Даврни аниқланг'
        format_period = 'Ушбу форматда ва мисол'
        or_choose_below = 'Йоки қуйида танланг'
    result = f"🕒 {determine_period}\n\n{format_period}:\n<b>{initial_period}</b>\n<b>{today}</b>\n\n👇 {or_choose_below}"
    return result


def get_recorded_to_basket(item_name: str, quantity: Union[int, str], price: Union[str, int], language: str,
                           remainder: Union[str, int], access_more_order=False):
    total = int(price) * int(quantity)
    result = '\n\n'.join([
        f'✅ {item_name.capitalize()} - <b>{RECORDED_TO_BASKET[language].lower() if not access_more_order else RECORDED_TO_MORE_ORDER[language].lower()}</b> <code>{quantity}</code> <b>{UNIT_WT[language].lower()}</b>',
        get_remainder(language=language, num=remainder),
        get_amount(language=language, num=price)
    ])
    result += f"\n{get_total(language=language, total=total)}"
    return result


YOUR_ORDER = {
    LANGUAGE_RU: 'Ваш заказ',
    LANGUAGE_EN: 'Your order',
    LANGUAGE_UZ: 'Сизнинг буюртмангиз'
}

YOUR_MORE_ORDER = {
    LANGUAGE_RU: 'Доп. заказ',
    LANGUAGE_EN: 'Add. order',
    LANGUAGE_UZ: 'Қўшимча буюртма'
}

LOADING = {
    LANGUAGE_RU: 'Загрузка... 🚀',
    LANGUAGE_EN: 'Loading... 🚀',
    LANGUAGE_UZ: 'Юклаш... 🚀'
}

YOU_SHOULD_BUY = {
    LANGUAGE_RU: 'Минимальное количество товаров',
    LANGUAGE_EN: 'Minimum quantity of goods',
    LANGUAGE_UZ: 'Товарларнинг минимал миқдори'
}

HAS_NOT_ENOUGH = {
    LANGUAGE_RU: 'На складе, не хватает',
    LANGUAGE_EN: 'In stock, not enough',
    LANGUAGE_UZ: 'Стокда, етарли емас'
}

CHANGED_QUANTITY_RUNNING = {
    LANGUAGE_RU: 'Ходовые товары, изменилось количество',
    LANGUAGE_EN: 'Hot goods, quantity changed',
    LANGUAGE_UZ: 'Иссиқ махсулотлар, уларнинг сони ўзгарган'
}

FAILURE = {
    LANGUAGE_RU: 'Произошла ошибка, попробуйте позже...',
    LANGUAGE_EN: 'An error occured, please try later...',
    LANGUAGE_UZ: 'Хато юз берди, илтимос кейинроқ уриниб кўринг...'
}

MENU = {
    LANGUAGE_RU: 'Меню',
    LANGUAGE_EN: 'Menu',
    LANGUAGE_UZ: 'Меню'
}

TOTAL = {
    LANGUAGE_RU: 'Всего',
    LANGUAGE_EN: 'Total',
    LANGUAGE_UZ: 'Жами'
}

QUANTITY = {
    LANGUAGE_RU: 'Количество',
    LANGUAGE_EN: 'Quantity',
    LANGUAGE_UZ: 'Миқдор'
}

EMPTY_BASKET = {
    LANGUAGE_RU: '🛒 Корзина пуста',
    LANGUAGE_EN: '🛒 Basket is empty',
    LANGUAGE_UZ: '🛒 Сават бўш'
}

CART_EMPTIED = {
    LANGUAGE_RU: '✅ Корзина очищена',
    LANGUAGE_EN: '✅ Cart has been emptied',
    LANGUAGE_UZ: '✅ Сават бўшатилди'
}

ADDITIONAL_ORDER_EMPTIED = {
    LANGUAGE_RU: '🗑 Доп. заказ очищен',
    LANGUAGE_EN: '🗑 Add. order cleared',
    LANGUAGE_UZ: '🗑 Қўшиш буюртма тозаланди'
}

WRITE_QUANTITY = {
    LANGUAGE_RU: '⚠ Введите количество',
    LANGUAGE_EN: '⚠ Enter quantity',
    LANGUAGE_UZ: '⚠ Миқдорини киритинг'
}

WANT_TO_ADD_BASKET = {
    LANGUAGE_RU: 'Хотите заказать еще?',
    LANGUAGE_EN: 'Want to order more?',
    LANGUAGE_UZ: 'Кўпроқ буюртма беришни хошлайсизми?'
}

SEND_NUMBER = {
    LANGUAGE_RU: '📱 Отправьте или введите номер телефона (можно и несколько через запятую)\n'
                 'В таком формате: <b>+998 ** *** ****</b>',
    LANGUAGE_EN: '📱 Send or enter a phone number (you can also have several separated by commas)\n'
                 'In this format: <b>+998 ** *** ****</b>',
    LANGUAGE_UZ: '📱 Телефон рақамини юборинг ёки киритинг (бир нечта вергул билан ажратилган бўлиши мумкин)\n'
                 'Ушбу форматда: <b>+998 ** *** ****</b>'
}

SEND_LOCATION = {
    LANGUAGE_RU: '📍 Отправьте вашу локацию или введите ориентир',
    LANGUAGE_EN: '📍 Send your location or enter a landmark',
    LANGUAGE_UZ: '📍 Жойлашувингизни юборинг ёки белгини киритинг'
}

SEND_ME_TYPE_OF_PAYMENTS = {
    LANGUAGE_RU: 'Выберите способ оплаты за Ваш заказ',
    LANGUAGE_EN: 'Select a payment method for your order',
    LANGUAGE_UZ: 'Буюртма учун тўлов усулини танланг'
}

PHONE_NUMBER = {
    LANGUAGE_RU: 'Телефон',
    LANGUAGE_EN: 'Phone number',
    LANGUAGE_UZ: 'Телефон'
}

NOT_SET = {
    LANGUAGE_RU: 'Не задано',
    LANGUAGE_EN: 'Not set',
    LANGUAGE_UZ: 'Ўрнатилмаган'
}

ADDRESS = {
    LANGUAGE_RU: 'Адрес',
    LANGUAGE_EN: 'Address',
    LANGUAGE_UZ: 'Манзил'
}

COMMENT = {
    LANGUAGE_RU: 'Комментарий',
    LANGUAGE_EN: 'Comment',
    LANGUAGE_UZ: 'Шарх'
}

TYPE_OF_PAYMENT = {
    LANGUAGE_RU: 'Способ оплаты',
    LANGUAGE_EN: 'Payment method',
    LANGUAGE_UZ: 'Тўлов усули'
}

ACCEPTED = {
    LANGUAGE_RU: 'Принят',
    LANGUAGE_EN: 'Accepted',
    LANGUAGE_UZ: 'Қабул қилинган'
}

CANCELED = {
    LANGUAGE_RU: 'Отменен',
    LANGUAGE_EN: 'Canceled',
    LANGUAGE_UZ: 'Бекор қилинди'
}

ORDER_STATUS = {
    LANGUAGE_RU: 'Статус заказа',
    LANGUAGE_EN: 'Order status',
    LANGUAGE_UZ: 'Буюртма холади'
}

EMPTY_ORDER = {
    LANGUAGE_RU: 'Нет истории заказов 😕',
    LANGUAGE_EN: 'No order history 😕',
    LANGUAGE_UZ: 'Буюртма тарихи йўк 😕'
}

DONT_HACK_ME = {
    LANGUAGE_RU: 'Не пытайтесь меня взломать 😔',
    LANGUAGE_EN: 'Don\'t try to hack me 😔',
    LANGUAGE_UZ: 'Мени бузишга уринманг 😔'
}

NOTE = {
    LANGUAGE_RU: 'Примечание',
    LANGUAGE_EN: 'Note',
    LANGUAGE_UZ: 'Еслатма'
}


async def get_text_for_item(basket_item, language, attr=None, quantity=None):
    if attr is None:
        attr = others.get_attribute_by_language(language=language)
    if quantity is None:
        quantity = basket_item.quantity
    item = basket_item.product
    total = item.price * quantity

    reminder = item.reminder
    if not item.reminder:
        reminder = NOT_SET[language].lower()
    text = f"<b>{getattr(item, attr)}</b> ({get_remainder(language=language, num=item.reminder)})"

    # text += f"\n\n {get_remainder(language=language, num=item.reminder)}"
    text += f"\n\n {get_amount(language=language, num=item.price)}"
    text += f"\n {get_total(language=language, total=total)}"
    return text


async def get_text_for_item_2(quantity, item, language):
    attr_desc = others.get_attribute_by_language(language=language, name_object='description')
    total = quantity * item.price

    text = f"{markdown.hbold(getattr(item, others.get_attribute_by_language(language=language)))} ({get_remainder(language=language, num=item.reminder)})"
    result_description = getattr(item, attr_desc)
    if result_description:
        text += f"\n\n {result_description}"
    # text += f"\n\n {get_remainder(language=language, num=item.reminder)}"
    text += f"\n\n {get_amount(language=language, num=item.price)}"
    text += f"\n {get_total(language=language, total=total)}"

    return text


def get_title_delete_from_basket(product: str, language: str):
    result = ''
    if language == LANGUAGE_RU:
        result = f"✅ Удалено <b>{product}</b> из корзины"
    elif language == LANGUAGE_UZ:
        result = f"✅ Саватдан <b>{product}</b> олинди"
    elif language == LANGUAGE_EN:
        result = f"✅ Removed <b>{product}</b> from the cart"
    return result


def get_title_order(language: str, basket_items, additional_order={'order_list': [], "access": False}):
    total = 0
    total_quantity = 0
    result = f'<b>——————{YOUR_ORDER[language].upper()}————————</b>\n\n'

    # result += f"\n<b>📒 {MENU[language].upper()}:</b>\n\n"
    attr = others.get_attribute_by_language(language=language)
    i = 1
    for bst_item in basket_items:
        total_one = bst_item.quantity * bst_item.product.price
        total_quantity += bst_item.quantity
        total += total_one

        result += f"<b>{i}) {getattr(bst_item.product, attr)}</b> (" \
                  f"{get_remainder(language=language, num=bst_item.product.reminder)}) - " \
                  f"<code>{bst_item.quantity}</code> x " \
                  f"<code>{bst_item.product.price} {get_currency(language=language).lower()}</code> = <code>{total_one} {SUM[language].lower()}</code>" \
                  f'\n'
        i = i + 1

    result += f"\n<b>{TOTAL[language].upper()}:</b> {'{:,}'.format(total_quantity).replace(',', ' ')} {UNIT_WT_low[language].lower()}; {'{:,}'.format(total).replace(',', ' ')} {get_currency(language=language).lower()}\n\n"

    # ----------- MORE_ORDER ----------
    order_list = additional_order['order_list']
    if additional_order['access']:
        if len(order_list) > 0:
            result += f'<b>———————{YOUR_MORE_ORDER[language].upper()}————————</b>\n'

        total = 0
        total_quantity = 0
        i = 1
        for add_order in order_list:
            total_one = add_order['quantity'] * add_order['item'].price
            total_quantity += add_order['quantity']
            total += total_one

            result += f"<b>{i}) {getattr(add_order['item'], attr)}</b> (" \
                      f"{get_remainder(language=language, num=add_order['item'].reminder)}) - " \
                      f"<code>{add_order['quantity']}</code> x " \
                      f"<code>{add_order['item'].price} {get_currency(language=language).lower()}</code> = <code>{total_one} {SUM[language].lower()}</code>" \
                      f'\n'
            i = i + 1

        if len(order_list) > 0:
            result += f"\n<b>{TOTAL[language].upper()}:</b> {'{:,}'.format(total_quantity).replace(',', ' ')} {UNIT_WT_low[language].lower()}; {'{:,}'.format(total).replace(',', ' ')} {get_currency(language=language).lower()}"

    return result


async def get_data_user(language: str):
    data = await dp.current_state().get_data()
    location = data.get("location")
    phone_number = data.get("phone_number")
    comment = data.get("comment")
    type_of_payment = data.get("type_of_payment")
    title_phone_number = f"<b>{PHONE_NUMBER[language]}</b>: {phone_number if phone_number else NOT_SET[language]}"
    title_address = f"<b>{ADDRESS[language]}</b>: {location if location else NOT_SET[language]}"
    title_comment = f"<b>{COMMENT[language]}</b>: {comment if comment else NOT_SET[language]}"
    # title_type_of_payment = f"<b>{TYPE_OF_PAYMENT[language]}</b>: {type_of_payment if type_of_payment else NOT_SET[language]}"
    # result = '\n'.join([title_phone_number, title_address, title_type_of_payment, title_comment])
    result = '\n'.join([title_phone_number, title_address, title_comment])
    return result


async def title_accepted_order(language: str, basket_items, id: Union[str, int], order_additional_list):
    result = await title_confirm_order(language=language, basket_items=basket_items, id=id,
                                       order_additional_list=order_additional_list)
    return result


def get_canceled_order(id, language: str):
    result = f"❌ {YOUR_ORDER[language].upper()} - #{id} - {CANCELED[language].upper()}"
    return result


async def title_confirm_order(language: str, basket_items, id: Union[str, int] = None, order_additional_list=None):
    total = 0
    total_quantity = 0
    contacts_user = await get_data_user(language)
    if id:
        result = '\n\n'.join([
            f"<b>{YOUR_ORDER[language].upper()} - #{id}</b>\n✅ {ACCEPTED[language]}!",
            contacts_user,
            f'———————<b>{YOUR_ORDER[language].upper()}</b>————————\n'
        ])
    else:
        result = '\n\n'.join([
            f"<b>{YOUR_ORDER[language].upper()}</b>",
            contacts_user,
            f'———————<b>{YOUR_ORDER[language].upper()}</b>————————\n'
        ])

    attr = others.get_attribute_by_language(language=language)
    i = 1
    for bst_item in basket_items:
        total_one = bst_item.quantity * bst_item.product.price
        total_quantity += bst_item.quantity
        total += total_one
        result += f"<b>{i}) {getattr(bst_item.product, attr)}</b> - " \
                  f"<code>{bst_item.quantity}</code> x " \
                  f"<code>{bst_item.product.price} {get_currency(language=language).lower()}</code> = <code>{total_one} {SUM[language].lower()}</code>" \
                  f'\n'
        i = i + 1
    result += f"\n<b>{TOTAL[language].upper()}:</b> {'{:,}'.format(total_quantity).replace(',', ' ')} {UNIT_WT_low[language].lower()}; {'{:,}'.format(total).replace(',', ' ')} {get_currency(language=language).lower()}\n\n"

    # more_order
    if order_additional_list is not None and len(order_additional_list) > 0:
        total = 0
        total_quantity = 0

        result += f'———————<b>{YOUR_MORE_ORDER[language].upper()}</b>————————\n'
        i = 1
        for order_add in order_additional_list:
            total_one = order_add.quantity * order_add.product.price
            total_quantity += order_add.quantity
            total += total_one
            result += f"<b>{i}) {getattr(order_add.product, attr)}</b> - " \
                      f"<code>{order_add.quantity}</code> x " \
                      f"<code>{order_add.product.price} {get_currency(language=language).lower()}</code> = <code>{total_one} {SUM[language].lower()}</code>" \
                      f'\n'
            i = i + 1
        result += f"\n<b>{TOTAL[language].upper()}:</b> {'{:,}'.format(total_quantity).replace(',', ' ')} {UNIT_WT_low[language].lower()}; {'{:,}'.format(total).replace(',', ' ')} {get_currency(language=language).lower()}"

    return result


# ----------------------------------------- MY ORDERS -------------------------------------

async def title_my_order(language: str, order):
    total = 0
    contacts_user = await get_data_order(language, order)

    order_status = order.order_status
    order_status = ORDER_STATUSES[order_status].get(language)
    title_order_status = f"<b>{ORDER_STATUS[language]}</b>: {order_status if order_status else NOT_SET[language]}"

    note = order.note
    title_note = f"<b>{NOTE[language]}</b>: {note if note else NOT_SET[language]}\n"

    line = '———————————————'
    result = '\n'.join([
        f"<b>{YOUR_ORDER[language].upper()} - #{order.id}</b>\n",
        contacts_user,
        f'{line}\n'
    ])

    attr = others.get_attribute_by_language(language=language)
    i = 1
    order_items = await db_commands.get_order_item_filter(order=order)
    if order_items:
        for order_item in order_items:
            total += order_item.quantity * order_item.price
            result += f"<b>{i}) {getattr(order_item.product, attr)}</b> - <code>{order_item.quantity}</code> x <code>{order_item.price}</code> {get_currency(language=language).lower()}" \
                      f'\n'
            i = i + 1
    result += f"\n<b>{TOTAL[language].upper()}:</b> {'{:,}'.format(total).replace(',', ' ')} {get_currency(language=language).lower()}\n\n"

    more_order_items = await db_commands.get_more_order_item_filter(order=order)
    if more_order_items and len(more_order_items):
        total = 0
        total_quantity = 0

        result += f'———————<b>{YOUR_MORE_ORDER[language].upper()}</b>————————\n'
        i = 1
        for more_order in more_order_items:
            total += more_order.quantity * more_order.price
            result += f"<b>{i}) {getattr(more_order.product, attr)}</b> - <code>{more_order.quantity}</code> x <code>{more_order.price}</code> {get_currency(language=language).lower()}" \
                      f'\n'
            i = i + 1

        result += f"\n<b>{TOTAL[language].upper()}:</b> {'{:,}'.format(total).replace(',', ' ')} {get_currency(language=language).lower()}\n\n"

    result += f"{line}\n{title_order_status}\n{title_note}"
    return result


async def get_data_order(language: str, order):
    location = order.address
    phone_number = order.phone_number
    comment = order.comment

    type_of_payment = None
    if order.type_of_payment:
        type_of_payment = TYPES_OF_PAYMENT[order.type_of_payment].get(language)
    title_phone_number = f"<b>{PHONE_NUMBER[language]}</b>: {phone_number if phone_number else NOT_SET[language]}"
    title_address = f"<b>{ADDRESS[language]}</b>: {location if location else NOT_SET[language]}"
    title_comment = f"<b>{COMMENT[language]}</b>: {comment if comment else NOT_SET[language]}"
    # title_type_of_payment = f"<b>{TYPE_OF_PAYMENT[language]}</b>: {type_of_payment if type_of_payment else NOT_SET[language]}"

    result = '\n'.join([title_phone_number,
                        title_address, title_comment])
    # title_type_of_payment,

    return result


async def get_text_for_calculator(quantity: int, item, language: str, sample_quantity: int):
    total = quantity * item.price

    text = f"{markdown.hbold(getattr(item, others.get_attribute_by_language(language=language)))} ({get_remainder(language=language, num=item.reminder)})"
    # attr_desc = others.get_attribute_by_language(language=language, name_object='description')
    # result_description = getattr(item, attr_desc)
    # if result_description:
    #     text += f"\n\n {result_description}"
    # text += f"\n\n {get_remainder(language=language, num=item.reminder)}"
    text += f"\n\n {get_amount(language=language, num=item.price)}"
    text += f"\n {get_total(language=language, total=total)}"
    text += f"\n {get_quantity(language=language, quantity=quantity)}"
    text += f"\n\n {get_sample_quantity(language=language, num=sample_quantity)}"

    return text
