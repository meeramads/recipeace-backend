from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('users.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    image = CharField ()
    
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe= True)
    print("TABLES Created")
    DATABASE.close()