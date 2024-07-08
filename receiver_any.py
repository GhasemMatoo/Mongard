import pika
from pika.exchange_type import ExchangeType
credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))

chanel_1 = connection.channel()
chanel_1.exchange_declare(exchange="test", exchange_type=ExchangeType.headers)
queue = chanel_1.queue_declare(queue='HQ-any', exclusive=True)

bind_args = {
    "x-match": "any", "name": "ghasem"
}

queue_name = queue.method.queue
chanel_1.queue_bind(exchange="test", queue=queue_name, arguments=bind_args)

def callback(ch, method, properties, body):
    print(f'booody{body}')
    print(f'method{queue}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


chanel_1.basic_consume(queue=queue_name, on_message_callback=callback)
print('Waiting for receiving message, to exit press ctrl+c')
print(f'method{queue_name}')

chanel_1.start_consuming()
