import pika
import json
from mongoengine import connect, Document, StringField, BooleanField
import certifi
from faker import Faker

fake = Faker('uk-UA')

connect(db="HW_Web_8",
        host=f"mongodb+srv://web_dz08:15061992@artem.z75si5r.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='send_message')


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
    phone = StringField()
    address = StringField(max_length=150)
    meta = {'collection': 'contacts'}


def create_task(num: int):
    for _ in range(10):
        full_name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address()

        # Save Contacts in DB
        contact = Contact(full_name=full_name, email=email, phone=phone, address=address)
        contact.save()

        # Send message to queue RabbitMQ with ObjectID to contact
        message = {'contact_id': str(contact.id)}
        channel.basic_publish(exchange='', routing_key='send_message', body=json.dumps(message))

        print(f"Contact '{full_name}' added to the queue")

    connection.close()


if __name__ == "__main__":
    create_task(6)