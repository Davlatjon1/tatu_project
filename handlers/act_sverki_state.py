import base64
import datetime
import os
from data import config
from data.config import LANGUAGE_RU
from django_project.telegrambot.constants.models import Constants, SettingsAPI
from django_project.telegrambot.usersmanage.models import User
from aiogram.types import Message, InputFile
import requests
from requests.auth import HTTPBasicAuth
import logging
from handlers import botControl
from utils.values import values_title


async def act_sverki_text(user: User, message: Message, start_period: str, end_period: str):
    if user.client is None \
            or datetime.datetime.strptime(start_period, '%d.%m.%Y') > datetime.datetime.strptime(end_period,
                                                                                                 '%d.%m.%Y'):
        await botControl.act_sverki(user=user, message=message)
        return
    await message.answer(values_title.LOADING[user.language])
    constant: Constants = Constants.default_constant()
    params = {'start_period': start_period, 'end_period': end_period, 'client': user.client.uuid_1c,
              "group_of_counterparties": user.access_group_of_counterparties}
    try:
        response = requests.post(url=constant.setting_api.url_to_act_sverki,
                                 auth=HTTPBasicAuth(constant.setting_api.login_1c.encode('UTF-8'),
                                                    constant.setting_api.password_1c.encode('UTF-8')),
                                 json=params)
        if response.status_code == 200:
            response_params = response.json()

            for res in response_params['results']:
                if constant.setting_api.type_of_act_sverki == SettingsAPI.TypeOfActSverki.FILE_PDF:
                    data = base64.b64decode(res['file_base64'])
                    period_str = f"c {res['initial_period']}-{res['end_period']}" if res['initial_period'] != res[
                        'end_period'] else f"на {res['initial_period']}"
                    output_file = f"Акт_сверки {period_str}.pdf"
                    caption = (res['client']['name']).upper()
                    data_file = open(output_file, 'wb')
                    data_file.write(data)
                    try:
                        await message.answer_document(document=InputFile(output_file), caption=caption)
                    except Exception as err:
                        logging.error(f"error: {err}")
                        logging.info(f"info: {err}")

                    if os.path.exists(output_file):
                        os.remove(output_file)
                else:
                    text = f'<i>📃Акт сверки на {start_period} - {end_period}</i>\n\n'
                    text += f"<b>Валюта:</b> {res['currency']}\n"
                    text += f"<b>Клиент:</b> {res['client']['name'] if res['client']['name'] else values_title.NOT_SET[LANGUAGE_RU]}\n"
                    text += '-------------------------\n'
                    text += f"<b>⏳Нач. остаток:</b> {res['initial_balance']}\n"
                    text += f"<b>💸Продажа:</b> {res['debit_turnover']}\n"
                    text += f"<b>💰Оплата:</b> {res['credit_turnover']}\n"
                    text += f"<b>⌛️Кон. остаток:</b> {res['final_balance']}\n"
                    text += '-------------------------\n'
                    text += f"🕰 Сформировано: <code>{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}</code>"

                    await message.answer(text=text)
            await botControl.home_state(language=user.language, message=message)
        else:
            await message.answer(values_title.FAILURE[user.language])
            await botControl.home_state(language=user.language, message=message)
            await botControl.send_to_group(text=f"text: {response.text}, reason: {response.reason}", user=user)

    except SyntaxError as err:
        # print(err)
        await message.answer(values_title.FAILURE[user.language])
        await botControl.home_state(language=user.language, message=message)
        await botControl.send_to_group(text='❌' + str(err), user=user)
