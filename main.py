from fastapi import FastAPI

app=FastAPI(title="ShopAssistant")

@app.get("/")
async def root():
    return{"message": "Welcome to the ShopAssistant!"}

def main():
    print("Hello from ShopAssistant!")


if __name__ == "__main__":
    main()
