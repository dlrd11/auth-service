from fastapi import FastAPI
from database import engine, Base
from routes import auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)  # This line initializes the database

app.include_router(auth_router, prefix="/auth")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
