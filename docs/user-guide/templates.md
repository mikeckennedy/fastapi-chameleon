# Writing Templates

Chameleon templates are HTML files that happen to be alive. Open one in a browser and it renders as a static mockup. Hand it to the engine with some data and the same file becomes the page. That trick is possible because Chameleon's logic lives in attributes on ordinary elements, not in tags of its own.

If you have used Zope Page Templates or Pyramid, this is the TAL and METAL you already know. If you are arriving from Jinja or Django, the first thing to unlearn is `{% %}` and `{ }`. Chameleon has neither. Interpolation is `${expr}`, and loops and conditions are `tal:` attributes. After about an hour the syntax stops feeling foreign and starts feeling like your HTML got a promotion.


# Interpolation and expressions

Anything inside `${ }` is a Python expression, evaluated against the dict your view returned:

``` html
<h1>Hello, ${user.name.title()}!</h1>
<p>You have ${len(items)} item(s).</p>
```

Real Python, not a template dialect. Method calls, slicing, conditional expressions, `len()`, all of it.

Output is HTML-escaped by default, so a book title containing `<script>` is displayed, not executed. When you have markup you already trust, say a rendered Markdown description, use the `structure:` prefix to insert it unescaped:

``` html
<div tal:content="structure: raw_html"></div>
```


# TAL attributes

Here is the catalog page for Shelf Life, built from the handful of attributes that do most of the work:

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

Notice the placeholder text inside `tal:content` and `tal:replace`. It is what a designer sees when they open the file directly, and it vanishes when the engine renders the real value. Templates that double as their own mockups are one of Chameleon's quiet pleasures.

The full language is in the [Chameleon reference](https://chameleon.readthedocs.io/en/latest/reference.html).


# Shared layouts with METAL

Every page in the shop shares a header, a footer, and a stylesheet link. METAL macros are how Chameleon does what Jinja calls template inheritance: the layout defines a macro with named slots, and each page fills them in.

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

The `load:` expression resolves the layout relative to the current template file. The variables the view returned, `title` here, are visible inside the layout as well as the page, so the layout can set the browser tab title without any extra plumbing.


# Project layout

A folder structure that works well, and that the template name inference expects:

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

Both `.pt` and `.html` extensions work and Chameleon treats them identically. `.pt` announces "this is a page template" to anyone browsing the repo. `.html` gets syntax highlighting everywhere without configuration. The inference prefers `.html` and falls back to `.pt`, so pick one convention per project and stay with it. Explicit template names can use either.


# Editing templates while the server runs

Chameleon compiles each template to Python once and keeps the compiled version. That is fast, and it is also why your first edit to a template appears to do nothing. Pass `auto_reload=True` to [global_init()](../reference/global_init.md#fastapi_chameleon.global_init) during development and edits are picked up on the next request without a restart. Leave it off in production. See [Configuration](configuration.md).


# A note on undefined variables

Reference a variable the view did not return and Chameleon raises `NameError` at render time, naming the missing variable. FastAPI turns that into a `500`. It is the most common template error there is, and [Troubleshooting](troubleshooting.md) has the full catalogue of what can go wrong and what each message means.
