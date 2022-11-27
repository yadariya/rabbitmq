import pika, os
from time import sleep

host_ = os.environ['HOST']
print(host_)
port_ = os.environ['PORT']
print(port_)
user_ = os.environ['USER']
print(user_)
password_ = os.environ['PASSWORD']
print(password_)

credentials = pika.PlainCredentials(user_, password_)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host_, port=int(port_), credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

while True:
    channel.basic_publish(exchange='', routing_key='hello', body=b'Dariya')
    channel.basic_publish(exchange='', routing_key='hello', body=b'Vakhitova')
    sleep(5)

connection.close()