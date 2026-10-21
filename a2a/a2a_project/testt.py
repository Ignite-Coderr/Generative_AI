import httpx, asyncio

async def main():
    for url in ["http://localhost:8001/a2a", "http://localhost:8002/a2a", "http://localhost:8003/a2a"]:
        try:
            r = await httpx.AsyncClient().post(
                url,
                json={"jsonrpc": "2.0", "id": 1, "method": "agent/getCard", "params": {}},
                timeout=5.0,
            )
            print(url, "->", r.status_code)
        except Exception as e:
            print(url, "ERROR:", e)

asyncio.run(main())