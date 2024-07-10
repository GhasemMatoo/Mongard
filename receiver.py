import pika
from pika.exchange_type import ExchangeType
credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))

chanel_1 = connection.channel()
queue = chanel_1.queue_declare(queue="request-queue")

def callback(ch, method, properties, body):
    print(f'Received {properties.correlation_id}')
    ch.basic_publish(exchange="", routing_key=properties.reply_to, body=f'reply to {properties.correlation_id}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


chanel_1.basic_consume(queue="request-queue", on_message_callback=callback)
print('Waiting for receiving message, to exit press ctrl+c')

chanel_1.start_consuming()
