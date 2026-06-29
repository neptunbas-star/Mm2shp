import aiosqlite

async def init_db():
    async with aiosqlite.connect("shop.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price TEXT
            )
        """)
        await db.commit()

async def add_product(name, price):
    async with aiosqlite.connect("shop.db") as db:
        await db.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        await db.commit()

async def get_products():
    async with aiosqlite.connect("shop.db") as db:
        cursor = await db.execute("SELECT name, price FROM products")
        return await cursor.fetchall()
