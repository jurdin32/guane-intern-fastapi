import datetime
from peewee import *
database = SqliteDatabase('my_app.db')

class Dog(Model):
    name = CharField()
    picture = CharField()
    is_adopted=BooleanField()
    create_Date=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
#database.create_tables([Dog])

class User(Model):
    username=CharField()
    password=CharField()

    class Meta:
        database = database

#database.create_tables([User])
