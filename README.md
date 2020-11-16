# fastapi-chameleon

Adds integration of the Chameleon template language to FastAPI. If you are interested in Jinja instead, see the sister project: [github.com/AGeekInside/fastapi-jinja](https://github.com/AGeekInside/fastapi-jinja).

## Installation

For the moment, this is not yet on pypi and is fairly unstable, but if you wish to used it directly from here, just do the following:

```bash
pip install git+https://github.com/mikeckennedy/fastapi-chameleon
```

You may want to fork this repo and then use your URL until this is more final.

## Usage

This is easy to use. Just create a folder within your web app to hold the templates such as:

```
├── main.py
├── views.py
│
├── templates
│   ├── home
│   │   └── index.pt
│   └── shared
│       └── layout.pt

```

In the app startup, tell the library about the folder you wish to use:

```python
import os
import fastapi_chameleon

dev_mode = True

folder = os.path.dirname(__file__)
template_folder = os.path.join(folder, 'templates')
template_folder = os.path.abspath(template_folder)

fastapi_chameleon.global_init(template_folder, auto_reload=dev_mode)
```

Then just decorate the FastAPI view methods (works on sync and async methods):

```python
@router.post('/')
@fastapi_chameleon.template('home/index.pt')
async def home_post(request: Request):
    form = await request.form()
    vm = PersonViewModel(**form) 

    return vm.dict() # {'first':'Michael', 'last':'Kennedy', ...}

```

The view method should return a `dict` to be passed as variables/values to the template. 

If a `fastapi.Response` is returned, the template is skipped and the response along with status_code and
other values is directly passed through. This is common for redirects and error responses not meant
for this page template.
