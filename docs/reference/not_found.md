## not_found()


Short-circuit the current view and render a friendly 404 page.


Usage

``` python
not_found(four04template_file="errors/404.pt")
```


Call this from inside a [template()](template.md#fastapi_chameleon.template)-decorated view when a resource cannot be found. It raises an exception that the decorator catches and turns into an HTTP 404 response rendered from `four04template_file`. This function never returns normally.


## Parameters


`four04template_file: str = ``"errors/404.pt"`  
The template to render for the 404 response (path relative to the template folder). Defaults to `errors/404.pt`.


## Raises


`FastAPIChameleonNotFoundException`  
Always; this is how the 404 is signalled to the decorator.
