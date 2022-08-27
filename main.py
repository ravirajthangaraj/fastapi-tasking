from fastapi import Depends, FastAPI
import uvicorn
from app.routers import users


application = FastAPI()

application.include_router(users.router)


@application.get('/', response_model=dict)
def root():
    # TODO: add title, version and description
    return {'message': 'Welcome to FastAPI Tasking'}


"""for development and debugging"""
# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port="8000")
