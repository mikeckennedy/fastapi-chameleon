import os

from fastapi import FastAPI
import fastapi_jinja


app = FastAPI()

folder = os.path.dirname(__name__)
template_folder = os.path.join(folder, "templates")
template_folder = os.path.abspath(template_folder)

fastapi_jinja.global_init(template_folder)


@app.get("/")
async def root():
  return {"message": "Hello World"}


@app.get("/jinja")
@fastapi_jinja.template("test.j2")
async def jinja_test():

  render_dict = {
    "title": "Test Title",
    "users": [
      {
        'url': 'test_url',
        'username': 'test_user',
      }
    ]
  }

  return render_dict
