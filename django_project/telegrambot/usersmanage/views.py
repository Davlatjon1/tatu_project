from hashlib import sha224

from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_project.telegrambot.usersmanage.models import Item
from decimal import Decimal


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_items_index(request, *args, **kwargs):
    data = {
        'message': 'Успешно. Товары',
        'results': []
    }
    items = Item.objects.filter(show_bot=True, reminder__gt=Decimal(0.00)).all()
    for item in items:
        data["results"].append(
            {
                'id': item.id,
                'name': item.name,
                'remainder': item.reminder,
                'price': item.price,
                'price_for': item.price_for,
                'measure': item.measure,
                'description': item.description,
                'picture_id': item.image_url_file_id,
            }
        )
    return Response(data=data, status=status.HTTP_200_OK)
