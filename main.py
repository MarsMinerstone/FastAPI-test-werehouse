from fastapi import FastAPI
from router import router

###
from password_alg import verify_password, get_password_hash

###


app = FastAPI()

app.include_router(router)