## End-to-end wiring

A complete, minimal app — engine init, a decorated view, and the template it renders. The `@template` path is always relative to the folder passed to `global_init()`.

```python
# main.py
from pathlib import Path
import fastapi
import fastapi_chameleon

app = fastapi.FastAPI()

# Init once at startup, BEFORE any decorated view is defined.
templates = Path(__file__).resolve().parent / 'templates'
fastapi_chameleon.global_init(str(templates), auto_reload=True)  # auto_reload for dev only


@app.get('/')
@fastapi_chameleon.template('home/index.pt')   # route decorator OUTERMOST, @template just above the function
def index():
    return {'title': 'Home', 'items': ['a', 'b', 'c']}   # dict == the template model
```

```html
<!-- templates/home/index.pt -->
<!DOCTYPE html>
<html lang="en">
<body>
  <h1>${title}</h1>
  <ul>
    <li tal:repeat="item items">${item}</li>
  </ul>
</body>
</html>
```

The decorator is signature-transparent (ParamSpec overloads + `functools.wraps`), so FastAPI dependency injection — `Request`, path/query params, `Depends(...)` — keeps working on decorated views, sync or async.

## Chameleon template syntax (this is TAL, not Jinja)

Chameleon templates are valid XML/HTML where directives live in `tal:`, `metal:`, and `i18n:` attributes. There is no `{% ... %}` or `{{ ... }}` — do not use Jinja/Django syntax. Interpolation uses `${ ... }` and may contain arbitrary Python expressions.

```html
<!-- Interpolation: any Python expression inside ${ } -->
<h1>Hello, ${user.name.title()}!</h1>
<p>You have ${len(items)} item(s).</p>

<!-- Loop -->
<li tal:repeat="item items">${item.name} — ${item.price}</li>

<!-- The repeat variable exposes index/number/even/odd/first/last -->
<li tal:repeat="item items" tal:attributes="class 'odd' if repeat.item.odd else 'even'">
  ${repeat.item.number}. ${item}
</li>

<!-- Condition (element is omitted entirely when falsy) -->
<div tal:condition="user">Welcome back, ${user.name}.</div>
<div tal:condition="not user">Please sign in.</div>

<!-- Set element content / replace whole element -->
<span tal:content="message">placeholder shown only in a browser preview</span>
<span tal:replace="formatted_date">2024-01-01</span>

<!-- Set attributes (semicolon-separated); escaping is automatic -->
<a tal:attributes="href item.url; class item.css_class">${item.name}</a>

<!-- Define a reusable local variable -->
<span tal:define="total sum(i.price for i in items)">Total: ${total}</span>
```

Escaping is on by default (`${expr}` is HTML-escaped). Use `structure:` to emit already-safe HTML without escaping: `<div tal:content="structure: raw_html"></div>`.

## Shared layouts with METAL macros

METAL is how Chameleon does template inheritance / partials — the equivalent of Jinja's `{% extends %}`/`{% block %}`.

```html
<!-- templates/shared/layout.pt -->
<html metal:define-macro="layout">
  <head><title>${title}</title></head>
  <body>
    <main metal:define-slot="content">default content</main>
  </body>
</html>
```

```html
<!-- templates/home/index.pt -->
<div metal:use-macro="load: ../shared/layout.pt">
  <div metal:fill-slot="content">
    <h1>${title}</h1>
  </div>
</div>
```

## Template resolution & project layout

With an explicit path (`@template('catalog/item.pt')`) the string is resolved relative to the `global_init()` folder. With the bare form (`@template` or `@template()`) the path is derived **once at decoration time** as `{last segment of module}/{function_name}.html`, falling back to `.pt` if the `.html` file does not exist on disk.

```
my_app/
├── main.py                # global_init() here, before views are imported/defined
├── views/
│   └── home.py            # def index(...)  ->  bare @template looks for home/index.html|.pt
├── templates/
│   ├── home/index.pt
│   ├── errors/404.pt      # default target of not_found()
│   └── shared/layout.pt   # METAL macros
└── static/
```

## Redirects and pass-through responses

Return any `fastapi.Response` subclass from a decorated view and the template is skipped entirely — the idiomatic shape for POST/redirect/GET flows:

```python
@router.post('/account/login')
@fastapi_chameleon.template('account/login.pt')
async def login(request: fastapi.Request):
    user = await try_login(request)
    if user:
        return fastapi.responses.RedirectResponse('/account', status_code=302)
    return {'error': 'Invalid login'}  # falls through: re-render the form with an error
```

## Friendly error pages from anywhere below a view

`not_found()` and `generic_error()` are exception-based control flow: they always raise, the `@template` decorator catches, so they work from deep in a service or data layer — as long as a decorated view is above them on the call stack. FastAPI's default 404 is JSON; this is how you get an HTML error page instead.

```python
@router.get('/catalog/item/{item_id}')
@fastapi_chameleon.template('catalog/item.pt')
async def item(item_id: int):
    item = service.get_item_by_id(item_id)   # service may call not_found() itself
    if not item:
        fastapi_chameleon.not_found()        # renders errors/404.pt at 404, empty model
    return item.dict()

# Any status code, with data for the error template:
fastapi_chameleon.generic_error('errors/500.pt', 500, template_data={'detail': 'Something went sideways.'})
```

`not_found()` renders its template with an **empty** model; only `generic_error()` can pass `template_data` through. Both render as `text/html` regardless of the decorator's `mimetype`.

## Fetching the docs as Markdown

Every page on the documentation site has a plain-Markdown twin: swap the `.html` extension for `.md` to get token-efficient source without the site chrome. For example https://mkennedy.codes/docs/fastapi-chameleon/reference/template.html is also available at https://mkennedy.codes/docs/fastapi-chameleon/reference/template.md. Prefer the `.md` form when reading these docs programmatically.
