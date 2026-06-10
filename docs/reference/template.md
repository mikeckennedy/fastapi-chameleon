## template()


Decorate a FastAPI view method to render an HTML response.


Usage

``` python
template(template_file: Optional[Union[Callable[..., R], str]] = None, mimetype: str = "text/html") -> Callable[[Callable[P, R]], Callable[P, R]]
 
template(f: Callable[P, R]) -> Callable[P, R]
```


## Parameters


`template_file: str = None`  
Optional, the Chameleon template file (path relative to template folder, \*.pt).

`mimetype: str = ``"text/html"`  
The mimetype response (defaults to text/html).


## Returns


Decorator to be consumed by FastAPI
