---
name: fastapi-chameleon
description: >
  Adds integration of the Chameleon template language to FastAPI. Use when writing Python code that uses the fastapi_chameleon package.
license: MIT
compatibility: Requires Python >=3.10.
---

# FastAPI Chameleon

Adds integration of the Chameleon template language to FastAPI.

## Installation

```bash
pip install fastapi-chameleon
```

## When to use what

| Need | Use |
|------|-----|
| Render a Chameleon template from a FastAPI view (sync or async) | `@fastapi_chameleon.template('home/index.pt') on the view function` |
| Return a friendly HTML 404 page instead of FastAPI's JSON default | `fastapi_chameleon.not_found()` |
| Render any error template with any status code (optionally with data) | `fastapi_chameleon.generic_error(template_file, status_code, template_data={...})` |
| Build a rendered Response with a custom status code or mimetype | `fastapi_chameleon.response(template_file, mimetype=..., status_code=..., **model)` |
| Redirect (or return JSON) from a decorated view | `return a fastapi.Response subclass — the template is skipped` |
| Get rendered HTML as a plain string | `fastapi_chameleon.engine.render(template_file, **model)` |

## API overview

### Setup

Point the library at your Chameleon templates folder once at app startup.

- `global_init`: Initialize the Chameleon template engine for your app

### Rendering views

Decorate FastAPI view functions to render templates, or build a response directly.

- `template`: Decorate a FastAPI view to render its return value through a Chameleon template
- `response`: Render a template and return it as a FastAPI response directly

### Error responses

Short-circuit a view to render a friendly error page with the right status code.

- `not_found`: Short-circuit the current view and render a friendly 404 page
- `generic_error`: Short-circuit the current view and render an error page with a custom status code

### Exceptions

Exception types raised by the library (the error helpers raise these internally).

- `exceptions.FastAPIChameleonException`
- `exceptions.FastAPIChameleonNotFoundException`
- `exceptions.FastAPIChameleonGenericException`

## Gotchas

1. global_init() is one-shot by default: with cache_init=True, later calls are silently ignored. Pass cache_init=False or call fastapi_chameleon.engine.clear() to re-initialize.
2. The bare @template form resolves the template file name once, at decoration time — if global_init() hasn't run yet, the folder silently defaults to 'templates' relative to the CWD and a later global_init() won't re-resolve it.
3. Decorated views must return a dict (the template model) or a fastapi.Response; any other return type raises FastAPIChameleonException at request time.
4. The decorator keyword is mimetype (not content_type), and @template has no status_code parameter — use response() when you need a non-200 status.
5. Error pages from not_found()/generic_error() always render as text/html at their own status; the decorator's mimetype does not apply.
6. not_found() renders the 404 template with an empty model; only generic_error() can pass template_data into the error template.
7. not_found()/generic_error() only work below a @template-decorated view — from an undecorated route or middleware the exception goes unhandled and FastAPI returns a 500.

## Best practices

- Call global_init(template_folder, auto_reload=dev_mode) exactly once at app startup, before view modules are imported/registered.
- Put the route decorator outermost: @app.get(...) above @fastapi_chameleon.template(...), which sits directly on the view function.
- Return plain dicts from views; return a fastapi.Response only for redirects and other pass-through cases.
- Enable auto_reload only during development so templates stay cached in production.
- Use fastapi_chameleon.response() where the decorator doesn't fit — custom status codes, non-HTML mimetypes, or rendering outside a view.

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


## Resources

- [Full documentation](https://mkennedy.codes/docs/fastapi-chameleon/)
- [llms.txt](llms.txt) — Indexed API reference for LLMs
- [llms-full.txt](llms-full.txt) — Comprehensive documentation for LLMs
- [Source code](https://github.com/mikeckennedy/fastapi-chameleon)
