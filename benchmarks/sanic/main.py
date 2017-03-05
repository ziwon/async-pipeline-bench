from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)


async def somebody():
    return


@app.route("/")
async def hello(request):
    await somebody()
    return text("Hello world!")

app.run(host="0.0.0.0", port=8080)