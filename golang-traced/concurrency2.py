import asyncio
import time


async def proc1():
    await asyncio.sleep(4)
    print(1)

async def proc2():
    await asyncio.sleep(5)
    print(2)

def main():
    async def parallel():
        await asyncio.gather(
            proc1(),
            proc2()
        )
    print(f"started at {time.strftime('%X')}")
    asyncio.run(parallel())  
    print(f"finished at {time.strftime('%X')}")

main()

