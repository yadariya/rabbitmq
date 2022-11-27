import pika, sys, os
from time import sleep
import psycopg2


def main(db_host_, host_, port_, user_, password_):
    conn = psycopg2.connect(
        host=db_host_,
        database="postgres",
        user="postgres",
        password="postgres")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS name('
                'name VARCHAR(255))')
    cur.close()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS surname('
                'surname VARCHAR(255))')
    cur.close()
    credentials_ = pika.PlainCredentials(user_, password_)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_, port=port_, credentials=credentials_))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        if (body==b'Dariya'):
            print(" [x] Received name %r" % body)
            cur = conn.cursor()
            cur.execute('INSERT INTO name (name) values(%s)',[body])
            cur.close()
        elif (body==b'Vakhitova'):
            print(" [x] Received surname %r" % body)
            cur = conn.cursor()
            cur.execute('INSERT INTO surname (surname) values(%s)',[body])
            cur.close()

        cur = conn.cursor()
        cur.execute('SELECT (SELECT COUNT(*) FROM name) as names, (SELECT COUNT(*) FROM surname) as surnames')
        print('Count of names and surnames is', cur.fetchone())
        cur.close()

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    # sleep(10)
    db_host_ = os.environ['DB_HOST']
    print(db_host_)
    host_ = os.environ['HOST']
    print(host_)
    port_ = os.environ['PORT']
    print(port_)
    user_ = os.environ['USER']
    print(user_)
    password_ = os.environ['PASSWORD']
    print(password_)
    try:
        main(db_host_, host_, port_, user_, password_)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
