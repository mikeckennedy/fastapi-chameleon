## template()


Decorate a FastAPI view to render its return value through a Chameleon template.


Usage

``` python
template(template_file: Optional[Union[Callable[..., R], str]] = None, mimetype: str = "text/html") -> Callable[[Callable[P, R]], Callable[P, R]]
 
template(f: Callable[P, R]) -> Callable[P, R]
```


Works on both sync and async view functions, and can be used three ways:

``` python
@template('home/index.pt')   # explicit template file
@template()                  # infer the template name
@template                    # bare form, also infers the name
```

When no template file is given, the name is inferred as `{module}/{function}` under the template folder (the module's last dotted segment and the view's name), preferring a `.html` file and falling back to `.pt`.

The decorated view should return a `dict` (used as the template's variables). If it returns a `fastapi.Response` instead, the template is skipped and the response is passed through unchanged. Returning anything else raises [FastAPIChameleonException](exceptions.FastAPIChameleonException.md#fastapi_chameleon.exceptions.FastAPIChameleonException).


## Parameters


`template_file: Optional[Union[Callable[…, R], str]] = None`  
The Chameleon template file (path relative to the template folder). Omit it (or pass `None`) to infer the name from the view. In the bare `@template` form this argument receives the view function itself.

`mimetype: str = ``"text/html"`  
The response media type. Defaults to `text/html`.


## Returns


The decorated view (bare form) or a decorator to apply to the view.
