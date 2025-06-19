from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from logic import ClientLogic, ClientGeolocation, ClientItems
from keyboards import BranchCallback, LocationCallback, ItemCallback, Emoji
import states

router = Router()


@router.message(Command("menu"))
async def start_menu(message: types.Message, state: FSMContext):
    # создаем экземпляр объекта с бизнес логикой
    logic_obj = ClientLogic(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    await state.clear()
    text, keyboard = await logic_obj.get_main_menu_data()
    if text:
        await message.answer(text=text, reply_markup=keyboard)


@router.message(Command("info"))
async def start_info(message: types.Message):
    """Обрабатывает ивент, когда нужно переслать
    пользователю информацию о том как с данным ботом
    взаимодействовать и что он умеет
    """
    text = (f'Данный бот предназначен для поиска товаров'
            f' на полках магазина/склада.\n\n'
            f'{Emoji.blue}Кнопка [<u><b>Найти один товар</b></u>] позволит найти 1 какой-то товар на полках. '
            f'Введите наименование товара <i>({Emoji.warn} вводить полностью не нужно)</i> и вам будет предложено '
            f'не более 10 наиболее похожих по названию товаров от того, что вы написали. '
            f'После выбора конкретного товара вам вернется схема с точкой, где данный товар расположен\n\n'
            f'{Emoji.blue}Кнопка [<u><b>Найти список товаров</b></u>] выполняет то же самое, только по '
            f'списку товаров + построит кротчайший маршрут\n\n'
            f'{Emoji.blue}Кнопка [<u><b>Выбрать магазин</b></u>] позволяет сменить магазин/склад в котором '
            f'необходимо производить поиск. Выбрать магазин можно по геолокации <i>({Emoji.warn} будут предложены 3 ближайших адреса '
            f'относительно вашей геолокации)</i> или можно выбрать вручную')
    await message.answer(text)


@router.message(Command("support"))
async def support_info(message: types.Message):
    """Перенаправление на техническую поддержку"""
    await message.answer(
        f"Напишите в <a href='https://t.me/Udalovps'>техподдержку</a> если есть вопросы!",
        disable_web_page_preview=True
    )


@router.callback_query(lambda c: c.data == "main_menu")
async def open_main_menu(callback: types.CallbackQuery):
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    text, keyboard = await logic_obj.get_main_menu_data()
    if text:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data == "choice_branch")
async def handle_test_button(callback: types.CallbackQuery):
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    text, keyboard = await logic_obj.get_init_geo_menu()
    if text:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data == "location_geo")
async def start_location_geo(callback: types.CallbackQuery):
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    text, keyboard = await logic_obj.get_send_geo_menu()
    if text:
        await callback.message.delete()
        await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.answer()


@router.message(F.location)
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    logic_obj = ClientGeolocation(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    await message.answer(
        text=f"{Emoji.clock} Обрабатываю геолокацию", reply_markup=types.ReplyKeyboardRemove()
    )

    text, keyboard = await logic_obj.get_branches_by_geo(
        latitude=lat, longitude=lon, limit=3
    )
    if text:
        await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(BranchCallback.filter(F.action == "update_branch"))
async def handle_branch_selection(
    callback: types.CallbackQuery,
    callback_data: BranchCallback  # Автоматически парсится в объект
):
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    text, keyboard = await logic_obj.update_client_location(branch_id=callback_data.id)
    if text:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        if "изменена" in text:
            text, keyboard = await logic_obj.get_main_menu_data()
            await callback.message.answer(text=text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "location_hand")
async def start_location_hand(callback: types.CallbackQuery, state: FSMContext):
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    text, keyboard = await logic_obj.choice_country_menu()
    if text:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(LocationCallback.filter(F.action == "choice_country"))
async def send_district_name(
    callback: types.CallbackQuery,
    callback_data: LocationCallback,
    state: FSMContext
):
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    # ищем наименование страны которая была выбрана
    for row in callback.message.reply_markup.inline_keyboard:
        if row[0].callback_data == callback.data:
            country_name = row[0].text
    text, keyboard = await logic_obj.send_district_name_menu(
        country_id=callback_data.id, country_name=country_name, state=state
    )
    if text:
        message = await callback.message.edit_text(text=text, reply_markup=keyboard)
        await state.update_data(last_message_id = message.message_id)
    else:
        await callback.message.delete()


@router.message(StateFilter(states.LocationHand.choice_district))
async def get_districts_for_choice(
        message: types.Message,
        state: FSMContext,
        bot: Bot
):
    """Обработка ивента когда пользователь прислал
    наименование региона, и нужно вернуть ему список регионов
    """
    logic_obj = ClientGeolocation(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    text, keyboard = await logic_obj.get_districts_by_name(
        search_name=message.text, state=state
    )
    if text:
        storage_data = await state.get_data()
        last_message_id = storage_data.get("last_message_id")
        if last_message_id:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.chat.id, message_id=last_message_id, text=text, reply_markup=keyboard
            )
        else:
            await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(LocationCallback.filter(F.action == "choice_district"))
async def send_city_name(
    callback: types.CallbackQuery,
    callback_data: LocationCallback,
    state: FSMContext
):
    """Обработка ивента, когда пользователь нажал на кнопку и выбрал
    регион. Теперь ему нужно ввести наименование города
    """
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    # ищем наименование региона которая была выбрана
    for row in callback.message.reply_markup.inline_keyboard:
        if row[0].callback_data == callback.data:
            district_name = row[0].text

    text, keyboard = await logic_obj.send_city_name_menu(
        district_id=callback_data.id, district_name=district_name, state=state
    )
    if text:
        message = await callback.message.edit_text(text=text, reply_markup=keyboard)
        await state.update_data(last_message_id=message.message_id)
    else:
        await callback.message.delete()


@router.message(StateFilter(states.LocationHand.choice_city))
async def get_districts_for_choice(
        message: types.Message,
        state: FSMContext,
        bot: Bot
):
    """Обработка ивента когда пользователь прислал
    наименование города и нужно вернуть список городов
    """
    logic_obj = ClientGeolocation(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    text, keyboard = await logic_obj.get_city_by_name(
        search_name=message.text, state=state
    )
    if text:
        storage_data = await state.get_data()
        last_message_id = storage_data.get("last_message_id")
        if last_message_id:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.chat.id, message_id=last_message_id, text=text, reply_markup=keyboard
            )
        else:
            await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(LocationCallback.filter(F.action == "choice_city"))
async def send_branch_address_name(
    callback: types.CallbackQuery,
    callback_data: LocationCallback,
    state: FSMContext
):
    """Обработка ивента, когда пользователь нажал на кнопку и выбрал
    город. Отправляем запрос на введение адреса магазина
    """
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    # ищем наименование города которая была выбрана
    for row in callback.message.reply_markup.inline_keyboard:
        if row[0].callback_data == callback.data:
            city_name = row[0].text

    text, _ = await logic_obj.send_branch_address_menu(
        city_id=callback_data.id, city_name=city_name, state=state
    )
    if text:
        message = await callback.message.edit_text(text=text, reply_markup=None)
        await state.update_data(last_message_id=message.message_id)
    else:
        await callback.message.delete()


@router.message(StateFilter(states.LocationHand.choice_branch))
async def get_branches_for_choice(
        message: types.Message,
        state: FSMContext,
        bot: Bot
):
    """Обработка ивента когда пользователь прислал
    адрес магазина и нужно прислать ему список магазинов
    с похожими адресами чтобы он выбрал
    """
    logic_obj = ClientGeolocation(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    text, keyboard = await logic_obj.get_branches_by_address(
        search_name=message.text, state=state
    )
    if text:
        storage_data = await state.get_data()
        last_message_id = storage_data.get("last_message_id")
        if last_message_id:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.chat.id, message_id=last_message_id, text=text, reply_markup=keyboard
            )
        else:
            await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(LocationCallback.filter(F.action == "choice_branch"))
async def update_user_location_by_hand(
    callback: types.CallbackQuery,
    callback_data: BranchCallback,
    state: FSMContext
):
    """Ивент когда пользователь выбрал магазин и нужно изменить его локацию"""
    logic_obj = ClientGeolocation(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    text, keyboard = await logic_obj.update_client_location(branch_id=callback_data.id, state=state)
    if text:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        if "изменена" in text:
            text, keyboard = await logic_obj.get_main_menu_data()
            await callback.message.answer(text=text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "find_one")
async def start_one_item_logic(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Обрабатываем ивент, когда пользователь нажал на кнопку для
    того чтобы найти 1 товар на полках в магазине
    """
    await state.set_state(states.ItemsState.choice_one_item)
    message = await callback.message.edit_text(text="Введите наименование товара (не нужно вводить полностью)")
    await state.update_data(last_message_id=message.message_id)
    await callback.answer()


@router.message(StateFilter(states.ItemsState.choice_one_item))
async def get_items_by_name(
        message: types.Message,
        state: FSMContext,
        bot: Bot
):
    """Обработка ивента когда пользователь ввел наименование товара
    и нужно вернуть список наиболее похожих товаров
    """
    logic_obj = ClientItems(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    text, keyboard = await logic_obj.get_items_by_name(
        search_name=message.text, state=state
    )
    data = await state.get_data()
    last_message_id = data.get("last_message_id")
    if text:
        if last_message_id:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.chat.id, message_id=last_message_id, text=text, reply_markup=keyboard
            )
        else:
            await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(ItemCallback.filter(F.action == "one_item"))
async def get_one_item_schemas(
    callback: types.CallbackQuery,
    callback_data: BranchCallback,
    state: FSMContext
):
    """Ивент когда пользователь выбрал 1 товар и нужно отправить ему
    схему в какой ячейке данный товар находится
    """
    logic_obj = ClientItems(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    text_list, image = await logic_obj.get_scheme(item_id=callback_data.id, state=state)
    await callback.message.answer_photo(photo=image, caption=text_list.pop(0))
    if text_list:
        for text in text_list:
            await callback.message.answer(text)
    await callback.message.delete()
    await callback.answer()


@router.callback_query(lambda c: c.data == "find_many")
async def start_find_many_spots(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Ивент когда пользователь собирается добавить целый список товаров"""
    await state.set_state(states.ItemsState.choice_many_items)
    message = await callback.message.edit_text(text="Введите наименование товара (не нужно вводить полностью)")
    await state.update_data(last_message_id=message.message_id)
    await callback.answer()


@router.message(StateFilter(states.ItemsState.choice_many_items))
async def get_items_by_name(
        message: types.Message,
        state: FSMContext,
        bot: Bot
):
    """Обработка ситуации когда пользователь ввел наименование товара и нужно найти
    похожие на него по наименованию и вывести в список
    """
    logic_obj = ClientItems(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    text, keyboard = await logic_obj.get_items_by_name(
        search_name=message.text, state=state, many=True
    )
    data = await state.get_data()
    last_message_id = data.get("last_message_id")
    if text:
        await message.delete()
        # await message.answer(text=text, reply_markup=keyboard)
        await bot.edit_message_text(
            chat_id=message.chat.id, message_id=last_message_id, text=text, reply_markup=keyboard
        )


@router.callback_query(ItemCallback.filter(F.action == "many_item"))
async def get_one_item_schemas(
    callback: types.CallbackQuery,
    callback_data: BranchCallback,
    state: FSMContext
):
    """Ивент когда пользователь выбрал конкретный товар.
    Его нужно добавить в state и спросить нужно ли еще добавить товар или отобразить
    на схеме то что есть
    """
    logic_obj = ClientItems(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                item_name = button.text

    text, keyboard = await logic_obj.add_item_in_list_menu(
        item_id=callback_data.id, item_name=item_name, state=state
    )
    if text:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.message.delete()
    await callback.answer()


@router.callback_query(ItemCallback.filter(F.action == "many_choice"))
async def get_scheme_for_many_items(
    callback: types.CallbackQuery,
    callback_data: BranchCallback,
    state: FSMContext
):
    """Ивент когда пользователь собрал список товаров и хочет
    сразу весь список товаров найти на полках
    """
    logic_obj = ClientItems(
        user_id=callback.from_user.id,
        name=callback.from_user.first_name,
        username=callback.from_user.username,
    )
    #! Не забыть обработать ситуацию, когда мы ОТМЕНЯЕМ ПОИСК
    text_list, image = await logic_obj.get_scheme(item_id=callback_data.id, state=state, many=True)
    await callback.message.answer_photo(photo=image, caption=text_list.pop(0))
    if text_list:
        for text in text_list:
            await callback.message.answer(text)
    await callback.message.delete()
    await callback.answer()


@router.message(F.text)
async def init_bot(message: types.Message):
    """Роутер который первым встречает пользователя"""
    text = ("Данный бот предназначен для поиска товаров на полках магазина/склада\n"
            "/menu - для открытие главного меню\n"
            "/info - для получения информации о том, что данный бот умеет и как с ним работать\n"
            "/support - связь с технической поддержкой")
    await message.answer(text)