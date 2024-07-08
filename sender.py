import pika

credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
chanel_1 = connection.channel()

chanel_1.exchange_declare(exchange="test", exchange_type="topic")

messages = {
    'error.warning.important': 'This is an important message',
    'info.debug.notimportant': 'This is not an important message'
}

for k, v in messages.items():
    chanel_1.basic_publish(exchange="test", routing_key=k, body=v)
print("Message sending")
connection.close()
