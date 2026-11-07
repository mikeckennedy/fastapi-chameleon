## exceptions.FastAPIChameleonGenericException


Signals an arbitrary error response from inside a decorated view.


Usage

``` python
exceptions.FastAPIChameleonGenericException(
    template_file, status_code, message=None, template_data=None
)
```


Raised by [generic_error()](generic_error.md#fastapi_chameleon.generic_error) and caught by the [template()](template.md#fastapi_chameleon.template) decorator, which renders `template_file` with the chosen `status_code`. You normally raise it indirectly via [generic_error()](generic_error.md#fastapi_chameleon.generic_error) rather than constructing it yourself.

## Examples

``` python
try:
    fastapi_chameleon.generic_error('errors/403.pt', 403, template_data={'user': user})
except FastAPIChameleonGenericException as e:
    assert e.status_code == 403 and e.template_data == {'user': user}
```


## Attributes


`template_file: str`  
The template to render for the error response.

`status_code: int`  
The HTTP status code to return.

`message: Optional[str]`  
The optional human-readable message describing the error.

`template_data: Optional[dict]`  
Optional variables passed to the template when rendering.
