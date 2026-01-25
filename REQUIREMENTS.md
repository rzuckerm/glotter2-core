# Requirements

## Introduction

The purpose of this project is to provide a simple API that can be reused
in the following projects:

- [subete][subete]
- [ronbun][ronbun]

The code in this repo will be refactored out of the [glotter2][glotter2] repo,
but it will be simplified and lightweight such that it is only dependent on
[pyyaml].

## Subete

[Subete][subete] does the following that is in [glotter2][glotter2]:

- Read in `.glotter.yml` to get a list of projects
- Walk the `archive` directory to find a list of language paths, where a
- language path is a directory that contains only files. However,
  [glotter2][glotter2] looks specifically for directories that contain
  `testinfo.yml`. [Subete][subete] needs to find both testable and untestable
  languages, so this is probably not a good fit as is. A possible compromise
  would be to find all directories that have a specified set of files.
- TBD

## Ronbun

[Ronbun][ronbun] does the following that is in [glotter2][glotter2]:

- TBD

[subete]: https://github.com/TheRenegadeCoder/subete
[ronbun]: https://github.com/TheRenegadeCoder/sample-programs-readmes
[glotter2]: https://github.com/rzuckerm/glotter2
[pyyaml]: https://pypi.org/project/PyYAML/