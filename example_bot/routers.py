from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from logic import ClientLogic, ClientGeolocation, ClientItems
from keyboards import BranchCallback, LocationCallback, ItemCallback
import states

router = Router()


@router.message(Command("start"))
async def init_bot(message: types.Message):
    # создаем экземпляр объекта с бизнес логикой
    logic_obj = ClientLogic(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
    )
    text, keyboard = await logic_obj.get_main_menu_data()
    if text:
        await message.answer(text=text, reply_markup=keyboard)


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
        text="Обрабатываю геолокацию", reply_markup=types.ReplyKeyboardRemove()
    )

    text, keyboard = await logic_obj.get_branches_by_geo(
        latitude=lat, longitude=lon, limit=3
    )
    if text:
        await message.answer(text=text, reply_markup=keyboard)
        # await state.set_state(states.LocationGeo.choice_branch)

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
    text, _ = await logic_obj.update_client_location(branch_id=callback_data.id)
    if text:
        await callback.message.edit_text(text=text, reply_markup=None)


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
    text, _ = await logic_obj.send_district_name_menu(
        country_id=callback_data.id, country_name=callback_data.name, state=state
    )
    if text:
        await callback.message.edit_text(text=text, reply_markup=None)
    else:
        await callback.message.delete()


@router.message(StateFilter(states.LocationHand.choice_district))
async def get_districts_for_choice(
        message: types.Message,
        state: FSMContext
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
    text, _ = await logic_obj.send_city_name_menu(
        district_id=callback_data.id, district_name=callback_data.name, state=state
    )
    if text:
        await callback.message.edit_text(text=text, reply_markup=None)
    else:
        await callback.message.delete()


@router.message(StateFilter(states.LocationHand.choice_city))
async def get_districts_for_choice(
        message: types.Message,
        state: FSMContext
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
    text, _ = await logic_obj.send_branch_address_menu(
        city_id=callback_data.id, city_name=callback_data.name, state=state
    )
    if text:
        await callback.message.edit_text(text=text, reply_markup=None)
    else:
        await callback.message.delete()


@router.message(StateFilter(states.LocationHand.choice_branch))
async def get_branches_for_choice(
        message: types.Message,
        state: FSMContext
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
    text, _ = await logic_obj.update_client_location(branch_id=callback_data.id, state=state)
    if text:
        await callback.message.edit_text(text=text, reply_markup=None)


@router.callback_query(lambda c: c.data == "find_one")
async def start_one_item_logic(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """Обрабатываем ивент, когда пользователь нажал на кнопку для
    того чтобы найти 1 товар на полках в магазине
    """
    await state.set_state(states.ItemsState.choice_one_item)
    await callback.message.edit_text(text="Введите наименование товара (не нужно вводить полностью)")
    await callback.answer()


@router.message(StateFilter(states.ItemsState.choice_one_item))
async def get_items_by_name(
        message: types.Message,
        state: FSMContext
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
    if text:
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
    await callback.message.edit_text(text="Введите наименование товара (не нужно вводить полностью)")
    await callback.answer()


@router.message(StateFilter(states.ItemsState.choice_many_items))
async def get_items_by_name(
        message: types.Message,
        state: FSMContext
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
    if text:
        await message.answer(text=text, reply_markup=keyboard)


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