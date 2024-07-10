import pika
from pika.exchange_type import ExchangeType
from uuid import uuid4
credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
chanel_1 = connection.channel()

reply_queue = chanel_1.queue_declare(queue='', exclusive=True)


def on_reply_message_receive(ch, method, properties, body):
    print(f'reply_message_receive == {body}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

chanel_1.basic_consume(queue=reply_queue.method.queue, on_message_callback=on_reply_message_receive)

chanel_1.queue_declare(queue="request-queue")
core_id = str(uuid4())
messages = "Hello Word...!"
properties = pika.BasicProperties(reply_to=reply_queue.method.queue, correlation_id=core_id)
chanel_1.basic_publish(exchange="", routing_key="request-queue", body=messages, properties=properties)
print("Message sending")
chanel_1.start_consuming()
