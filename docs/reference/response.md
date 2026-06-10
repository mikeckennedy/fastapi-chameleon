## response()


Render a template and return it as a FastAPI response directly.


Usage

``` python
response(
    template_file,
    mimetype="text/html",
    status_code=200,
    **template_data,
)
```


Use this when you want a rendered `Response` without the [template()](template.md#fastapi_chameleon.template) decorator, for example to return a fully-formed response from a view that does its own branching. Requires [global_init()](global_init.md#fastapi_chameleon.global_init) to have been called first.


## Parameters


`template_file: str`  
The Chameleon template file to render (path relative to the template folder, `*.pt`).

`mimetype: str = ``"text/html"`  
The response media type. Defaults to `text/html`.

`status_code: int = ``200`  
The HTTP status code for the response. Defaults to `200`.

`template_data={}`  
Keyword arguments passed through to the template as variables.


## Returns


`fastapi.Response`  
A `fastapi.Response` containing the rendered HTML.


## Raises


`FastAPIChameleonException`  
If [global_init()](global_init.md#fastapi_chameleon.global_init) has not been called.
