import uvicorn
from fastapi import FastAPI

from src.secret.router import router as router_secret

app = FastAPI(title="APIsecret")

""" Роутер для secret"""
app.include_router(router_secret)











if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)