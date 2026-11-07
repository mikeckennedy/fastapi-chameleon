# Decorating Views

A view in this package has one job: decide what to show. It looks at the request, talks to whatever data it needs, and returns a `dict`. It never touches HTML. The template does the showing, and the decorator is the handshake between them.

That split is the point. Views stay small and testable, templates stay editable by someone who never opens a Python file, and FastAPI keeps doing all the things it is good at underneath.


# Decorator order

The route decorator goes on the outside. `@fastapi_chameleon.template(...)` sits directly on the function.

``` python
@router.post('/')
@fastapi_chameleon.template('home/index.pt')
async def home_post(request: fastapi.Request):
    form = await request.form()
    vm = PersonViewModel(**form)
    return vm.model_dump()
```

FastAPI's dependency injection does not notice the decorator is there. Path parameters, query parameters, `Request`, and `Depends(...)` all resolve exactly as before, because the wrapper is built with `functools.wraps` and the decorator is typed with ParamSpec-based overloads. Your parameters still appear in the OpenAPI schema, and your type checker still sees the original signature.


# Three ways to name the template

``` python
@fastapi_chameleon.template('home/index.pt')   # explicit template file
@fastapi_chameleon.template()                  # inferred template name
@fastapi_chameleon.template                    # bare form, also inferred
```

The explicit form is resolved relative to the folder you passed to [global_init()](../reference/global_init.md#fastapi_chameleon.global_init). Nothing clever happens, which is exactly why most people use it.

The inferred forms are for the tidy-minded. Leave the name off and the decorator works it out from where the view lives:

- The file is `{module}/{function_name}` under the template folder, where `module` is the last segment of the view's dotted module name.
- An `.html` file is preferred. If it does not exist, `.pt` is used.
- `def index()` in `views/home.py` resolves to `templates/home/index.html`, falling back to `templates/home/index.pt`.

Inference happens once, when the module is imported, so there is no filesystem lookup per request. It also means the engine must already know its folder when the view module is imported. If [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) has not run yet, the folder silently defaults to `templates` relative to the current working directory, and a later [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) does not go back and re-resolve names that were already derived. Explicit template names never have this problem. Pick inference when your project layout is disciplined, and pick explicit names when you would rather read the path than remember the rule.


# What a view may return

Three outcomes, and only three.

| Return value | Result |
|----|----|
| `dict` | Rendered through the template as its variables. |
| any `fastapi.Response` | Passed through untouched. The template is skipped. |
| anything else (`None`, a Pydantic model, a list) | [FastAPIChameleonException](../reference/exceptions.FastAPIChameleonException.md#fastapi_chameleon.exceptions.FastAPIChameleonException) is raised at request time. |

The second row is how Shelf Life's login form works. A successful login should not render the login page again, it should send the customer to their account. Returning a `Response` says "I have already decided what to send, step aside":

``` python
@router.post('/account/login')
@fastapi_chameleon.template('account/login.pt')
async def login(request: fastapi.Request):
    user = await try_login(request)
    if user:
        return fastapi.responses.RedirectResponse('/account', status_code=302)

    return {'error': 'Invalid login'}  # re-render the form with an error
```

The third row is strict on purpose. A view that returns `None` because someone forgot the `return` statement, or returns a Pydantic model straight from the database layer, fails loudly with `Invalid return type <class 'NoneType'>` rather than rendering a blank page at 2am. Convert first: `model.model_dump()` for Pydantic, `dataclasses.asdict(obj)` for dataclasses, `{'books': books}` for a list.


# Non-HTML output

Templates are not only for pages. Shelf Life's sitemap is a Chameleon template too, and the decorator takes a `mimetype` for exactly that:

``` python
@router.get('/sitemap.xml')
@fastapi_chameleon.template('seo/sitemap.pt', mimetype='application/xml')
def sitemap():
    return {'urls': load_urls()}
```

A rendered dict always goes out with status `200`. Error pages raised with [not_found()](../reference/not_found.md#fastapi_chameleon.not_found) or [generic_error()](../reference/generic_error.md#fastapi_chameleon.generic_error) ignore this `mimetype` and are always `text/html`, because a browser that asked for a sitemap and got a 404 should still see a readable page. See [Friendly Error Pages](error-pages.md).


# Manual rendering with [response()](../reference/response.md#fastapi_chameleon.response)

Sometimes you want the wheel. A status code other than `200`, a view that renders one of several different templates depending on the data, a response assembled outside a route entirely. For those, skip the decorator and call [response()](../reference/response.md#fastapi_chameleon.response):

``` python
@router.get('/report')
def report():
    return fastapi_chameleon.response('reports/summary.pt', status_code=202, title='Monthly summary')
```

It renders the template with the keyword arguments as the model and returns a `fastapi.Response` with the given `mimetype` (default `text/html`) and `status_code` (default `200`). It needs [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) to have run, like everything else in the package.

And when you want the HTML as a plain string, say for the body of a confirmation email or an assertion in a test, use `fastapi_chameleon.engine.render(template_file, **model)`.


# Reference

- [template()](../reference/template.md)
- [response()](../reference/response.md)
