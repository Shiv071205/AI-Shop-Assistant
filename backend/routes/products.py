from fastapi import APIRouter
from backend.db.mysql import get_db_connection


router = APIRouter()
@router.get("/products")
def get_products():
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return {"products": products}
 