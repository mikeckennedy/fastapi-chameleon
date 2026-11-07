# Changelog

All notable changes to **fastapi-chameleon** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> The published changelog at
> <https://mkennedy.codes/docs/fastapi-chameleon/changelog.html> is generated
> from GitHub Releases. This file is the source-tree record and is maintained
> by hand.

## [Unreleased]

### Fixed

- `global_init()` now accepts any `os.PathLike` (such as `pathlib.Path`) as the template folder. Previously a `Path` passed validation but every render then failed inside Chameleon's loader with `TypeError: 'PosixPath' object is not iterable`.
- The `dev` optional-dependencies extra is installable on Python 3.10 again: `great-docs` (which needs 3.11+) now carries a `python_version` marker.

### Documentation

- New user guide at <https://mkennedy.codes/docs/fastapi-chameleon/user-guide/getting-started.html>: Getting Started, Decorating Views, Writing Templates, Friendly Error Pages, Troubleshooting, Testing and CI, Configuration, How It Works, and FAQ. Its pages are included in `llms-full.txt`.
- Replaced the auto-generated Agent Skill with a hand-written `skills/fastapi-chameleon/SKILL.md` covering the rules of the package (init order, return contract, where `not_found()` works, TAL not Jinja) rather than only its API names.
- Added `Example` blocks to every public docstring and an entry-point overview to the package docstring.
- README links each section to the guide page that expands it, documents Python 3.15 support, and uses `Path` objects with `global_init()`.
- `scripts/build_docs.py` now fails when `llms.txt`, `llms-full.txt`, or the skill files are missing from the built site.
- The docs build requires `great-docs>=0.17` (pinned in `requirements-dev.txt`). The 0.13 release that was in the project venv silently drops the `package-info` page, the lightbox assets, and the `Llms-txt` lines in `robots.txt`.
- `ruff.toml` limits Ruff to Python sources and skips `docs/` and `great-docs/`, because Ruff 0.17 formats code blocks inside Markdown by default and would rewrap README and SKILL.md snippets.
- `tox.ini` adds a `py315` environment.
- Tidied `pyproject.toml`: removed the dead `[tool.setuptools]` table and the unused `hatch-vcs` build requirement, and corrected the sdist excludes (`/example_app` never existed, so the example app, docs site, and skill were shipping in the sdist).

## [0.1.18]

### Added

- Ship inline type information to consumers via a `py.typed` marker (PEP 561),
  so downstream type checkers can see the package's annotations.
- New `dev` optional-dependencies extra (`pip install fastapi-chameleon[dev]`)
  bundling `pytest`, `ty`, and `pyrefly`.
- A full documentation site built with Great Docs (Quarto), published at
  <https://mkennedy.codes/docs/fastapi-chameleon/>, including an auto-generated
  API reference from the package docstrings.
- Expanded PyPI keywords for better discoverability (templating, rendering,
  decorator, ASGI, Starlette, and more).

### Changed

- Tightened type hints across the public API so the package now passes both
  `ty` and `pyrefly` cleanly: `NoReturn` on `not_found()` / `generic_error()`,
  typed decorator wrappers and casts, and annotations on `global_init()`,
  `clear()`, and `response()`.
- Removed the inaccurate `dict` element type on `**template_data`.
- Expanded Sphinx-style docstrings for the public API (`template`, the internal
  render path, `clear`) and added `:ivar:` documentation to the exception types.
- Rewrote `README.md` with a runnable quick start, full public-API reference,
  friendly-error and view-testing guides, dev-mode/caching notes, a docs badge,
  and corrected example-app and contributing instructions.

## [0.1.17]

- Baseline release prior to the documentation and typing work above.

[Unreleased]: https://github.com/mikeckennedy/fastapi-chameleon/compare/v0.1.18...HEAD
[0.1.18]: https://github.com/mikeckennedy/fastapi-chameleon/compare/v0.1.17...v0.1.18
[0.1.17]: https://github.com/mikeckennedy/fastapi-chameleon/releases/tag/v0.1.17
