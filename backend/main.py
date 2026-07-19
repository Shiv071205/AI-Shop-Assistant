from fastapi import FastAPI
from backend.routes import chat, products
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="ShopAssistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(products.router)
