from aiohttp import web


async def health(request):
    return web.Response(
        text="birthday bot alive"
    )


async def start_webserver():
    app = web.Application()

    app.router.add_get("/", health)

    runner = web.AppRunner(app)

    await runner.setup()

    port = 10000

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(
        f"Webserver started on {port}"
    )
