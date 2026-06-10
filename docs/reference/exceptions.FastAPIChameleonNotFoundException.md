## exceptions.FastAPIChameleonNotFoundException


Signals a 404 response from inside a decorated view.


Usage

``` python
exceptions.FastAPIChameleonNotFoundException()
```


Raised by [not_found()](not_found.md#fastapi_chameleon.not_found) and caught by the [template()](template.md#fastapi_chameleon.template) decorator, which renders `template_file` with an HTTP 404 status. You normally raise it indirectly via [not_found()](not_found.md#fastapi_chameleon.not_found) rather than constructing it yourself.
