import pika
import json
import certifi
from mongoengine import connect
from producer import Contact

connect(db="HW_Web_8",
        host=f"mongodb+srv://web_dz08:15061992@artem.z75si5r.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='send_message')


def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    message_dict = json.loads(message)
    contact_id = message_dict['contact_id']

    # Знайдення контакту за ObjectID
    contact = Contact.objects(id=contact_id).first()

    if contact:

        contact.message_sent = True
        contact.save()
        print(f"Contact '{contact.full_name}' message status updated to 'sent'.")
    else:
        print(f"Contact with ID '{contact_id}' not found.")


channel.basic_consume(queue='send_message', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()