from hashlib import sha224

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django_project.telegrambot.contractors.models import Client, Branch
from django_project.telegrambot.usersmanage.models import Item, Category, Order, OrderItem, User, Subcategory, \
    AdditionOrderItem


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def items_index(request, *args, **kwargs):
    results = request.data.get('results')
    if isinstance(results, list):
        try:
            all_api_items = []
            for line in results:
                api_uuid = str(line["uuid"])
                api_name = ' '.join(str(line['name']).split())
                api_measure = str(line["measure"])
                # api_measure = ''
                if not api_uuid or not api_name:
                    continue
                category = Category.objects.filter(uuid_1c=line['category']['uuid']).first()
                if not category:
                    category = Category()
                    category.name = line['category']['name']
                    category.uuid_1c = line['category']['uuid']
                    category.name_en = category.name
                    category.name_uz = category.name
                    category.save()

                item = Item.objects.filter(uuid_1c=api_uuid).first()
                if not item:
                    item = Item(uuid_1c=api_uuid)
                item.name = api_name
                item.name_uz = item.name
                item.name_en = item.name
                item.category = category
                item.measure = api_measure

                if line.get('price') is not None:
                    api_price = float(line['price'])
                    item.price = api_price

                if line.get('remainder') is not None:
                    api_remainder = float(line['remainder'])
                    item.reminder = api_remainder

                if line.get('subcategory') is not None:
                    api_subcategory = str(line['subcategory'])
                    subcategory = Subcategory.objects.filter(name=api_subcategory).first()
                    if not subcategory:
                        subcategory = Subcategory()
                        subcategory.name = api_subcategory
                        subcategory.name_en = subcategory.name
                        subcategory.name_uz = subcategory.name
                        subcategory.save()
                    item.subcategory = subcategory

                if line.get('id_picture') is not None:
                    api_id_picture = str(line["id_picture"])
                    item.image_url_file_id = api_id_picture

                if isinstance(line.get('running'), bool):
                    item.running = line.get('running')

                if isinstance(line.get('load'), bool):
                    item.load = line.get('load')

                item.save()

                all_api_items.append(item.uuid_1c)
            # ------------------------- EXCLUDES ITEMS --------------------
            exclude_items = Item.objects.exclude(uuid_1c__in=all_api_items).all()
            for excl_item in exclude_items:
                excl_item.price = 0
                excl_item.reminder = 0
                excl_item.running = False
                excl_item.load = False
                excl_item.save()

            return Response(data="Done", status=status.HTTP_200_OK)
        except Exception as err:
            return Response(data=f"При загрузки произошла ошибка... {err}", status=status.HTTP_404_NOT_FOUND)
    else:
        message = 'Неверный тип'
        return Response(data=message, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def clients_index(request, *args, **kwargs):
    results = request.data.get('results')
    if isinstance(results, list):
        try:
            for client_api in results:
                api_name = str(client_api["name"])
                api_uuid = str(client_api["uuid"])
                if not api_uuid or not api_name:
                    continue
                client_object = Client.objects.filter(uuid_1c=api_uuid).first()
                if not client_object:
                    client_object = Client(uuid_1c=api_uuid)
                client_object.name = api_name

                if client_api.get('territory'):
                    client_object.territory = client_api["territory"]

                if client_api.get('days_of_the_week'):
                    client_object.days_of_the_week = client_api["days_of_the_week"]

                if client_api.get('address'):
                    client_object.address = client_api["address"]

                if client_api.get('phone'):
                    client_object.phone = client_api["phone"]

                if client_api.get('deletion_mark'):
                    client_object.deletion_mark = client_api["deletion_mark"]

                if client_api.get('branch') and client_api['branch'].get('uuid') and client_api['branch'].get('name'):
                    api_branch_uuid = client_api['branch']['uuid']
                    branch_object = Branch.objects.filter(uuid_1c=api_branch_uuid).first()
                    if not branch_object:
                        branch_object = Branch(uuid_1c=api_branch_uuid)
                    branch_object.name = client_api['branch']['name']
                    branch_object.save()

                    client_object.branch = branch_object

                client_object.save()

            return Response(data="Done", status=status.HTTP_200_OK)
        except Exception as err:
            return Response(data=f"При загрузки произошла ошибка... {err}", status=status.HTTP_404_NOT_FOUND)
    else:
        message = 'Неверный тип'
        return Response(data=message, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def orders_index(request, *args, **kwargs):
    results = request.data.get('results')
    data = {
        'message': '',
        'results': []
    }
    if isinstance(results, list):
        try:
            for orders_api in results:
                find_order = Order.objects.filter(unique_id=str(orders_api["uuid"])).first()
                if find_order:
                    user = User.objects.filter(user_id=int(orders_api["user_id"])).first()
                    client = Client.objects.filter(uuid_1c=str(orders_api["client"]["uuid"])).first()
                    if not client and orders_api["client"]["name"]:
                        client = Client(uuid_1c=str(orders_api["client"]["uuid"]))
                        client.name = str(orders_api["client"]["name"])
                        client.save()

                    # if user.client != client:
                    #     user.client = client
                    #     user.save()
                    find_order.buyer = user
                    find_order.order_status = orders_api["order_status"]
                    find_order.client = client
                    if orders_api.get('note'):
                        find_order.note = orders_api.get('note')
                    if orders_api.get('comment'):
                        find_order.comment = orders_api.get('comment')
                    find_order.save_updated_from_api()

                    OrderItem.objects.filter(order=find_order).all().delete()
                    for line_api_item in orders_api["list_items"]:
                        line_item = OrderItem(order=find_order)
                        item = Item.objects.filter(uuid_1c=str(line_api_item["item"]["uuid"])).first()
                        if not item:
                            item = Item(uuid_1c=str(line_api_item["item"]["uuid"]))
                            item.name = str(line_api_item["item"]["name"])
                            item.save()
                        line_item.product = item
                        line_item.quantity = float(line_api_item["quantity"])
                        line_item.price = float(line_api_item["price"])
                        line_item.save()

                    # MORE_ORDER
                    AdditionOrderItem.objects.filter(order=find_order).all().delete()
                    for line_api_item in orders_api["additional_order"]:
                        line_item = AdditionOrderItem(order=find_order)
                        item = Item.objects.filter(uuid_1c=str(line_api_item["item"]["uuid"])).first()

                        if not item:
                            item = Item(uuid_1c=str(line_api_item["item"]["uuid"]))
                            item.name = str(line_api_item["item"]["name"])
                            item.save()
                        line_item.product = item
                        line_item.quantity = float(line_api_item["quantity"])
                        line_item.price = float(line_api_item["price"])
                        line_item.save()

            orders = Order.objects.filter(update_api=True).all()
            order_structure(orders, data, uncheck_api=True)
            data["message"] = "Done"
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as err:
            data["message"] = f"При загрузки произошла ошибка... {err}"
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data["message"] = 'Неверный тип'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)


def order_structure(orders, data: dict, uncheck_api: bool = True):
    if data.get('results') is None:
        data['results'] = []
    if orders:
        for order in orders:
            structure_order = {"id": order.id,
                               "uuid": str(order.unique_id),
                               "order_status": str(order.order_status),
                               "date": {'day': order.purchase_time.day,
                                        'month': order.purchase_time.month,
                                        'year': order.purchase_time.year,
                                        'hour': order.purchase_time.hour,
                                        'minute': order.purchase_time.minute,
                                        'second': order.purchase_time.second,
                                        },
                               "user": {
                                   'name': str(order.buyer.name),
                                   'id': int(order.buyer.user_id)},
                               "client": '' if not order.client else str(order.client.uuid_1c),
                               "list_items": [],
                               "additional_order": [],
                               "note": '' if not isinstance(order.note, str) else order.note,
                               "comment": '' if not isinstance(order.comment, str) else order.comment}
            order_items = order.items.all()
            for order_item in order_items:
                structure_order_items = {
                    'item': str(order_item.product.uuid_1c),
                    'quantity': float(order_item.quantity),
                    'price': float(order_item.price),
                }
                structure_order["list_items"].append(structure_order_items)

            additional_order = order.add_items.all()
            for add_order in additional_order:
                structure_add_order = {
                    'item': str(add_order.product.uuid_1c),
                    'quantity': float(add_order.quantity),
                    'price': float(add_order.price),
                }
                structure_order["additional_order"].append(structure_add_order)

            data["results"].append(structure_order)

            if uncheck_api:
                order.save_updated_from_api()
