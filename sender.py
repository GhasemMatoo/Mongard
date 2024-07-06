import pika

credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
chanel_1 = connection.channel()

chanel_1.queue_declare(queue="one")

properties = pika.BasicProperties(headers={"test": 'TEST'})
chanel_1.basic_publish(exchange="", routing_key="one", body="Hello world...!", properties=properties)
print("Message sending")
chanel_1.close()
