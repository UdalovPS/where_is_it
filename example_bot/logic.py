import logging
from typing import Optional, Tuple, List

from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

import states
from web_core import WebCore
import keyboards
import schemas

logger = logging.getLogger(__name__)


class ClientLogic:
    """Класс с логикой обработки пути пользователя"""
    web_app = WebCore()

    def __init__(
            self,
            user_id: int,
            name: str,
            username: Optional[str] = None,
    ):
        self.user_id = user_id
        self.name = name
        self.username = username

    async def get_user_data(self) -> Optional[schemas.ClientSchem]:
        """Получение данных пользователя из веб сервера"""
        # извлекаем данные пользователя
        user_data = await self.web_app.get_web_user_data(user_id=self.user_id)
        if not user_data.data and not user_data.error:
            return None
        logger.info(f"{user_data.data}")
        if user_data.error:
            # логика нужно ли создавать нового пользователя
            if user_data.error.name == "NotFoundError":
                user_data = await self.web_app.create_new_user(
                    user_id=self.user_id, name=self.name, username=self.username
                )
                if user_data.error:
                    return None
                else:
                    return user_data.data
        else:
            return user_data.data

    async def get_main_menu_data(self) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Создаем данные для главного меню"""
        user_data = await self.get_user_data()
        if user_data:
            if not user_data.location:
                keyboard = keyboards.create_init_geo_menu_board()
                return "Меню выбора магазина/склада", keyboard
            else:
                keyboard = keyboards.create_main_menu_board()
                return "Главное меню", keyboard
        else:
            return None, None


class ClientGeolocation(ClientLogic):
    """Логический класс для работы с данными локации клиента"""

    @staticmethod
    async def get_init_geo_menu() -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Создаем начальное меню выбора локации"""
        keyboard = keyboards.create_init_geo_menu_board()
        return "Главное меню", keyboard

    @staticmethod
    async def get_send_geo_menu() -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Создаем кнопку отправки геолокации"""
        keyboard = keyboards.create_send_geolocation_menu()
        return "Нажмите на кнопку снизу чтобы отправить геолокацию \U0001F447", keyboard

    async def get_branches_by_geo(
            self,
            latitude: float,
            longitude: float,
            limit: int = 3
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Создаем меню филиала по его геолокации
        Args:
            latitude: широта
            longitude: долгота
            limit: кол-во записей которые нужно вернуть из запроса
        """
        branches = await self.web_app.get_location_by_geo(
            latitude=latitude, longitude=longitude, user_id=self.user_id, limit=limit
        )
        if branches.data:
            keyboard = keyboards.create_choice_branches_by_geo_menu(data=branches.data)
            return "Выберите магазин/склад", keyboard
        else:
            return "Не удалось найти магазины/склад по геолокации", None

    async def update_client_location(
            self,
            branch_id: int,
            state: Optional[FSMContext] = None
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Обновляем локацию клиента
        Args:
            branch_id: идентификатор филиала, за которым требуется закрепить клиента
            state: объект в котором хранится состояние диалога пользователя
        """
        if state:
            data = await state.get_data()
            if branch_id == -1:
                # ко вводу адреса заново
                return await self.send_branch_address_menu(
                    city_id=data["city_id"], city_name=data["city_name"], state=state
                )
            if branch_id == -2:
                # к вводу города заново
                await state.set_state(states.LocationHand.choice_city)
                return await self.send_city_name_menu(
                    district_id=data["district_id"], district_name=data["district_name"], state=state
                )

        if branch_id == 0:
            # отмена при изменении по геолокации
            keyboard = keyboards.create_main_menu_board()
            return "Главное меню", keyboard

        update = await self.web_app.update_client_location(branch_id=branch_id, user_id=self.user_id)
        if state:
            await state.clear()

        if update.data:
            return f"{keyboards.Emoji.ok} Локация изменена", None
        else:
            return "Ошибка при изменении локации", None

    async def choice_country_menu(self) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Создание меню для выбора списка стран"""
        countries = await self.web_app.get_countries(user_id=self.user_id)
        if countries.data:
            keyboard = keyboards.create_choice_countries_menu(data=countries.data)
            return "Выберите страну", keyboard
        else:
            keyboard = keyboards.create_init_geo_menu_board()
            return f"{keyboards.Emoji.warn} Не удалось получить список стран. Попробуйте заново", keyboard

    async def send_district_name_menu(
            self,
            country_id: int,
            country_name: str,
            state: FSMContext
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Этап когда выбрана страна и нужно отправить наименование
        района
        Args:
            country_id: идентификатор страны
            country_name: наименование страны
            state: объект стадии диалога, в котором хранится на каком этапе идет диалог
        """
        if country_id == 0:
            # переходим в главное меню
            keyboard = keyboards.create_main_menu_board()
            return "Главное меню", keyboard
        else:
            # устанавливаем состояние
            await state.set_state(states.LocationHand.choice_district)
            await state.update_data(country_id=country_id, country_name=country_name)
            return f"Страна: <b>{country_name}</b>\nВведите название региона (вводить полностью не обязательно)", None

    async def get_districts_by_name(
            self,
            search_name: str,
            state: FSMContext
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Обработка этапа когда пользователь ввел наименование региона
        и нужно извлечь список регионов
        Args:
            search_name: наименование региона который нужно найти
            state: объект стадии диалога, в котором хранится на каком этапе идет диалог
        """
        # извлекаем данные из state
        data = await state.get_data()
        districts = await self.web_app.get_districts_by_name(
            country_id=data["country_id"], search_name=search_name, user_id=self.user_id
        )
        if not districts.data:
            return f"{keyboards.Emoji.warn} Не удалось найти регион <b>{search_name}</b>. Попробуйте заново", None
        else:
            keyboard = keyboards.create_choice_district_menu(data=districts.data)
            return f'Страна: <b>{data["country_name"]}</b>\nВыберите регион', keyboard

    async def send_city_name_menu(
            self,
            district_id: int,
            district_name: str,
            state: FSMContext
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Этап когда выбран регион и нужно ввести наименование городе
        Args:
            district_id: идентификатор региона
            district_name: наименование региона
            state: объект стадии диалога, в котором хранится на каком этапе идет диалог
        """
        data = await state.get_data()
        if district_id == 0:
            # переход к тому, чтобы ввести наименование региона заного
            return await self.send_district_name_menu(
                country_id=data["country_id"], country_name=data["country_name"], state=state
            )
        if district_id == -1:
            # переход ко вводу страны
            await state.clear()
            return await self.choice_country_menu()
        else:
            # устанавливаем состояние
            await state.set_state(states.LocationHand.choice_city)
            await state.update_data(district_id=district_id, district_name=district_name)
            return f"Страна: <b>{data["country_name"]}</b>\nРегион: <b>{district_name}</b>\nВведите название города (вводить полностью не обязательно)", None

    async def get_city_by_name(
            self,
            search_name: str,
            state: FSMContext
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Обработка этапа когда пользователь ввел наименование города
        и нужно извлечь список городов
        Args:
            search_name: наименование города который нужно найти
            state: объект стадии диалога, в котором хранится на каком этапе идет диалог
        """
        # извлекаем данные из state
        data = await state.get_data()
        cities = await self.web_app.get_city_by_name(
            district_id=data["district_id"], search_name=search_name, user_id=self.user_id
        )
        if not cities.data:
            return f"{keyboards.Emoji.warn} Не удалось найти город <b>{search_name}</b>. Попробуйте заново", None
        else:
            keyboard = keyboards.create_choice_city_menu(data=cities.data)
            return f'Страна: <b>{data["country_name"]}</b>\nРегион: <b>{data["district_name"]}</b>\nВыберите город', keyboard

    async def send_branch_address_menu(
            self,
            city_id: int,
            city_name: str,
            state: FSMContext
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Этап когда выбран город и нужно ввести адрес
        Args:
            city_id: идентификатор города
            city_name: наименование города
            state: объект стадии диалога, в котором хранится на каком этапе идет диалог
        """
        data = await state.get_data()
        if city_id == 0:
            # переход к тому, чтобы ввести наименование города заново
            return await self.send_city_name_menu(
                district_id=data["district_id"], district_name=data["district_name"], state=state
            )
        if city_id == -1:
            # переход ко вводу региона
            await state.set_state(states.LocationHand.choice_district)
            return await self.send_district_name_menu(
                country_id=data["country_id"], country_name=data["country_name"], state=state
            )
        else:
            # устанавливаем состояние
            await state.set_state(states.LocationHand.choice_branch)
            await state.update_data(city_id=city_id, city_name=city_name)
            return f"Страна: <b>{data["country_name"]}</b>\nРегион: <b>{data["district_name"]}</b>\nГород: <b>{city_name}</b>\nВведите адрес магазина (вводить полностью не обязательно)", None

    async def get_branches_by_address(
            self,
            search_name: str,
            state: FSMContext
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Обработка этапа когда пользователь ввел адрес магазина
        и нужно вернуть ему список магазинов с похожим адресом
        Args:
            search_name: адрес введенный пользователем
            state: объект стадии диалога, в котором хранится на каком этапе идет диалог
        """
        # извлекаем данные из state
        data = await state.get_data()
        branches = await self.web_app.get_branches_by_address(
            city_id=data["city_id"], search_name=search_name, user_id=self.user_id, limit=2
        )
        if not branches.data:
            return f"{keyboards.Emoji.warn} Не удалось найти адрес <b>{search_name}</b>. Попробуйте заново", None
        else:
            keyboard = keyboards.create_choice_branches_menu(data=branches.data)
            return f'Страна: <b>{data["country_name"]}</b>\nРегион: <b>{data["district_name"]}</b>\nГород: <b>{data["city_name"]}</b>\nВыберите адрес', keyboard


class ClientItems(ClientLogic):
    """Логический объект работы с данными товаров и их расположением на полках"""

    async def get_items_by_name(
            self,
            search_name: str,
            state: FSMContext,
            many: bool = False
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Обработка этапа когда нужно по названию товара
        извлечь их список чтобы пользователь выбрал среди них
        Args:
            search_name: наименование товара который нужно найти
            state: объект, который хранит состояние диалога
            many: обработка ситуации, когда отрабатывает логика добавления списка товаров
        """
        items = await self.web_app.get_items_by_name(
            search_name=search_name,
            user_id=self.user_id,
            limit=3,
            similarity_threshold=0.1
        )
        if items.data:
            keyboard = keyboards.create_choice_items_meny(data=items.data, many=many)
            return "Выберите товар", keyboard
        else:
            return f"Не удалось найти товары с похожим наименованием <b>{search_name}</b>. Введите другое наименование", None

    async def get_scheme(
            self,
            state: FSMContext,
            many: bool = False,
            item_id: Optional[int] = None,
    ):
        """Обработка ситуации когда нужно по списку товаров
        вернуть схему где какой товар расположен
        Args:
            item_id: идентификатор товара
            many: флаг нужно искать много товаров или или нет
            state: объект хранящий состояние диалога
        """
        if many:
            items_data = await state.get_data()
            items_list = items_data.get("items_list")
            items_ids = [item["id"] for item in items_list]
        else:
            items_ids = [item_id]
        await state.clear()
        # извлекаем список ячеек
        spots_data = await self.web_app.get_spots_by_items(
            items_ids=items_ids,
            user_id=self.user_id
        )
        # загружаем схему с пометками
        image = await self.web_app.download_scheme(url=spots_data.data.download_url)

        return self.get_captions_list(data=spots_data.data.spots_data), BufferedInputFile(image.getvalue(), filename="scheme.jpg")

    def get_captions_list(self, data: List[schemas.SpotsWithShelvesSchem]) -> List[str]:
        """Формируем комментарии с описание в ячейке под каким номером располагается
        тот или иной товар. У телеграмма есть ограничение (не более 1024 символов)
        Args:
            data: список ячеек в расположенных на них товарах
        """
        item_id: int = 0 # ID товара чтобы пронумеровать правильно
        index_now: int = 1
        tmp_list = list()
        for spot in data:
            if spot.item_data.id == item_id:
                continue
            else:
                item_id = spot.item_data.id
                tmp_list.append(f"{index_now}) {spot.item_data.name}")
                index_now += 1
        return self.chunk_strings(strings=tmp_list, max_length=1024)

    @staticmethod
    def chunk_strings(strings: List[str], max_length=1024) -> List[str]:
        """Формируем список строк длиной не более max_length символов
        Args:
            strings: исходный список строк
            max_length: максимальная длина текста на которую требуется разбить символы
        """
        one_chunk = ""
        res_list = list()
        for string in strings:
            if (len(one_chunk) + len(string)) > max_length:
                res_list.append(one_chunk)
                one_chunk = f"{string}\n"
            else:
                one_chunk += f"{string}\n"
        res_list.append(one_chunk)
        return res_list

    async def add_item_in_list_menu(
            self,
            item_id: int,
            item_name: str,
            state: FSMContext
    ) -> Tuple[Optional[str], Optional[InlineKeyboardMarkup]]:
        """Обработка ситуации когда пользователь выбрал конкретный товар
        и нужно добавить его в список и спросить, нужно ли добавить что-то
        еще или отобразить схему
        Args:
            item_id: идентификатор товара
            item_name: наименование товара
            state: объект хранящий состояние диалога
        """
        state_data = await state.get_data()
        items_list: list = state_data.get("items_list")
        if not items_list:
            items_list = [{"id": item_id, "name": item_name}]
        else:
            items_list.append({"id": item_id, "name": item_name})
        await state.update_data(items_list=items_list)
        keyboard = keyboards.create_many_items_choice()
        text = "\n".join([f"{i + 1}){item["name"]}" for i, item in enumerate(items_list)])
        return text, keyboard



if __name__ == '__main__':
    import asyncio
    obj = ClientItems(1, "2")

    l = ["1", "2", "3", "4", "5"]

    print(obj.chunk_strings(strings=l, max_length=3))

