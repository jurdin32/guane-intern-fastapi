from fastapi import FastAPI, Depends, HTTPException
import requests
from auth import *
from celery_worker import createDogs
from schema import *
from models import Dog, User

app = FastAPI()
auth_handler = AuthHandler()


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if User.select().where(User.username == auth_details.username):
        raise HTTPException(status_code=400, detail='Username ya esta registrado..!')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    user = User.create(
        username=auth_details.username,
        password=hashed_password
    )
    user.save()
    return {'user': [user]}


@app.post('/login')
def login(auth_details: AuthDetails):
    password = auth_handler.get_password_hash(auth_details.password)
    if (User.select().where(User.username == auth_details.username, User.password == password)):
        raise HTTPException(status_code=401, detail='Usuario o contraseña invalida.!')
    token = auth_handler.encode_token(auth_details.username)
    return {'token': token}


# devuelve todos
@app.get("/api/dogs")
def read_all():
    listado = []
    for d in Dog.select():
        listado.append({"id": d.id, "name": d.name, "picture": d.picture, "create_date": d.create_Date,
                        "is_adopted": d.is_adopted,'user_id':d.user_id})
    return {"dogs": listado}


# todos cuya bandera is_adopted=true
@app.get("/api/dogs/is_adopted")
def list_adopted():
    listado = []
    for d in Dog.select().where(Dog.is_adopted == True):
        listado.append({"id": d.id, "name": d.name, "picture": d.picture, "create_date": d.create_Date,
                        "is_adopted": d.is_adopted,'user_id':d.user_id})
    return {"dogs": listado}


# devuelve por nombre
@app.get("/api/dogs/{name}")
def read_name(name: str):
    data = []
    try:
        d = Dog.get(Dog.name == name)
        data.append({"id": d.id, "name": d.name, "picture": d.picture, "create_date": d.create_Date,
                     "is_adopted": d.is_adopted,'user_id':d.user_id})
    except:
        raise HTTPException(status_code=401, detail='No hay mascotas con ese nombre, reintente.!')
    return {"dog": data}


#crea una nueva mascota
@app.post("/api/dogs/{name}")
def create_dogs(name: str, username=Depends(auth_handler.auth_wrapper)):
    createDogs.delay(name,username)
    return {'dog':'Creando..!'}

#actualiza la mascota
@app.put("/api/dogs/{name}")
def update_dogs(name: str, username=Depends(auth_handler.auth_wrapper)):
    URL = 'https://dog.ceo/api/breeds/image/random'
    data = requests.get(URL)
    data = data.json()
    dog = Dog.select().where(Dog.name == name).get()
    dog.name = name,
    dog.picture = data['message'],
    dog.is_adopted = True
    dog.save()
    return {'dog': [dog]}

#elimina la mascota
@app.delete("/api/dogs/{name}")
def delete_dogs(name: str, username=Depends(auth_handler.auth_wrapper)):
    Dog.delete().where(Dog.name == name).execute()
    return {"dog": "Eliminado..!"}


