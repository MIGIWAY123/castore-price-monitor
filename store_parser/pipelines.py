import requests
import os
from dotenv import load_dotenv
from .database import Session, Product, PriceHistory


class StoreParserPipeline:
    def open_spider(self, spider):
        self.session = Session()
        # Читаем данные из окружения
        self.bot_token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def close_spider(self, spider):
        self.session.close()

    def send_telegram(self, message):
        # Здесь логика остается прежней, она уже использует self.bot_token
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Ошибка отправки в TG: {e}")

    def process_item(self, item, spider):
        product = self.session.query(Product).filter_by(url=item['link']).first()

        if not product:
            product = Product(name=item['name'], url=item['link'])
            self.session.add(product)
            self.session.commit()
            # Если товар новый, просто шлем приветствие
            self.send_telegram(f"🆕 <b>Новый товар в мониторинге:</b>\n{item['name']}\nЦена: {item['price']} сум")
        else:
            # Сравниваем с последней ценой в базе
            last_price_record = self.session.query(PriceHistory).filter_by(product_id=product.id).order_by(
                PriceHistory.timestamp.desc()).first()

            if last_price_record and item['price'] < last_price_record.price:
                diff = last_price_record.price - item['price']
                msg = (f"🔥 <b>ЦЕНА УПАЛА!</b>\n"
                       f"🏷 {item['name']}\n"
                       f"📉 Скидка: {diff} сум\n"
                       f"💰 Новая цена: {item['price']} сум\n"
                       f"🔗 <a href='{item['link']}'>Купить на сайте</a>")
                self.send_telegram(msg)

        # Сохраняем новую цену в любом случае
        new_price = PriceHistory(product_id=product.id, price=item['price'])
        self.session.add(new_price)
        self.session.commit()

        return item
