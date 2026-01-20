import scrapy


class CastoreSpiderSpider(scrapy.Spider):
    name = "castore_spider"
    allowed_domains = ["castore.uz"]

    # Базовый URL. Мы добавим к нему параметр страницы
    base_url = "https://castore.uz/smartfony-i-gadzhety/?PAGEN_1="
    current_page = 1

    def start_requests(self):
        # Количество страниц, которые мы хотим собрать одновременно
        # На castore в смартфонах обычно около 30-40 страниц
        total_pages = 50

        for page in range(1, total_pages + 1):
            url = f"{self.base_url}{page}"
            self.logger.info(f"Запланирован запрос для страницы: {url}")

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                # Устанавливаем высокий приоритет, чтобы Scrapy не отвлекался
                priority=total_pages - page,
                # Это поможет избежать дубликатов, если сайт странно редиректит
                dont_filter=False
            )

    def parse(self, response):
        # Проверяем, не пустая ли страница пришла
        products = response.css('div.product_slider-card')

        if not products:
            self.logger.warning(f"Страница {response.url} пуста. Возможно, товаров больше нет.")
            return

        for product in products:
            name = product.css('.product_slider-name::text').get()
            link = product.css('.product_slider-name::attr(href)').get()
            price_raw = product.css('.row_price .price span::text').get()

            if name and price_raw:
                clean_price = float(''.join(filter(str.isdigit, price_raw)))
                yield {
                    'name': name.strip(),
                    'price': clean_price,
                    'link': response.urljoin(link)
                }