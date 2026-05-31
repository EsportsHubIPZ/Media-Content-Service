import pika
import json
from app.config import settings

class RabbitMQPublisher:
    def __init__(self):
        self.connection_url = settings.RABBITMQ_URL
        self.exchange = "esports.news.exchange"
        self._setup()

    def _setup(self):
        try:
            params = pika.URLParameters(self.connection_url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.exchange_declare(exchange=self.exchange, exchange_type='topic', durable=True)
            connection.close()
        except Exception as e:
            print(f"Failed to setup RabbitMQ: {e}")

    def publish_news_event(self, event_data: dict):
        try:
            params = pika.URLParameters(self.connection_url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            
            channel.basic_publish(
                exchange=self.exchange,
                routing_key="news.published",
                body=json.dumps(event_data),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            connection.close()
        except Exception as e:
            print(f"Failed to publish event: {e}")
