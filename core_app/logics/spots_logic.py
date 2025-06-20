"""logics/spots_logic
Логические объекты для поиска местоположения товаров на полках
"""
import logging
from typing import List, Optional, Union
import secrets

import config
# импортируем логические объекты
from logics.base_logic import BaseLogic
from logics.painter import Painter, Shelf, Branch
from PIL import Image

# импортируем глобальные объекты
from schemas.base_schemas import BaseResultSchem
import schemas.storage_schem.items_schem
from schemas import storage_schem, logic_schem
import exceptions
from exception_handler import handle_view_exception


logger = logging.getLogger(__name__)


class SpotLogic(BaseLogic):
    """Объект с методами для нахождения местоположения товаров на полках"""

    async def use_get_product_data_by_name(
            self,
            search_name: str,
            token: str,
            api: str,
            limit: int = 3,
            similarity_threshold: float = 0.1,
            frontend_id: Optional[int] = None,
            frontend_service_id: Optional[int] = None,
            branch_id: Optional[int] = None

    ) -> BaseResultSchem[List[schemas.storage_schem.items_schem.SimilarItemsSchem]]:
        """НАВИГАЦИОННЫЙ МЕТОД поиска данных по товару по его имени.
        - Проходим аутентификацию по токену
        - находим данные клиента в зависимости от типа фронтенд приложения
        - проверяем в БД есть ли данные товары в нужном помещении и возвращаем результат
        Args:
            frontend_id: идентификатор клиента из frontend сервиса который обращается к API
            frontend_service_id: тип frontend сервиса который взаимодействует с системой
            search_name: наименование товара который нужно найти
            token: токен аутентификации
            api: раздел в котором происходит действие
            limit: кол-во записей который нужно извлечь
            similarity_threshold: степень похожести
            branch_id: идентификатор помещения в котором необходимо найти товары
        return:
            BaseResultSchem(
                error: Optional[BaseErrorSchem] - данные об ошибке, если она произошла
                data: Any = данные которые должна вернуть API
            )
        """
        try:
            logger.info(f"Обрабатываю логику поиска товара по имени. frontend_id: {frontend_id}, "
                        f"frontend_service_id: {frontend_service_id}, search_name: {search_name}")

            # аутентификация
            await self.check_authenticate(token=token, api=api)

            # валидация данных
            if not branch_id and (not frontend_id or not frontend_service_id):
                raise exceptions.ValidationError(api=api, detail="branch_id and frontend_data cannot be empty")

            if not branch_id:
                # поиск данных филиала
                branch_id = await self.get_branch_id_by_client_data(
                    frontend_id=frontend_id,
                    frontend_service_id=frontend_service_id,
                    api=api
                )

            # проверяем есть ли в помещении в котором находится пользователь данные товары
            items_data = await self.items_obj.get_similar_items(
                branch_id=branch_id,
                search_name=search_name,
                count=limit,
                sim_threshold=similarity_threshold,
                organization_id=self.ORGANIZATION_ID
            )
            if not items_data:
                # ошибка если по данному имени не найден товар
                raise exceptions.NotFoundError(item_name="items_data", api=api)

            return BaseResultSchem[List[schemas.storage_schem.items_schem.SimilarItemsSchem]](data=items_data)
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def get_spots_schem(
            self,
            items_ids: List[int],
            token: str,
            api: str,
            branch_id: Optional[int] = None,
            frontend_id: Optional[int] = None,
            frontend_service_id: Optional[int] = None,
            route: bool = False
    ):
        """НАВИГАЦИОННЫЙ МЕТОД
        Поиск ячеек на полках помещения списка товаров и отметка на схеме (изображении)
        помещения где конкретно находится тот или иной товар
        - Проходим аутентификацию по токену
        - Находим branch_id если он не передан в аргументах
        - Извлекаем список ячеек в которых расположены товары + информацию о полках
            на которых они лежат + информация о товарах
        - Извлекаем схему помещения
        - Если передан список разных товаров, то производим построение оптимального маршрута
        - Отмечаем расположение ячеек на схемах
        - Возвращаем полученный результат
        Args:
            frontend_id: идентификатор клиента во frontend системе
            frontend_service_id: идентификатор frontend сервиса от которого исходит запрос
            items_ids: список идентификаторов товаров которые нужно найти
            token: токен аутентификации
            api: раздел API в котором происходит логика
            branch_id: идентификатор филиала в котором нужно искать данные товары
            route: флаг который говорит о том, нужно ли из точек стоить оптимальный маршрут
                или нет
        """
        try:
            logger.info(f"Пришла задача по поиску расположения расположения товаров на полках."
                        f"frontend_id: {frontend_id}, frontend_service_id: {frontend_service_id}, "
                        f"items_ids: {items_ids}, branch_id: {branch_id}")

            # аутентификация
            await self.check_authenticate(token=token, api=api)

            # валидация данных
            if not branch_id and (not frontend_id or not frontend_service_id):
                raise exceptions.ValidationError(api=api, detail="branch_id and frontend_data cannot be empty")

            # поиск данных филиала
            if not branch_id:
                branch_id = await self.get_branch_id_by_client_data(
                    frontend_id=frontend_id,
                    frontend_service_id=frontend_service_id,
                    api=api
                )

            # поиск ячеек на которых расположены товары
            spots_data = await self.spots_obj.get_data_by_item_and_organization(
                items_ids=items_ids, org_id=self.ORGANIZATION_ID, branch_id=branch_id
            )
            if not spots_data:
                raise exceptions.NotFoundError(item_name="spots_data", api=api)

            # извлекаем из хранилища схему помещения
            branch_schem_data = await self.branch_schemas_obj.get_data_by_branch_id(branch_id=branch_id)
            if not branch_schem_data:
                raise exceptions.NotFoundError(item_name="branch_schem_data", api=api)

            # вычисляем координаты расположения ячеек на общей схеме помещения
            for spot in spots_data:
                x, y = Shelf(
                    x1=spot.shelf_data.x1,
                    y1=spot.shelf_data.y1,
                    x2=spot.shelf_data.x2,
                    y2=spot.shelf_data.y2,
                    cell_count=spot.shelf_data.cell_count,
                    floor_count=spot.shelf_data.floor_count
                ).find_coord(cell_index=spot.cell_number)
                spot.x_spot_coord = x
                spot.y_spot_coord = y

            if route and len(spots_data) > 2:   # логика построения оптимального маршрута
                # вычисляем координаты расположения ячеек на общей схеме помещения
                spots_data = self.create_optimal_route(spots_data=spots_data, branch_data=branch_schem_data)

            # сохраняем данные в КЭШ чтобы потом по ним скачать изображение
            key = str(secrets.token_hex(32))

            result = logic_schem.spot_schem.SpotResultSchem(
                spots_data=spots_data,
                download_url=f"{config.API_URL}/api/client/download/{key}"
            )

            await self.cache_obj.set_data_in_cache(key=key, value=result, live_time=60)

            return BaseResultSchem[logic_schem.spot_schem.SpotResultSchem](data=result)

        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    async def download_schem(
            self,
            download_key: str,
            token: str,
            api: str,
    ) -> Union[Image, BaseResultSchem]:
        """Отмечаем на изображении координаты ячеек и возвращаем изображение обратно на запрос
        Args:
            download_key: ключ для скачивания файла
            token: токен аутентификации
            api: раздел API в котором происходит логика
        """
        try:
            logger.info(f"Выполнение задания по скачиванию файла с отмеченными ячейками - {download_key}")

            # аутентификация
            await self.check_authenticate(token=token, api=api)

            # извлекаем данные из КЭШа по ключу
            data: logic_schem.spot_schem.SpotResultSchem = await self.cache_obj.get_data_from_cache(
                key=download_key, data_class=logic_schem.spot_schem.SpotResultSchem
            )
            if not data:
                raise exceptions.DownloadKeyError(key=download_key, api=api)

            branch_schem_data = await self.branch_schemas_obj.get_data_by_branch_id(branch_id=data.spots_data[0].shelf_data.branch_id)
            if not branch_schem_data:
                raise exceptions.NotFoundError(item_name="branch_schem_data", api=api)

            # # отмечаем расположение ячеек на изображении
            item_id = 0
            count = 0
            painter = Painter(image_path=branch_schem_data.content.url)
            for spot in data.spots_data:
                if spot.item_data.id != item_id:
                    item_id = spot.item_data.id
                    count += 1
                painter.add_point(x=spot.x_spot_coord, y=spot.y_spot_coord, label=str(count))

            # painter.save_image("./out.jpg")

            return painter.image
        except Exception as _er:
            return handle_view_exception(ex=_er, api=api)

    def create_optimal_route(
            self,
            spots_data: List[storage_schem.spots_schem.SpotsWithShelvesSchem],
            branch_data: storage_schem.branches_schem.BranchPlanSchemaBase
    ):
        """Вычисляем оптимальный маршрут для посещения всех точек
        в помещении с максимально короткой дистанцией
        - вычисляем координаты ячеек которые нужно посетить
        - убираем лишние точки (если один и тот же товар повторяется на разных полках_
        - простраиваем оптимальный маршрут чтобы получить максимально короткую дистацию
        Args:
            spots_data: список точек которые нужно посетить
            branch_data: данные филиала вместе с его схемой
        """
        logger.info(f"Логика простраивания оптимального маршрута")

        # создаем объект помещения филиала. Для вычисления дальнейшей логики
        branch_obj = Branch(exit_x=branch_data.exit_x, exit_y=branch_data.exit_y)

        # убираем дубли
        spots_data = self.delete_double_spots(branch_obj=branch_obj, spots_data=spots_data)

        # простраиваем маршрут
        return self.calc_optimal_route(branch_obj=branch_obj, spots_data=spots_data)

    @staticmethod
    def calc_optimal_route(
            branch_obj: Branch,
            spots_data: List[storage_schem.spots_schem.SpotsWithShelvesSchem]
    ) -> List[storage_schem.spots_schem.SpotsWithShelvesSchem]:
        """Вычисление оптимального маршрута
        - по ближайшим соседям
        - доп оптимизация
        Args:
            branch_obj: объект помещения в котором будет вычисляться дальнейшая логика
            spots_data: список ячеек которые нужно посетить
        """
        # вычисляем оптимальный маршрут
        nearest_neighbor = branch_obj.nearest_neighbor(points=spots_data)
        return branch_obj.two_opt(path=nearest_neighbor)

    @staticmethod
    def delete_double_spots(
            branch_obj: Branch,
            spots_data: List[storage_schem.spots_schem.SpotsWithShelvesSchem]
    ) -> List[storage_schem.spots_schem.SpotsWithShelvesSchem]:
        """Проверяем наличие дудлирующих товаров в разных ячейках.
        Вернет список без дублей
        Args:
            branch_obj: объект помещения в котором будет вычисляться дальнейшая логика
            spots_data: список ячеек которые нужно посетить
        """
        center_x, center_y = branch_obj.get_centroid(spots_list=spots_data)
        tmp_distance_dict = dict()
        for index, spot in enumerate(spots_data):
            # вычисляем расстояние от точки до центроида
            tmp_distance = branch_obj.distance_between_points(x1=center_x, y1=center_y, x2=spot.x_spot_coord,
                                                              y2=spot.y_spot_coord)
            if spot.item_data.id not in tmp_distance_dict:
                tmp_distance_dict[spot.item_data.id] = {"min_value": tmp_distance, "index": index}
            else:
                if tmp_distance_dict[spot.item_data.id]["min_value"] > tmp_distance:
                    tmp_distance_dict[spot.item_data.id]["min_value"] = tmp_distance
                    tmp_distance_dict[spot.item_data.id]["index"] = index

        # оставляем в списке только те ближние к центроиду точки
        res_spot_list = list()
        for value in tmp_distance_dict.values():
            res_spot_list.append(spots_data[value["index"]])

        return res_spot_list

    async def get_branch_id_by_client_data(self, frontend_id: int, frontend_service_id: int, api: str) -> int:
        """Поиск данных филиала с которым связаны запросы клиента по
        идентификатору клиента из frontend приложения и идентификатору
        frontend сервиса
        Args:
            frontend_id: идентификатор клиента во frontend приложении
            frontend_service_id: идентификатор frontend сервиса
            api: раздел API в котором происходит взаимодействие
        """
        # получаем данные клиента
        client_data = await self.client_obj.get_data_by_frontend_id(
            frontend_id=frontend_id, frontend_service_id=frontend_service_id, organization_id=self.ORGANIZATION_ID
        )
        logger.info(f"Получены данные клиента: {client_data}")
        if not client_data:
            # если не найдены данные клиента то вызываем ошибку
            raise exceptions.NotFoundError(item_name="client_data", api=api)
        if not client_data.location:
            # если у клиента нет локации на которой он находится
            raise exceptions.NotFoundError(item_name="client_location", api=api)
        return client_data.location.branch_id
