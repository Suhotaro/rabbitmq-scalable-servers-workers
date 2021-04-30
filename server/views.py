from aiohttp import web


async def ping(request):
    return web.json_response({"result": "pong"})


async def task(request):
    # TODO: json request
    result = await request.app["rabbit"].request({"id": "add", "arg1":2, "arg2":10})
    return web.json_response({'result': result})
