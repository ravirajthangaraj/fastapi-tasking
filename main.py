
from fastapi import Depends, FastAPI
import uvicorn
from app.routers import users

app = FastAPI()

app.include_router(users.router)


@app.get('/')
def root():
    # TODO: add title, version and description
    return {'message': 'Welcome to FastAPI Tasking'}


"""for development and debugging"""
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port="8000")
