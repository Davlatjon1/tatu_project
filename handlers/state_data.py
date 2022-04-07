from django_project.telegrambot.usersmanage.models import Item
from loader import dp
from states.default import StateOrder


async def update_more_order(reset_list=False, access=False, check_access=True):
    if access and check_access:  # проверка state вдруг аралаш
        access = (await dp.current_state().get_state()) == StateOrder.additional_order.state

    structure = {'order_list': [], 'access': access}
    if reset_list:
        await dp.current_state().update_data(additional_order=structure)
    else:
        data = await dp.current_state().get_data()
        structure_data = data.get("additional_order")
        if isinstance(structure_data, dict) and isinstance(structure_data.get("order_list"), list) and isinstance(
                structure_data.get('access'), bool):
            pass
        else:
            await dp.current_state().update_data(additional_order=structure)


async def get_structure_from_more_order() -> dict:
    data = await dp.current_state().get_data()
    additional_order = data.get('additional_order')
    order_list = []
    access = False
    if isinstance(additional_order, dict):
        if additional_order.get('order_list') is not None:
            order_list = additional_order.get('order_list')

        if additional_order.get('access') is not None:
            access = additional_order.get('access')

    if access:
        access = (await dp.current_state().get_state()) == StateOrder.additional_order.state

    structure = {'order_list': order_list, 'access': access}
    return structure


async def get_item_from_more_order(item: Item) -> dict:
    data = await dp.current_state().get_data()
    additional_order = data.get('additional_order')
    result = {'item': item, "quantity": 0}
    if isinstance(additional_order, dict) and isinstance(additional_order.get('order_list'), list):
        for item_add_order in additional_order.get('order_list'):
            if item_add_order['item'] == item:
                result['quantity'] = item_add_order['quantity']
                break
    return result


async def update_item_to_more_order(item: Item, quantity: 0):
    additional_order = await get_structure_from_more_order()
    order_list = additional_order['order_list']
    found = False
    for add_order in order_list[:]:
        if add_order['item'] == item:
            if quantity == 0:
                order_list.remove(add_order)
            else:
                add_order['quantity'] = quantity
            found = True
            break

    if not found and quantity != 0:
        order_list.append({'item': item, 'quantity': quantity})

    additional_order['order_list'] = order_list
    await dp.current_state().update_data(additional_order=additional_order)


async def get_total_quantity_additional_order():
    structure = await get_structure_from_more_order()
    return sum([line['quantity'] for line in
                structure['order_list']])
