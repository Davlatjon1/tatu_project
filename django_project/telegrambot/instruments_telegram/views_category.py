from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_project.telegrambot.usersmanage.models import Category


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def category_index(request, *args, **kwargs):
    results = request.data.get('results')
    try:
        all_saved_categories = []
        for res in results:
            api_name = ' '.join(res['name'].split())
            api_uuid = res['uuid']
            api_show_bot = res['show_bot']

            category, created = Category.objects.get_or_create(uuid_1c=api_uuid)
            category.name = api_name
            category.name_en = category.name
            category.name_uz = category.name
            category.show_bot = api_show_bot
            category.save()

            all_saved_categories.append(category.uuid_1c)

        # ------------------------- EXCLUDES ITEMS --------------------
        exclude_categories = Category.objects.exclude(uuid_1c__in=all_saved_categories).all()
        for excl_ctg in exclude_categories:
            excl_ctg.show_bot = False
            excl_ctg.save()

        return Response(data="Done", status=status.HTTP_200_OK)
    except Exception as err:
        return Response(data=f"При загрузки произошла ошибка... {err}", status=status.HTTP_404_NOT_FOUND)
