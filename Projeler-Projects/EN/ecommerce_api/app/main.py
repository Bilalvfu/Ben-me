from app.routers import auth, category, order, product
from fastapi import FastAPI

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    description="Production-ready E-Commerce REST API with FastAPI and SQLAlchemy",
)


app.include_router(category.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)

@app.get("/")
def root():
  return {"message": "Welcome to the E-Commerce API! Everything is running."}

if __name__ == "__main__":
  import uvicorn

  uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
