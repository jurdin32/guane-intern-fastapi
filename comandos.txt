#flower:

celery flower -A celery_worker.celery --broker:amqp://localhost//


#celery:

celery f-A celery_worker.celery worker --loglevel=info


#app:

uvicorn main:app --reload
