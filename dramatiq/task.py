import asyncio
import aiopg
import dramatiq
import json

from requests import get
from time import sleep
from dramatiq.brokers.redis import RedisBroker
from apscheduler.schedulers.blocking import BlockingScheduler

API_URL = "http://worldtimeapi.org/api/timezone/Europe/Moscow"
broker = RedisBroker(url="redis://redis:6379/0")
dramatiq.set_broker(broker)


@dramatiq.actor
def check_unix_time():
    response = json.loads(get(API_URL).text)
    unix_time = response["unixtime"]

    async def mem():
        connection_async = await aiopg.connect(database="drama", user="drama_user", password="pass", host="db")
        cur = await connection_async.cursor()
        await cur.execute("SELECT * FROM responses;")
        data = await cur.fetchone()

        await cur.execute("BEGIN;")
        if not data:
            await cur.execute("INSERT INTO responses (id, url, unix_time) VALUES (1, (%s), (%s));",
                              ("UNIX_TIME FROM " + API_URL, unix_time))
        else:
            await cur.execute("UPDATE responses SET unix_time = (%s) WHERE url = (%s);",
                              (unix_time, "UNIX_TIME FROM " + API_URL))
        await cur.execute("COMMIT;")
        await connection_async.close()

    async def lol():
        task = asyncio.create_task(mem())
        await task

    asyncio.run(lol())


if __name__ == '__main__':
    sleep(7)


    async def create_table():
        connection = await aiopg.connect(database="drama", user="drama_user", password="pass", host="db")
        cursor = await connection.cursor()
        await cursor.execute("BEGIN;")
        await cursor.execute(
            "CREATE TABLE IF NOT EXISTS responses (id serial PRIMARY KEY, url varchar, unix_time integer);")
        await cursor.execute("COMMIT;")
        await connection.close()


    async def mem():
        task = asyncio.create_task(create_table())
        await task


    asyncio.run(mem())

    scheduler = BlockingScheduler()
    scheduler.add_job(check_unix_time.send, 'interval', seconds=2)

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
