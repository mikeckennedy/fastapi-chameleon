## exceptions.FastAPIChameleonNotFoundException


Signals a 404 response from inside a decorated view.


Usage

``` python
exceptions.FastAPIChameleonNotFoundException(
    message=None, four04template_file="errors/404.pt"
)
```


Raised by [not_found()](not_found.md#fastapi_chameleon.not_found) and caught by the [template()](template.md#fastapi_chameleon.template) decorator, which renders `template_file` with an HTTP 404 status. You normally raise it indirectly via [not_found()](not_found.md#fastapi_chameleon.not_found) rather than constructing it yourself.

## Examples

``` python
try:
    fastapi_chameleon.not_found('errors/custom_404.pt')
except FastAPIChameleonNotFoundException as e:
    assert e.template_file == 'errors/custom_404.pt'
```


## Attributes


`template_file: str`  
The template to render for the 404 response (the constructor accepts it as `four04template_file`).

`message: Optional[str]`  
The optional human-readable message describing the error.
