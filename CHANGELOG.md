# Changelog

All notable changes to **fastapi-chameleon** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> The published changelog at
> <https://mkennedy.codes/docs/fastapi-chameleon/changelog.html> is generated
> from GitHub Releases. This file is the source-tree record and is maintained
> by hand.

## [Unreleased]

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
