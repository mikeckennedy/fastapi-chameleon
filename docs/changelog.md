# Changelog

This changelog is generated automatically from [GitHub Releases](https://github.com/mikeckennedy/fastapi-chameleon/releases).


# v0.1.18

*2026-06-11* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.18)


## \[0.1.18\]


### Added

- Ship inline type information to consumers via a `py.typed` marker (PEP 561), so downstream type checkers can see the package's annotations.
- New `dev` optional-dependencies extra (`pip install fastapi-chameleon[dev]`) bundling `pytest`, `ty`, and `pyrefly`.
- A full documentation site built with Great Docs (Quarto), published at <https://mkennedy.codes/docs/fastapi-chameleon/>, including an auto-generated API reference from the package docstrings.
- Expanded PyPI keywords for better discoverability (templating, rendering, decorator, ASGI, Starlette, and more).


### Changed

- Tightened type hints across the public API so the package now passes both `ty` and `pyrefly` cleanly: `NoReturn` on [not_found()](reference/not_found.html#fastapi_chameleon.not_found) / [generic_error()](reference/generic_error.html#fastapi_chameleon.generic_error), typed decorator wrappers and casts, and annotations on [global_init()](reference/global_init.html#fastapi_chameleon.global_init), `clear()`, and [response()](reference/response.html#fastapi_chameleon.response).
- Removed the inaccurate `dict` element type on `**template_data`.
- Expanded Sphinx-style docstrings for the public API ([template](reference/template.html#fastapi_chameleon.template), the internal render path, `clear`) and added `:ivar:` documentation to the exception types.
- Rewrote `README.md` with a runnable quick start, full public-API reference, friendly-error and view-testing guides, dev-mode/caching notes, a docs badge, and corrected example-app and contributing instructions.


# v0.1.17

*2025-04-04* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.17)

Updates the type information on [template()](reference/template.html#fastapi_chameleon.template) decorator to pass type information across better, removing errors triggered in pyright and others.
