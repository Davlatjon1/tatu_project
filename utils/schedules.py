import base64
import logging
import os
from aiogram import types
from django.utils import timezone
import datetime
from data import config
from django_project.telegrambot.constants.models import Constants, Restrict_Users_TGBOT
from django_project.telegrambot.usersmanage.models import User, Order
from handlers import botControlOrder, botControl
from loader import scheduler, dp
from utils.db_api import db_commands
import requests
from requests.auth import HTTPBasicAuth


async def send_message_to_users_about_turnover():
    constant: Constants = Constants.default_constant()
    if constant.setting_api is None:
        return
    clients_uuid, key_attr = await db_commands.get_clients_uuid_1c_inside_users(access=True, access_act_sverki=True)
    clients_uuid = [client_uuid.get(key_attr) for client_uuid in clients_uuid]
    params = {'clients_uuid': clients_uuid}
    URL_MAILING_ACT_SVERKI = ''
    try:
        response = requests.post(url=URL_MAILING_ACT_SVERKI,
                                 auth=HTTPBasicAuth(constant.setting_api.login_1c.encode('UTF-8'),
                                                    constant.setting_api.password_1c.encode('UTF-8')),
                                 json=params)
        if response.status_code == 200:
            response_params = response.json()
            results = response_params['results']
            for res in results:
                users = await db_commands.get_users(access=True, client__uuid_1c=res['client_uuid'],
                                                    access_act_sverki=True)
                data = base64.b64decode(res['file_base64'])
                period_str = f"c {res['initial_period']}-{res['end_period']}" if res['initial_period'] != res[
                    'end_period'] else f"на {res['initial_period']}"
                output_file = f"Акт сверки {period_str}.pdf"
                data_file = open(output_file, 'wb')
                data_file.write(data)
                for user in users:
                    user_id = user.user_id
                    try:
                        await dp.bot.send_document(chat_id=user_id, document=types.InputFile(output_file))
                    except Exception as err:
                        logging.error(f"error: {err}")
                        logging.info(f"info: {err}")
                if os.path.exists(output_file):
                    os.remove(output_file)
        else:
            logging.info(f'{response.text=} {response.reason}')
    except Exception as err:
        logging.info(err)


async def restrict_user_schedule():
    enabled = False
    days = 0
    constant = Constants.default_constant()
    disabled_users = []
    if constant is not None and constant.restrict_users is not None:
        restrict_users: Restrict_Users_TGBOT = constant.restrict_users
        days = restrict_users.days
        enabled = restrict_users.enabled
        dis_users = restrict_users.disabled_users.filter(disabled=True).values('user__user_id').distinct()
        disabled_users = [dis_user.get('user__user_id') for dis_user in dis_users]

    if not disabled_users:
        disabled_users.append(0)

    if enabled and days > 0:
        date = timezone.now() - datetime.timedelta(days=days)
        date_str = date.strftime("%Y-%m-%d")

        disabled_users_str = ','.join(str(_user) for _user in disabled_users)
        query_text = f"""SELECT nested.id, nested.max_date FROM (SELECT usersmanage_user.id, 
        MAX(usersmanage_order.created_at) AS max_date 
        FROM usersmanage_user LEFT JOIN usersmanage_order 
        ON usersmanage_user.id = usersmanage_order.buyer_id 
        WHERE (NOT (usersmanage_user.user_id IN ({disabled_users_str})) 
        AND usersmanage_user.access AND usersmanage_user.created_at < '{date_str}') GROUP BY usersmanage_user.id) AS nested WHERE 
        (nested.max_date IS NULL OR nested.max_date < '{date_str}')"""

        users_blocked = '🔒 <b>Пользователи заблокированы:</b>\n'
        users = User.objects.raw(query_text)
        for user in users:
            date_str = 'Пустая дата' if not isinstance(user.max_date, datetime.datetime) \
                else user.max_date.strftime("%d-%m-%Y")

            text_user = user.name
            if user.username:
                text_user = f"<a href='https://t.me/{user.username}'>{user.name}</a>"

            # text_id = f"<a href='http://127.0.0.1:8000/admin/usersmanage/user/{user.id}/change/'>Edit</a>"
            text_id = f"<a href='http://62.113.116.131:9222/admin/usersmanage/user/{user.id}/change/'>Edit</a>"

            users_blocked += f"{text_id} - {text_user}: {date_str}\n"
            user.access = False
            user.save()
        if users:
            await botControl.send_to_group(text=users_blocked)
            # await dp.bot.send_message(20936078, text=users_blocked)


def schedule_jobs():
    # scheduler.add_job(send_message_to_users_about_turnover, "interval", seconds=10, args=(), replace_existing=True)
    scheduler.add_job(send_message_to_users_about_turnover, 'cron', hour=18, minute=0)
    scheduler.add_job(restrict_user_schedule, 'cron', hour=19, minute=0)
    # scheduler.add_job(restrict_user_schedule, 'interval', seconds=5, replace_existing=False, args=())
