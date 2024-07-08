import pika

credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))

chanel_1 = connection.channel()
chanel_1.exchange_declare(exchange="test", exchange_type="fanout")
queue = chanel_1.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue
chanel_1.queue_bind(exchange="test", queue=queue_name)


def callback(ch, method, properties, body):
    print(f'booody{body}')
    print(f'method{queue}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


chanel_1.basic_qos(prefetch_count=1)
chanel_1.basic_consume(queue=queue_name, on_message_callback=callback)
print('Waiting for receiving message, to exit press ctrl+c')
print(f'method{queue_name}')
if input() == 'exit':
    chanel_1.stop_consuming()

chanel_1.start_consuming()
