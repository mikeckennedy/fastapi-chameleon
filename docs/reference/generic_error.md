## generic_error()


Short-circuit the current view and render an error page with a custom status code.


Usage

``` python
generic_error(
    template_file,
    status_code,
    template_data=None,
)
```


Like [not_found()](not_found.md#fastapi_chameleon.not_found), but for any error: call it from inside a [template()](template.md#fastapi_chameleon.template)-decorated view to render `template_file` with the HTTP `status_code` you choose (for example `401` or `500`). The decorator catches the raised exception and builds the response. This function never returns normally.


## Parameters


`template_file: str`  
The error template to render (path relative to the template folder).

`status_code: int`  
The HTTP status code to return (for example `fastapi.status.HTTP_401_UNAUTHORIZED`).

`template_data: dict = None`  
Optional variables passed to the template. Defaults to `None` (an empty context).


## Raises


`FastAPIChameleonGenericException`  
Always; this is how the error is signalled to the decorator.
