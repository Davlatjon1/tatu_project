import asyncio
from time import sleep
from typing import Union

import emoji
import requests
from aiogram.types import ParseMode
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_project.telegrambot.usersmanage.models import User
from loader import dp
from utils.db_api import db_commands
from loader import bot_tel


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def mailing_index(request, *args, **kwargs):
    results = request.data.get('results')
    users = request.data.get('users')
    photo_id = request.data.get('photo_id')
    if isinstance(results, list):
        try:
            for text in results:
                send_message_to_clients(text=text, users=users,photo_id=photo_id)
            return Response(data="Done", status=status.HTTP_200_OK)
        except Exception as err:
            return Response(data=f"При отправки произошла ошибка... {err}", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(data='Неверный тип', status=status.HTTP_404_NOT_FOUND)


def send_message_to_clients(text, users=None, photo_id=None):
    if users is None:
        users = [user.user_id for user in db_commands.get_available_users()]

    text = emoji.emojize(text)
    for user_id in users:
        try:
            if photo_id:
                bot_tel.send_photo(chat_id=user_id, photo=photo_id, caption=text)
            else:
                bot_tel.send_message(chat_id=user_id, text=text, parse_mode='html')
        except Exception as err:
            print(err)
