import pika
from pika.exchange_type import ExchangeType
credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
chanel_1 = connection.channel()

chanel_1.exchange_declare(exchange="headers", exchange_type=ExchangeType.headers)

messages = "Hello Word...!"
properties = pika.BasicProperties(headers={"name": "ghasem", "test": "ok"})
chanel_1.basic_publish(exchange="test", routing_key="", body=messages, properties=properties)
print("Message sending")
connection.close()
