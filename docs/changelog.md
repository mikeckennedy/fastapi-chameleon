# Changelog

This changelog is generated automatically from [GitHub Releases](https://github.com/mikeckennedy/fastapi-chameleon/releases).


# v0.1.19

*2026-11-07* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.19)


## \[0.1.19\]


### Fixed

- [global_init()](reference/global_init.html#fastapi_chameleon.global_init) now accepts any `os.PathLike` (such as `pathlib.Path`) as the template folder. Previously a `Path` passed validation but every render then failed inside Chameleon's loader with `TypeError: 'PosixPath' object is not iterable`.
- The `dev` optional-dependencies extra is installable on Python 3.10 again: `great-docs` (which needs 3.11+) now carries a `python_version` marker.


### Documentation

- New user guide at <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/getting-started.html>: Getting Started, Decorating Views, Writing Templates, Friendly Error Pages, Troubleshooting, Testing and CI, Configuration, How It Works, and FAQ. Its pages are included in `llms-full.txt`.
- Replaced the auto-generated Agent Skill with a hand-written `skills/fastapi-chameleon/SKILL.md` covering the rules of the package (init order, return contract, where [not_found()](reference/not_found.html#fastapi_chameleon.not_found) works, TAL not Jinja) rather than only its API names.
- Added `Example` blocks to every public docstring and an entry-point overview to the package docstring.
- README links each section to the guide page that expands it, documents Python 3.15 support, and uses `Path` objects with [global_init()](reference/global_init.html#fastapi_chameleon.global_init).
- `scripts/build_docs.py` now fails when `llms.txt`, `llms-full.txt`, or the skill files are missing from the built site.
- The docs build requires `great-docs>=0.17` (pinned in `requirements-dev.txt`). The 0.13 release that was in the project venv silently drops the `package-info` page, the lightbox assets, and the `Llms-txt` lines in `robots.txt`.
- `ruff.toml` limits Ruff to Python sources and skips `docs/` and `great-docs/`, because Ruff 0.17 formats code blocks inside Markdown by default and would rewrap README and SKILL.md snippets.
- `tox.ini` adds a `py315` environment.
- Tidied `pyproject.toml`: removed the dead `[tool.setuptools]` table and the unused `hatch-vcs` build requirement, and corrected the sdist excludes (`/example_app` never existed, so the example app, docs site, and skill were shipping in the sdist).


# v0.1.16

*2026-11-07* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.16)


### Added

- [generic_error()](reference/generic_error.html#fastapi_chameleon.generic_error) accepts `template_data` so error templates can render dynamic content ([\#26](https://github.com/mikeckennedy/fastapi-chameleon/issues/26), PR [\#27](https://github.com/mikeckennedy/fastapi-chameleon/issues/27) by VLPatton).
- Example FastAPI app under `example/`.


### Changed

- Packaging moved from `setup.py` to `pyproject.toml` with the hatchling backend.
- Ruff adopted for linting and formatting; classifiers and tox environments updated for current Python versions.

Note: 0.1.13 and 0.1.15 were bumped in source but never uploaded to PyPI.

*Backfilled release record. Published to PyPI on 2024-11-10.*


# v0.1.14

*2026-11-07* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.14)


### Added

- `generic_error(template_file, status_code)`: render any error template with a chosen HTTP status code, the general form of [not_found()](reference/not_found.html#fastapi_chameleon.not_found). Exported from the package (including `from fastapi_chameleon import *`).


### Changed

- Build fix: the package build locates the requirements file again.

*Backfilled release record. Published to PyPI on 2023-02-11.*


# v0.1.12

*2026-11-07* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.12)


### Changed

- Added type information to several more return types in the engine.

*Backfilled release record. Published to PyPI on 2021-10-12.*


# v0.1.11

*2026-11-07* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.11)


### Changed

- README documents the friendly 404 feature introduced in 0.1.10. No code changes.

*Backfilled release record. Published to PyPI on 2021-07-30.*


# v0.1.10

*2026-11-07* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.10)


### Added

- Friendly 404 pages: call [not_found()](reference/not_found.html#fastapi_chameleon.not_found) from anywhere below a decorated view to render a 404 template (`errors/404.pt` by default) instead of FastAPI's JSON error.

*Backfilled release record. Published to PyPI on 2021-07-30.*


# v0.1.9

*2026-11-07* · [GitHub](https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.9)

First release published to PyPI (closes [\#10](https://github.com/mikeckennedy/fastapi-chameleon/issues/10)). Adds Chameleon template rendering to FastAPI via [global_init()](reference/global_init.html#fastapi_chameleon.global_init) and the `[@template](https://github.com/template)` decorator, with convention-based template lookup (`{module}/{function}.html`, falling back to `.pt`).

*Backfilled release record. Published to PyPI on 2021-07-27.*


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
