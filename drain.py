import pika
import sys

q = sys.argv[1]

connection = pika.BlockingConnection(pika.ConnectionParameters(
                                host='localhost'))

channel = connection.channel()
channel.queue_declare(queue=q, durable=True)      

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=q)
channel.start_consuming()
