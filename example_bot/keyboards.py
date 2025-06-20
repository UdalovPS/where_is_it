import logging
from typing import List, Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import schemas


logger = logging.getLogger(__name__)


class BranchCallback(CallbackData, prefix="branch"):
    action: str  # Обязательно указываем типы полей
    id: int


class LocationCallback(CallbackData, prefix="location"):
    action: str  # Обязательно указываем типы полей
    id: int


class ItemCallback(CallbackData, prefix="item"):
    action: str  # Обязательно указываем типы полей
    id: int


class Emoji:
    back = "🔙"  # стрелка назад
    lupa = "🔍"  # лупа
    cart = "🛒"  # тележка для покупок
    store = "🏪"
    geo = "📍"
    hand = "🖐"
    cancel = "\U0000274C"
    ok = "\U00002705"
    pencil = "\U0000270F"
    warn = "\U000026A0"
    plus = "\U00002795"
    clock = "\U000023F3"
    blue = "\U0001F535"
    finger_right = "\U0001F449"


def create_main_menu_board():
    """Создание кнопки для главного меню"""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"{Emoji.lupa} Найти один товар",
        callback_data="find_one"
    )
    builder.button(
        text=f"{Emoji.cart} Найти список товаров",
        callback_data="find_many"
    )
    builder.button(
        text=f"{Emoji.store} Выбрать магазин",
        callback_data="choice_branch"
    )
    builder.adjust(1)  # Расположить кнопки в 1 колонку
    return builder.as_markup()

def create_init_geo_menu_board():
    """Создание кнопок создания меню выбора геолокации"""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"{Emoji.geo} По геолокации",
        callback_data="location_geo",
        request_location=True
    )
    builder.button(
        text=f"{Emoji.hand} Выбрать вручную",
        callback_data="location_hand"
    )
    builder.button(
        text=f"{Emoji.back} Назад",
        callback_data="main_menu"
    )
    builder.adjust(1)  # Расположить кнопки в 1 колонку
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def create_send_geolocation_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text=f"{Emoji.geo} Отправить геолокацию", request_location=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def create_choice_branches_by_geo_menu(data: List[schemas.BranchSchema]):
    """Создаем меню выбора филиалов по геолокации"""
    builder = InlineKeyboardBuilder()
    for branch in data:
        builder.button(
            text=f"{branch.city_data.name}. {branch.address}",
            callback_data=BranchCallback(action="update_branch", id=branch.id).pack()
        )
    builder.button(
        text=f"{Emoji.cancel} Отмена",
        callback_data=BranchCallback(action="update_branch",id=0).pack()
    )
    builder.adjust(1)
    return builder.as_markup()

def create_choice_countries_menu(data: List[schemas.CountrySchem]):
    """Создание меню выбора страны"""
    builder = InlineKeyboardBuilder()
    for country in data:
        builder.button(
            text=country.name,
            callback_data=LocationCallback(
                action="choice_country",
                id=country.id,
            ).pack()
        )
    builder.button(
        text=f"{Emoji.back} Назад",
        callback_data=LocationCallback(
            action="choice_country",
            id=0,
        ).pack()
    )
    builder.adjust(1)
    return builder.as_markup()

def create_choice_district_menu(data: List[schemas.DistrictSchem]):
    """Создание меню выбора регионов"""
    builder = InlineKeyboardBuilder()
    for district in data:
        builder.button(
            text=district.name,
            callback_data=LocationCallback(
                action="choice_district",
                id=district.id,
            ).pack()
        )
    builder.button(
        text=f"{Emoji.pencil} Ввести заново",
        callback_data=LocationCallback(
            action="choice_district",
            id=0,
        ).pack()
    )
    builder.button(
        text=f"{Emoji.back} К выбору страны",
        callback_data=LocationCallback(
            action="choice_district",
            id=-1,
        ).pack()
    )
    builder.adjust(1)
    return builder.as_markup()

def create_choice_city_menu(data: List[schemas.CitySchem]):
    """Создание меню выбора городов"""
    builder = InlineKeyboardBuilder()
    for city in data:
        builder.button(
            text=city.name,
            callback_data=LocationCallback(
                action="choice_city",
                id=city.id,
            ).pack()
        )
    builder.button(
        text=f"{Emoji.pencil} Ввести заново",
        callback_data=LocationCallback(
            action="choice_city",
            id=0,
        ).pack()
    )
    builder.button(
        text=f"{Emoji.back} К выбору региона",
        callback_data=LocationCallback(
            action="choice_city",
            id=-1,
        ).pack()
    )

    builder.adjust(1)
    return builder.as_markup()

def create_choice_branches_menu(data: List[schemas.BranchSchema]):
    """Создание меню выбора магазинов по адресу"""
    builder = InlineKeyboardBuilder()
    for branch in data:
        builder.button(
            text=branch.name,
            callback_data=LocationCallback(
                action="choice_branch",
                id=branch.id,
            ).pack()
        )
    builder.button(
        text=f"{Emoji.pencil} Ввести заново",
        callback_data=LocationCallback(
            action="choice_branch",
            id=-1,
        ).pack()
    )
    builder.button(
        text=f"{Emoji.back} К выбору города",
        callback_data=LocationCallback(
            action="choice_branch",
            id=-2,
        ).pack()
    )
    builder.adjust(1)
    return builder.as_markup()

def create_choice_items_meny(data: Optional[List[schemas.SimilarItemsSchem]] = None, many: bool = False):
    """Создание меню выбора товаров"""
    builder = InlineKeyboardBuilder()
    if data:
        for item in data:
            builder.button(
                text=f"{item.category} [{item.name}]",
                callback_data=ItemCallback(
                    action="one_item" if not many else "many_item",
                    id=item.id,
                ).pack()
            )
    builder.button(
        text="Отмена",
        callback_data=ItemCallback(
            action="one_item" if not many else "many_item",
            id=0,
        ).pack()
    )
    builder.adjust(1)
    return builder.as_markup()

def create_many_items_choice():
    """Создание меню в котором у пользователя спрашивается нужно
    ли добавить еще товар или отобращить то что уже есть
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"{Emoji.plus} Добавить еще",
        callback_data="find_many"
    )
    builder.button(
        text=f"{Emoji.lupa} Найти товары",
        callback_data=ItemCallback(
            action="many_choice",
            id=2,
        ).pack()
    )
    builder.button(
        text=f"{Emoji.cancel} Отмена",
        callback_data=ItemCallback(
            action="many_choice",
            id=0,
        ).pack()
    )
    builder.adjust(1)
    return builder.as_markup()
