## exceptions.FastAPIChameleonGenericException


Signals an arbitrary error response from inside a decorated view.


Usage

``` python
exceptions.FastAPIChameleonGenericException()
```


Raised by [generic_error()](generic_error.md#fastapi_chameleon.generic_error) and caught by the [template()](template.md#fastapi_chameleon.template) decorator, which renders `template_file` with the chosen `status_code`. You normally raise it indirectly via [generic_error()](generic_error.md#fastapi_chameleon.generic_error) rather than constructing it yourself.
