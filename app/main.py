import fastapi as fastApi
from app.routers.expenses import router as expenses_router

app = fastApi.FastAPI(
    title = "EMS",
    description = "Expense management system",
    version = "0.1.0"
)

@app.get("/")
def home():
    return{
        "message": "Expense Management System (EMS) is running"
    }

app.include_router(expenses_router)