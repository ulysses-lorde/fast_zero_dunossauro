from fastapi import FastAPI

from fast_zero.routes import auth, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
def home():
    return {'message': 'Olá Mundo!'}
