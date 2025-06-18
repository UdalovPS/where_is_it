from aiogram.fsm.state import StatesGroup, State


class LocationGeo(StatesGroup):
    """Этапы когда выбирают локацию по ГЕО данным"""
    choice_branch = State()


class LocationHand(StatesGroup):
    """Этапы когда выбирают локацию вручную"""
    choice_district = State()
    choice_city = State()
    choice_branch = State()


class ItemsState(StatesGroup):
    """Этапы поиска товаров на полках"""
    choice_one_item = State()
    choice_many_items = State()