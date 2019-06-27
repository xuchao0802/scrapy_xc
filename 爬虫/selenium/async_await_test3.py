#asyncio的wait_for
import asyncio
async def eternity():
    # Sleep for one hour
    await asyncio.sleep(4)
    print('yay!')

async def main():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(eternity(), timeout=5.0)
    except asyncio.TimeoutError:
        print('timeout!')

asyncio.run(main())