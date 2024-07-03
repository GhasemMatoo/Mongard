import pika

credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
chanel_1 = connection.channel()

chanel_1.queue_declare(queue="one")

chanel_1.basic_publish(exchange="", routing_key="one", body="Hello world...!")
print("Message sending")
chanel_1.close()
