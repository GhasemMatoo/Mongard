import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
chanel_1 = connection.channel()
chanel_1.queue_declare(queue="one")


def callback(ch, method, properties, body):
    print(f'booody{body}')


chanel_1.basic_consume(queue="one", on_message_callback=callback, auto_ack=True)
print('Waiting for receiving message, to exit press ctrl+c')

if input() == 'exit':
    chanel_1.stop_consuming()

chanel_1.start_consuming()
