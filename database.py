import aiosqlite

DB_NAME = "shop.db"

async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            name TEXT,
            price INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            product_name TEXT,
            price INTEGER,
            status TEXT
        )
        """)

        await db.commit()

async def add_product(category, name, price):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO products(category,name,price) VALUES(?,?,?)",
            (category, name, price)
        )
        await db.commit()


async def get_products(category):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id,name,price FROM products WHERE category=?",
            (category,)
        )
        return await cursor.fetchall()

async def delete_product(product_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "DELETE FROM products WHERE id=?",
            (product_id,)
        )
        await db.commit()
