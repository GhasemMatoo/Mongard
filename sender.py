import pika

credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
chanel_1 = connection.channel()

chanel_1.exchange_declare(exchange="test", exchange_type="fanout")

# properties = pika.BasicProperties(headers={"test": 'TEST'})
chanel_1.basic_publish(exchange="test", routing_key='', body="Hello world to FANOUT!")
print("Message sending")
connection.close()
