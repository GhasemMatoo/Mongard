import pika

credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
chanel_1 = connection.channel()


chanel_1.exchange_declare(exchange="second", exchange_type="fanout")
chanel_1.queue_declare(queue="test")
chanel_1.queue_bind(queue="test", exchange="second")


def callback(ch, method, properties, body):
    print(f'Received {body}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


chanel_1.basic_consume(queue="test", on_message_callback=callback)
print('Waiting for receiving message, to exit press ctrl+c')

chanel_1.start_consuming()
