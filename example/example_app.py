import asyncio
from pathlib import Path

import fastapi
import uvicorn

import fastapi_chameleon

app = fastapi.FastAPI()


@app.get("/")
@fastapi_chameleon.template('index.pt')
def hello_world():
    return {'message': "Let's go Chameleon and FastAPI!"}


@app.get('/async')
@fastapi_chameleon.template('async.pt')
async def async_world():
    await asyncio.sleep(.01)
    return {'message': "Let's go async Chameleon and FastAPI!"}


def add_chameleon():
    dev_mode = True

    BASE_DIR = Path(__file__).resolve().parent
    template_folder = (BASE_DIR / 'templates').as_posix()
    fastapi_chameleon.global_init(template_folder, auto_reload=dev_mode)


def main():
    add_chameleon()
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
