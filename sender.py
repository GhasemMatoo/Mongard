import pika

credentials = pika.PlainCredentials(username="ghasem", password="Mg1368")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', credentials=credentials))
chanel_1 = connection.channel()

chanel_1.exchange_declare(exchange="first", exchange_type="direct")
chanel_1.exchange_declare(exchange="second", exchange_type="fanout")
chanel_1.exchange_bind("first", "second")

chanel_1.basic_publish(exchange="firest", routing_key="", body="hello .....!")
print("Sending Message ......")
connection.close()
