# Glotter2-Core

[![Makefile CI](https://github.com/rzuckerm/glotter2-core/actions/workflows/makefile.yml/badge.svg)](https://github.com/rzuckerm/glotter2-core/actions/workflows/makefile.yml)
[![Coverage](https://rzuckerm.github.io/glotter2-core/badge.svg)](https://rzuckerm.github.io/glotter2-core/html_cov)
[![PyPI version](https://img.shields.io/pypi/v/glotter2-core)](https://pypi.org/project/glotter2-core)
[![Python Versions](https://img.shields.io/pypi/pyversions/glotter2-core)](https://pypi.org/project/glotter2-core)
[![Python wheel](https://img.shields.io/pypi/wheel/glotter2-core)](https://pypi.org/project/glotter2-core)

[![Glotter2 logo](https://rzuckerm.github.io/glotter2-core/_static/glotter2_small.png)](https://rzuckerm.github.io/glotter2-core/)

*The programming language icons were downloaded from [pngegg.com](https://www.pngegg.com/)*

This package is a simple, lightweight core library for [glotter2](https://github.com/rzuckerm/glotter2).
It can be used instead of Glotter2 when all that is needed is project and test information.

For getting started with Glotter2-Core, refer to our [documentation](https://rzuckerm.github.io/glotter2-core/).

## Contributing

If you'd like to contribute to Glotter2-Core, read our [contributing guidelines](./CONTRIBUTING.md).

## Changelog

### Glotter2-Core releases

* 0.1.2:
  * Add project dictionary to `CoreProject` class
  * Add `CoreLanguage` class
  * Remove `testinfo` field from `CoreSourceCategories` class
  * Modify `by_language` field in `CoreSourceCategories` class
    to be `dict[str, CoreLanguage]`
* 0.1.1:
  * Convert `untestable.yml` to the equivalent `testinfo.yml`
* 0.1.0:
  * Initial release
