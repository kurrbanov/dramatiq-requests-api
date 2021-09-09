import aiopg
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main():
    conn = await aiopg.connect(database='drama',
                               user='drama_user',
                               password='pass',
                               host='db', port=5432)
    cur = await conn.cursor()
    await cur.execute("SELECT * FROM responses;")
    result = await cur.fetchone()
    await conn.close()

    return {result[1]: result[2]}
