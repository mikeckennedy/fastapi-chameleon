# Writing Templates

Chameleon templates are HTML files with a small attribute language on top. If you have used Zope Page Templates or Pyramid, it is the same TAL and METAL. If you are coming from Jinja or Django, the first thing to unlearn is `{% %}` and `{ }`: Chameleon has neither. Interpolation is `${expr}` and control flow lives in `tal:` attributes on ordinary elements.


# Interpolation and expressions

Anything inside `${ }` is a Python expression evaluated against the dict your view returned:

``` html
<h1>Hello, ${user.name.title()}!</h1>
<p>You have ${len(items)} item(s).</p>
```

Output is HTML-escaped by default. To insert markup you already trust, use the `structure:` prefix:

``` html
<div tal:content="structure: raw_html"></div>
```


# TAL attributes

``` html
<!-- Loop. The repeat variable exposes index, number, even, odd, first, last. -->
<li tal:repeat="item items" tal:attributes="class 'odd' if repeat.item.odd else 'even'">
  ${repeat.item.number}. ${item.name}
</li>

<!-- Condition. The element is omitted entirely when the expression is falsy. -->
<div tal:condition="user">Welcome back, ${user.name}.</div>
<div tal:condition="not user">Please sign in.</div>

<!-- Replace element content, or the whole element. -->
<span tal:content="message">placeholder shown in a browser preview</span>
<span tal:replace="formatted_date">2024-01-01</span>

<!-- Set attributes, semicolon-separated. Escaping is automatic. -->
<a tal:attributes="href item.url; class item.css_class">${item.name}</a>

<!-- Define a local variable. -->
<span tal:define="total sum(i.price for i in items)">Total: ${total}</span>
```

The full language is documented in the [Chameleon reference](https://chameleon.readthedocs.io/en/latest/reference.html).


# Shared layouts with METAL

METAL macros are how Chameleon does what Jinja calls template inheritance. The layout defines a macro with slots, and each page fills the slots.

**`templates/shared/layout.pt`**

``` html
<html metal:define-macro="layout">
  <head><title>${title}</title></head>
  <body>
    <main metal:define-slot="content">default content</main>
  </body>
</html>
```

**`templates/home/index.pt`**

``` html

  <div metal:fill-slot="content">
    <h1>${title}</h1>
  </div>

```

The `load:` expression resolves the layout relative to the current template file. The variables the view returned, `title` here, are visible inside the layout too.


# Project layout

A layout that works well, and that the template name inference expects:

``` text
my_app/
├── main.py                # global_init() here, before views are imported
├── views/
│   └── home.py            # def index(...) with bare @template looks for home/index.html, then home/index.pt
├── templates/
│   ├── home/
│   │   └── index.pt
│   ├── errors/
│   │   └── 404.pt         # default target of not_found()
│   └── shared/
│       └── layout.pt      # METAL macros
└── static/
```

Both `.pt` and `.html` extensions work. Chameleon treats them the same. The inference prefers `.html` and falls back to `.pt`, so pick one convention per project and stick to it. Explicit template names can use either.


# Editing templates while the server runs

Chameleon compiles each template once and caches it. Pass `auto_reload=True` to [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) during development so edits are picked up on the next request without restarting. Leave it off in production. See [Configuration](configuration.md).


# A note on undefined variables

Referencing a variable the view did not return raises `NameError` from Chameleon at render time, naming the missing variable. FastAPI turns that into a `500`. See [Troubleshooting](troubleshooting.md) for the full list of errors you may hit.
