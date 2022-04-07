from aiogram import Dispatcher

from loader import dp
from .filters import AfterMode_ViaBot, AddToBasket, IsUserHasBlockMessage


if __name__ == "filters":
    dp.filters_factory.bind(AfterMode_ViaBot)
    dp.filters_factory.bind(AddToBasket)
    dp.filters_factory.bind(IsUserHasBlockMessage)
