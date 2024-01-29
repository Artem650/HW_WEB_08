from bson import json_util
import certifi
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

connect(db="HW_Web_8",
        host=f"mongodb+srv://web_dz08:15061992@artem.z75si5r.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)