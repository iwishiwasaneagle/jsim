[![jSim](https://raw.githubusercontent.com/iwishiwasaneagle/jsim/master/docs/_static/banner.png "jSim")](https://github.com/iwishiwasaneagle/jsim)

[![CI](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CI.yml/badge.svg)](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CI.yml)
[![CD](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CD.yml/badge.svg)](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CD.yml)
[![GitHub](https://img.shields.io/github/license/iwishiwasaneagle/jsim)](https://github.com/iwishiwasaneagle/jsim/blob/master/LICENSE.txt)
[![codecov](https://codecov.io/gh/iwishiwasaneagle/jsim/branch/master/graph/badge.svg?token=0X0UFKI79W)](https://codecov.io/gh/iwishiwasaneagle/jsim)

SAR is a unique design problem for path planning with little exposure to research. The search planning is highly dependent on the environment, and what it contains. Many papers use Probability Distribution Maps (PDMs) to inform the algorithms to make better paths since less time taken to find a missing person means higher chance of survivability.

This simulation environment is built to accommodate my research into this topic but anyone interested is more than welcome to help me build it.

## Installation

```bash
pip install jsim-utils
```

## Usage

`Agent`, `Simulation`, and `Environment` are designed to be used as base classes. The developer must extend them as required. Have a look at the [examples][examples] for more insight.

## Docs

Build yourself with `tox -e docs` or visit the [hosted docs][docs]

## Making Changes & Contributing

This project uses `pre-commit`, please make sure to install it before making any changes:

```bash
pip install pre-commit
cd jsim
pre-commit install
```

It is a good idea to update the hooks to the latest version:

```bash
pre-commit autoupdate
```

## References

- Architecture heavily inspired by [http://incompleteideas.net/RLinterface/RLI-Cplusplus.html](http://incompleteideas.net/RLinterface/RLI-Cplusplus.html)

[docs]: https://http://jsim.janhendrikewers.uk/
[examples]: https://http://jsim.janhendrikewers.uk/examples/
