from japronto import Application

async def somebody():
    return

async def hello(request):
    await somebody()
    return request.Response(text='Hello world!')

app = Application()
app.router.add_route('/', hello)
app.run(host='0.0.0.0', port=8080)