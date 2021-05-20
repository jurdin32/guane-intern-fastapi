from time import sleep
from celery import Celery
from celery.utils.log import get_task_logger
import requests

from models import Dog, User

celery = Celery('tasks', broker='amqp://guest:guest@127.0.0.1:5672//')
celery_log = get_task_logger(__name__)

@celery.task
def createDogs(name,username):
    URL = 'https://dog.ceo/api/breeds/image/random'
    data = requests.get(URL)
    data = data.json()
    complete_time_per_item = 5
    sleep(complete_time_per_item)
    user=User.get(User.username==username)
    dog = Dog.create(
        user_id=user.id,
        name=name,
        picture=data['message'],
        is_adopted=False
    )
    dog.save()
    print("El registro se ha creado")
    return dog.get()

