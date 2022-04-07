from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import MAIN_LANGUAGE_INLINE_MODE
from loader import bot, dp
from utils.db_api import db_commands
from utils.values.others import get_attribute_by_language


class AfterMode_ViaBot(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        result = False
        if type(message.via_bot) == types.User:
            if message.via_bot.id == bot.id:
                result = True
                # attr = get_attribute_by_language(MAIN_LANGUAGE_INLINE_MODE)
                # item = await db_commands.get_item_filter(first=True, show_bot=True,
                #                                          **{f"{attr}__icontains": message.text})
                # if item:
                #     result = True
        return result


class IsUserHasBlockMessage(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user = await db_commands.get_user(user_id=message.from_user.id,
                                          full_name=message.from_user.full_name,
                                          username=message.from_user.username)
        return not user.access


class AddToBasket(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        data = await dp.current_state().get_data()
        message_caption = data.get("message_caption")
        item_id_adding = data.get("item_id_adding")
        return message.text.isdigit() and message_caption is not None and item_id_adding is not None
