from rapidfuzz import process


class VectorStore:
    def find_similar_products(self, query: str, products_dict: dict, limit: int = 5):
        # Получаем список названий продуктов
        product_names = products_dict.keys()

        # Ищем наиболее похожие названия
        matches = process.extract(query, product_names, limit=limit)

        result = {products_dict[match[0]]: match[0] for match in matches}

        return result


if __name__ == '__main__':
    from contextlib import contextmanager
    import time
    import baggage

    @contextmanager
    def timeit():
        start = time.perf_counter()
        yield
        end = time.perf_counter()
        print(f"Время выполнения: {end - start:.6f} секунд")

    with timeit():
        query = "мол"
        similar_products = VectorStore().find_similar_products(query, baggage.data2, limit=10)
        print(similar_products)
